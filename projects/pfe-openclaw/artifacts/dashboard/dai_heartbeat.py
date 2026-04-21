"""
OpenClaw - Digital.ai Release Heartbeat Handler
================================================
Polling-based monitoring for DAI releases.
Référence: ADR-014, ADR-015

Usage:
    from dai_heartbeat import DAIHeartbeat
    
    heartbeat = DAIHeartbeat(db_path="openclaw.db")
    await heartbeat.start()
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import json

import aiosqlite

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIG
# =============================================================================

class PollMode(Enum):
    NORMAL = 60      # 60s default
    INCIDENT = 15    # 15s when active incident
    QUIET = 300      # 5min off-hours

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class DAIConfig:
    """Configuration polling DAI."""
    poll_intervals: Dict[str, int] = field(default_factory=lambda: {
        "normal": 60,
        "incident": 15,
        "quiet": 300
    })
    quiet_hours: tuple = (22, 6)  # 22h-6h
    circuit_breaker_threshold: int = 3
    circuit_breaker_timeout: int = 300  # 5min
    max_releases_per_poll: int = 50

# =============================================================================
# MCP CLIENT STUB (replace with actual MCP calls)
# =============================================================================

class MCPDAIClient:
    """
    Stub MCP client for Digital.ai Release.
    Replace with actual MCP implementation.
    """
    
    async def list_releases(
        self,
        active: bool = False,
        failing: bool = False,
        paused: bool = False,
        failed: bool = False,
        results_per_page: int = 50
    ) -> List[Dict]:
        """
        MCP: digitalai-release_list_releases
        Returns lightweight release overviews.
        """
        # TODO: Replace with actual MCP call
        # response = await mcp_call("digitalai-release_list_releases", {
        #     "request": {
        #         "active": active,
        #         "failing": failing,
        #         "paused": paused,
        #         "failed": failed,
        #         "results_per_page": results_per_page
        #     }
        # })
        # return response
        
        logger.warning("MCP stub: list_releases - implement with real MCP")
        return []
    
    async def get_release(self, release_id: str) -> Optional[Dict]:
        """
        MCP: digitalai-release_get_release
        Returns complete release with phases/tasks.
        """
        # TODO: Replace with actual MCP call
        logger.warning(f"MCP stub: get_release({release_id}) - implement with real MCP")
        return None
    
    async def get_activity_logs(self, release_id: str) -> List[Dict]:
        """
        MCP: digitalai-release_get_activity_logs
        Returns activity history.
        """
        logger.warning(f"MCP stub: get_activity_logs({release_id}) - implement with real MCP")
        return []

# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class DAIRelease:
    """Release summary from list_releases."""
    id: str
    title: str
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    folder_id: Optional[str] = None
    
    @classmethod
    def from_mcp(cls, data: Dict) -> "DAIRelease":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            status=data.get("status", "UNKNOWN"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            folder_id=data.get("folder_id")
        )

@dataclass
class DAIFailedTask:
    """Failed task details."""
    task_id: str
    task_title: str
    task_type: str
    phase_id: str
    phase_title: str
    error_message: Optional[str] = None

@dataclass
class DAIIncident:
    """Internal incident model."""
    id: str
    release_id: str
    release_title: str
    release_status: str
    status: str = "detecting"
    error_category: Optional[str] = None
    failed_tasks: List[DAIFailedTask] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)

# =============================================================================
# CIRCUIT BREAKER
# =============================================================================

class CircuitBreaker:
    """Circuit breaker for DAI API calls."""
    
    def __init__(self, db: aiosqlite.Connection, config: DAIConfig):
        self.db = db
        self.config = config
    
    async def get_state(self) -> CircuitState:
        cursor = await self.db.execute(
            "SELECT state, opened_at FROM dai_circuit_breaker WHERE id = 1"
        )
        row = await cursor.fetchone()
        if not row:
            return CircuitState.CLOSED
        
        state = CircuitState(row[0])
        
        # Check if should transition from OPEN to HALF_OPEN
        if state == CircuitState.OPEN and row[1]:
            opened_at = datetime.fromisoformat(row[1])
            if datetime.utcnow() - opened_at > timedelta(seconds=self.config.circuit_breaker_timeout):
                await self._set_state(CircuitState.HALF_OPEN)
                return CircuitState.HALF_OPEN
        
        return state
    
    async def record_success(self):
        await self.db.execute("""
            UPDATE dai_circuit_breaker 
            SET state = 'closed', 
                failure_count = 0,
                last_success_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """)
        await self.db.commit()
    
    async def record_failure(self):
        cursor = await self.db.execute(
            "SELECT failure_count FROM dai_circuit_breaker WHERE id = 1"
        )
        row = await cursor.fetchone()
        failure_count = (row[0] if row else 0) + 1
        
        if failure_count >= self.config.circuit_breaker_threshold:
            await self._set_state(CircuitState.OPEN)
            logger.error(f"Circuit breaker OPEN after {failure_count} failures")
        else:
            await self.db.execute("""
                UPDATE dai_circuit_breaker 
                SET failure_count = ?,
                    last_failure_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (failure_count,))
            await self.db.commit()
    
    async def _set_state(self, state: CircuitState):
        opened_at = "CURRENT_TIMESTAMP" if state == CircuitState.OPEN else "NULL"
        await self.db.execute(f"""
            UPDATE dai_circuit_breaker 
            SET state = ?,
                opened_at = {opened_at}
            WHERE id = 1
        """, (state.value,))
        await self.db.commit()

