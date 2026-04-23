"""
OpenClaw Dashboard - FastAPI Application MVP
=============================================
Référence: ADR-010, ADR-011, ADR-012, ADR-013
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import json

from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiosqlite

# =============================================================================
# CONFIG
# =============================================================================

DB_PATH = Path("openclaw.db")
TEMPLATES_DIR = Path("templates")
OPENCLAW_API = "http://localhost:8001"  # API interne OpenClaw

app = FastAPI(title="OpenClaw Dashboard", version="1.0.0")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# =============================================================================
# FILTERS JINJA2
# =============================================================================

def timeago_filter(dt: datetime) -> str:
    """Convert datetime to human-readable 'X ago' format."""
    if not dt:
        return "N/A"
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
    
    delta = datetime.utcnow() - dt
    
    if delta.seconds < 60:
        return "à l'instant"
    elif delta.seconds < 3600:
        mins = delta.seconds // 60
        return f"il y a {mins} min"
    elif delta.seconds < 86400:
        hours = delta.seconds // 3600
        return f"il y a {hours}h"
    else:
        days = delta.days
        return f"il y a {days}j"

templates.env.filters["timeago"] = timeago_filter

# =============================================================================
# DATABASE
# =============================================================================

async def get_db():
    """Get async SQLite connection."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def row_to_dict(row) -> dict:
    """Convert sqlite Row to dict with JSON parsing."""
    d = dict(row)
    # Parse JSON fields
    for key in ["files_changed", "recommendations", "diagnostic_json"]:
        if key in d and d[key]:
            try:
                d[key] = json.loads(d[key])
            except:
                pass
    return d

# =============================================================================
# ROUTES - PAGES HTML
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Page principale - liste incidents."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/incidents/{incident_id}", response_class=HTMLResponse)
async def incident_detail(
    request: Request,
    incident_id: str,
    db: aiosqlite.Connection = Depends(get_db)
):
    """Page détail incident."""
    cursor = await db.execute(
        "SELECT * FROM incidents WHERE id = ?", 
        (incident_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(404, "Incident non trouvé")
    
    incident = await row_to_dict(row)
    
    return templates.TemplateResponse("incident.html", {
        "request": request,
        "incident": incident
    })

# =============================================================================
# ROUTES - PARTIALS HTMX
# =============================================================================

@app.get("/incidents", response_class=HTMLResponse)
async def list_incidents(
    request: Request,
    status: Optional[str] = Query(None),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Liste incidents (partial HTMX)."""
    query = """
        SELECT id, pipeline_name, build_number, build_url, status, 
               error_category, detected_at, bug_id, bug_url
        FROM incidents
        WHERE detected_at > datetime('now', '-7 days')
    """
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY detected_at DESC LIMIT 50"
    
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    incidents = [await row_to_dict(row) for row in rows]
    
    return templates.TemplateResponse("partials/incident_list.html", {
        "request": request,
        "incidents": incidents
    })


@app.get("/incidents/{incident_id}/diagnostic", response_class=HTMLResponse)
async def get_diagnostic(
    request: Request,
    incident_id: str,
    db: aiosqlite.Connection = Depends(get_db)
):
    """Diagnostic incident (partial HTMX, refreshé toutes les 3s)."""
    cursor = await db.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(404)
    
    incident = await row_to_dict(row)
    
    return templates.TemplateResponse("partials/diagnostic.html", {
        "request": request,
        "incident": incident
    })

# =============================================================================
# ROUTES - ACTIONS
# =============================================================================

@app.post("/incidents/{incident_id}/create-bug", response_class=HTMLResponse)
async def create_bug(
    request: Request,
    incident_id: str,
    db: aiosqlite.Connection = Depends(get_db)
):
    """
    Crée bug ADO via OpenClaw (trust boundary).
    Dashboard n'a PAS de token ADO.
    """
    import httpx
    
    # Vérifier incident existe
    cursor = await db.execute(
        "SELECT id, bug_id FROM incidents WHERE id = ?",
        (incident_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(404, "Incident non trouvé")
    
    if row["bug_id"]:
        raise HTTPException(400, "Bug déjà créé")
    
    # TODO: Récupérer user_id depuis session auth
    user_id = "current_user"
    
    # Appeler OpenClaw API interne
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{OPENCLAW_API}/actions/create-bug",
                json={
                    "incident_id": incident_id,
                    "user_id": user_id
                },
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
        except httpx.RequestError as e:
            raise HTTPException(503, f"OpenClaw indisponible: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(e.response.status_code, e.response.text)
    
    return templates.TemplateResponse("partials/bug_created.html", {
        "request": request,
        "bug_id": result["bug_id"],
        "bug_url": result.get("bug_url", "#")
    })


@app.post("/incidents/{incident_id}/feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    incident_id: str,
    db: aiosqlite.Connection = Depends(get_db)
):
    """Soumettre feedback sur diagnostic."""
    form = await request.form()
    feedback = form.get("feedback")
    
    if feedback not in ["useful", "partial", "not_useful"]:
        raise HTTPException(400, "Feedback invalide")
    
    await db.execute(
        """UPDATE incidents 
           SET feedback = ?, feedback_at = CURRENT_TIMESTAMP 
           WHERE id = ?""",
        (feedback, incident_id)
    )
    await db.commit()
    
    # Log audit
    await db.execute(
        """INSERT INTO audit_log (action, incident_id, details)
           VALUES ('feedback', ?, ?)""",
        (incident_id, json.dumps({"feedback": feedback}))
    )
    await db.commit()
    
    return templates.TemplateResponse("partials/feedback_thanks.html", {
        "request": request
    })

# =============================================================================
# ROUTES - API JSON
# =============================================================================

@app.get("/api/incidents")
async def api_list_incidents(
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    db: aiosqlite.Connection = Depends(get_db)
):
    """API JSON liste incidents."""
    query = """
        SELECT * FROM incidents
        WHERE detected_at > datetime('now', '-7 days')
    """
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    query += f" ORDER BY detected_at DESC LIMIT {limit}"
    
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    
    return [await row_to_dict(row) for row in rows]


@app.get("/api/incidents/{incident_id}")
async def api_get_incident(
    incident_id: str,
    db: aiosqlite.Connection = Depends(get_db)
):
    """API JSON détail incident."""
    cursor = await db.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(404)
    
    return await row_to_dict(row)

# =============================================================================
# HEALTH & METRICS
# =============================================================================

@app.get("/health")
async def health():
    """Healthcheck endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/metrics")
async def metrics(db: aiosqlite.Connection = Depends(get_db)):
    """Prometheus-style metrics."""
    cursor = await db.execute("""
        SELECT 
            COUNT(*) as total_incidents,
            SUM(CASE WHEN status = 'ready' THEN 1 ELSE 0 END) as ready,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
            SUM(CASE WHEN bug_id IS NOT NULL THEN 1 ELSE 0 END) as bugs_created,
            AVG(processing_time_ms) as avg_processing_time_ms
        FROM incidents
        WHERE detected_at > datetime('now', '-24 hours')
    """)
    row = await cursor.fetchone()
    
    return {
        "incidents_24h_total": row["total_incidents"],
        "incidents_24h_ready": row["ready"],
        "incidents_24h_failed": row["failed"],
        "bugs_24h_created": row["bugs_created"],
        "avg_processing_time_ms": row["avg_processing_time_ms"]
    }

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    if not DB_PATH.exists():
        print(f"Creating database at {DB_PATH}")
        async with aiosqlite.connect(DB_PATH) as db:
            # Read schema.sql and execute
            schema_path = Path(__file__).parent / "schema.sql"
            if schema_path.exists():
                schema = schema_path.read_text()
                await db.executescript(schema)
                await db.commit()
                print("Database schema created")


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