# =============================================================================
# HEARTBEAT HANDLER
# =============================================================================

class DAIHeartbeat:
    """
    Digital.ai Release polling heartbeat.
    
    Polls DAI API at configured intervals to detect:
    - FAILED releases
    - FAILING releases (task in progress failing)
    - PAUSED releases (blocked on approval)
    """
    
    def __init__(
        self,
        db_path: str = "openclaw.db",
        config: Optional[DAIConfig] = None
    ):
        self.db_path = db_path
        self.config = config or DAIConfig()
        self.mcp = MCPDAIClient()
        self._running = False
        self._db: Optional[aiosqlite.Connection] = None
        self._circuit_breaker: Optional[CircuitBreaker] = None
    
    async def start(self):
        """Start heartbeat loop."""
        self._running = True
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        self._circuit_breaker = CircuitBreaker(self._db, self.config)
        
        logger.info("DAI Heartbeat started")
        
        while self._running:
            try:
                await self._poll_cycle()
            except Exception as e:
                logger.exception(f"Poll cycle error: {e}")
                await self._circuit_breaker.record_failure()
            
            interval = await self._get_poll_interval()
            logger.debug(f"Next poll in {interval}s")
            await asyncio.sleep(interval)
    
    async def stop(self):
        """Stop heartbeat."""
        self._running = False
        if self._db:
            await self._db.close()
        logger.info("DAI Heartbeat stopped")
    
    async def _get_poll_interval(self) -> int:
        """Determine polling interval based on context."""
        # Check active incidents
        cursor = await self._db.execute("""
            SELECT COUNT(*) FROM dai_incidents 
            WHERE status NOT IN ('ready', 'resolved', 'failed')
        """)
        row = await cursor.fetchone()
        if row[0] > 0:
            return self.config.poll_intervals["incident"]
        
        # Check quiet hours
        hour = datetime.now().hour
        start, end = self.config.quiet_hours
        if hour >= start or hour < end:
            return self.config.poll_intervals["quiet"]
        
        return self.config.poll_intervals["normal"]
    
    async def _poll_cycle(self):
        """Execute one poll cycle."""
        # Check circuit breaker
        state = await self._circuit_breaker.get_state()
        if state == CircuitState.OPEN:
            logger.warning("Circuit breaker OPEN - skipping poll")
            return
        
        logger.debug("Starting DAI poll cycle")
        
        # Fetch problematic releases
        releases = await self._fetch_releases()
        
        if not releases:
            logger.debug("No problematic releases found")
            await self._circuit_breaker.record_success()
            return
        
        logger.info(f"Found {len(releases)} problematic releases")
        
        for release in releases:
            await self._process_release(release)
        
        await self._circuit_breaker.record_success()
    
    async def _fetch_releases(self) -> List[DAIRelease]:
        """Fetch releases needing attention."""
        try:
            raw_releases = await self.mcp.list_releases(
                active=True,
                failing=True,
                paused=True,
                failed=True,
                results_per_page=self.config.max_releases_per_poll
            )
            
            return [DAIRelease.from_mcp(r) for r in raw_releases]
        
        except Exception as e:
            logger.error(f"Failed to fetch releases: {e}")
            raise
    
    async def _process_release(self, release: DAIRelease):
        """Process single release."""
        # Check if already tracked
        cursor = await self._db.execute(
            "SELECT id, release_status FROM dai_incidents WHERE release_id = ?",
            (release.id,)
        )
        existing = await cursor.fetchone()
        
        if not existing:
            # New incident
            await self._create_incident(release)
        elif existing["release_status"] != release.status:
            # Status changed
            await self._update_incident(existing["id"], release)
        else:
            # Update poll timestamp
            await self._db.execute(
                "UPDATE dai_incidents SET last_polled_at = CURRENT_TIMESTAMP WHERE release_id = ?",
                (release.id,)
            )
            await self._db.commit()
    
    async def _create_incident(self, release: DAIRelease):
        """Create new DAI incident."""
        incident_id = str(uuid4())
        
        logger.info(f"New DAI incident: {release.title} ({release.status})")
        
        # Determine error category
        error_category = self._categorize_error(release.status)
        
        await self._db.execute("""
            INSERT INTO dai_incidents (
                id, release_id, release_title, release_status,
                status, error_category, detected_at
            ) VALUES (?, ?, ?, ?, 'detecting', ?, CURRENT_TIMESTAMP)
        """, (
            incident_id,
            release.id,
            release.title,
            release.status,
            error_category
        ))
        await self._db.commit()
        
        # If FAILED/FAILING, fetch details
        if release.status in ("FAILED", "FAILING"):
            await self._enrich_incident(incident_id, release.id)
        
        # Trigger diagnostic pipeline
        await self._trigger_diagnostic(incident_id)
    
    async def _update_incident(self, incident_id: str, release: DAIRelease):
        """Update existing incident with new status."""
        logger.info(f"DAI incident status change: {release.title} -> {release.status}")
        
        await self._db.execute("""
            UPDATE dai_incidents 
            SET release_status = ?,
                last_polled_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (release.status, incident_id))
        await self._db.commit()
        
        # Re-enrich if now FAILED
        if release.status in ("FAILED", "FAILING"):
            await self._enrich_incident(incident_id, release.id)
    
    async def _enrich_incident(self, incident_id: str, release_id: str):
        """Fetch full release details and enrich incident."""
        logger.debug(f"Enriching incident {incident_id}")
        
        release_details = await self.mcp.get_release(release_id)
        if not release_details:
            return
        
        # Find failed tasks
        failed_tasks = self._find_failed_tasks(release_details)
        
        for task in failed_tasks:
            await self._db.execute("""
                INSERT OR REPLACE INTO dai_tasks_failed (
                    incident_id, task_id, task_title, task_type,
                    phase_id, phase_title, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                incident_id,
                task.task_id,
                task.task_title,
                task.task_type,
                task.phase_id,
                task.phase_title,
                task.error_message
            ))
        
        # Update incident with first failed task info
        if failed_tasks:
            first = failed_tasks[0]
            await self._db.execute("""
                UPDATE dai_incidents SET
                    failed_phase_id = ?,
                    failed_phase_title = ?,
                    failed_task_id = ?,
                    failed_task_title = ?,
                    failed_task_type = ?,
                    error_message = ?
                WHERE id = ?
            """, (
                first.phase_id,
                first.phase_title,
                first.task_id,
                first.task_title,
                first.task_type,
                first.error_message,
                incident_id
            ))
        
        await self._db.commit()
    
    def _find_failed_tasks(self, release: Dict) -> List[DAIFailedTask]:
        """Extract failed tasks from release structure."""
        failed = []
        
        phases = release.get("phases", [])
        for phase in phases:
            phase_id = phase.get("id", "")
            phase_title = phase.get("title", "")
            
            tasks = phase.get("tasks", [])
            for task in tasks:
                if task.get("status") in ("FAILED", "FAILING"):
                    failed.append(DAIFailedTask(
                        task_id=task.get("id", ""),
                        task_title=task.get("title", ""),
                        task_type=task.get("type", "xlrelease.Task"),
                        phase_id=phase_id,
                        phase_title=phase_title,
                        error_message=task.get("failureMessage")
                    ))
        
        return failed
    
    def _categorize_error(self, release_status: str) -> str:
        """Map release status to error category."""
        mapping = {
            "FAILED": "release_failed",
            "FAILING": "task_failing",
            "PAUSED": "approval_blocked",
            "ABORTED": "release_aborted"
        }
        return mapping.get(release_status, "unknown")
    
    async def _trigger_diagnostic(self, incident_id: str):
        """
        Trigger diagnostic pipeline for incident.
        Updates status to 'analyzing'.
        """
        await self._db.execute(
            "UPDATE dai_incidents SET status = 'analyzing' WHERE id = ?",
            (incident_id,)
        )
        await self._db.commit()
        
        # TODO: Integrate with diagnostic pipeline
        # await diagnostic_pipeline.run(incident_id, source="dai")
        logger.info(f"Diagnostic triggered for DAI incident {incident_id}")

# =============================================================================
# STANDALONE RUN
# =============================================================================

async def main():
    """Run heartbeat standalone."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    heartbeat = DAIHeartbeat(db_path="openclaw.db")
    
    try:
        await heartbeat.start()
    except KeyboardInterrupt:
        await heartbeat.stop()

if __name__ == "__main__":
    asyncio.run(main())
