-- =============================================================================
-- OPENCLAW - SCHEMA DIGITAL.AI RELEASE INCIDENTS
-- =============================================================================
-- Version: 1.0
-- Date: Avril 2026
-- Références: ADR-014, ADR-015
-- =============================================================================

-- =============================================================================
-- TABLE: dai_incidents
-- Description: Incidents releases Digital.ai détectés par polling
-- =============================================================================
CREATE TABLE IF NOT EXISTS dai_incidents (
    -- Identifiants
    id TEXT PRIMARY KEY,                    -- UUID v4 interne
    release_id TEXT NOT NULL UNIQUE,        -- ID release DAI (Applications/...)
    release_title TEXT NOT NULL,
    release_url TEXT,
    template_id TEXT,                       -- Template source
    template_title TEXT,
    folder_id TEXT,                         -- Folder DAI
    
    -- État
    status TEXT NOT NULL DEFAULT 'detecting',
    -- Values: detecting, collecting, analyzing, ready, failed, resolved
    
    release_status TEXT NOT NULL,           -- IN_PROGRESS, FAILED, FAILING, PAUSED, COMPLETED, ABORTED
    previous_status TEXT,                   -- Pour détecter transitions
    
    -- Phase/Task en erreur
    failed_phase_id TEXT,
    failed_phase_title TEXT,
    failed_task_id TEXT,
    failed_task_title TEXT,
    failed_task_type TEXT,                  -- xlrelease.Task, jenkins.Build, etc.
    
    -- Erreur
    error_category TEXT,                    -- task_failed, approval_timeout, gate_blocked, script_error
    error_message TEXT,                     -- Message erreur si disponible
    error_signature TEXT,                   -- Fingerprint pour déduplication
    
    -- Contexte release
    release_owner TEXT,
    release_start_date TIMESTAMP,
    release_due_date TIMESTAMP,
    release_tags TEXT,                      -- JSON array
    release_variables TEXT,                 -- JSON (variables non-sensibles)
    
    -- Diagnostic
    diagnostic_markdown TEXT,
    diagnostic_json TEXT,
    root_cause TEXT,
    impact_level TEXT,                      -- low, medium, high, critical
    recommendations TEXT,                   -- JSON array
    
    -- Actions
    teams_notified_at TIMESTAMP,
    bug_created_at TIMESTAMP,
    bug_id TEXT,
    bug_url TEXT,
    created_by_user TEXT,
    
    -- Résolution
    resolved_at TIMESTAMP,
    resolution_type TEXT,                   -- manual, auto_retry, skipped, aborted
    resolution_notes TEXT,
    
    -- Feedback
    feedback TEXT,
    feedback_comment TEXT,
    feedback_at TIMESTAMP,
    
    -- Debouncing
    notification_group_id TEXT,
    occurrence_count INTEGER DEFAULT 1,
    
    -- Timestamps
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_polled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_changed_at TIMESTAMP,
    
    -- Metadata
    openclaw_version TEXT,
    processing_time_ms INTEGER,
    llm_tokens_used INTEGER
);

-- Index
CREATE INDEX IF NOT EXISTS idx_dai_status ON dai_incidents(status);
CREATE INDEX IF NOT EXISTS idx_dai_release_status ON dai_incidents(release_status);
CREATE INDEX IF NOT EXISTS idx_dai_detected ON dai_incidents(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_dai_release_id ON dai_incidents(release_id);
CREATE INDEX IF NOT EXISTS idx_dai_template ON dai_incidents(template_id);
CREATE INDEX IF NOT EXISTS idx_dai_debounce ON dai_incidents(release_id, error_signature, detected_at);

-- =============================================================================
-- TABLE: dai_release_snapshots
-- Description: Snapshots état releases pour tracking progression
-- =============================================================================
CREATE TABLE IF NOT EXISTS dai_release_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    release_id TEXT NOT NULL,
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    release_status TEXT NOT NULL,
    active_phase_id TEXT,
    active_phase_title TEXT,
    active_task_id TEXT,
    active_task_title TEXT,
    completion_percentage INTEGER,          -- 0-100
    
    FOREIGN KEY (release_id) REFERENCES dai_incidents(release_id)
);

CREATE INDEX IF NOT EXISTS idx_snapshots_release ON dai_release_snapshots(release_id, snapshot_at DESC);

-- =============================================================================
-- TABLE: dai_tasks_failed
-- Description: Détails des tasks failed dans une release
-- =============================================================================
CREATE TABLE IF NOT EXISTS dai_tasks_failed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    task_title TEXT,
    task_type TEXT,
    phase_id TEXT,
    phase_title TEXT,
    failure_time TIMESTAMP,
    error_message TEXT,
    task_owner TEXT,
    retry_count INTEGER DEFAULT 0,
    
    FOREIGN KEY (incident_id) REFERENCES dai_incidents(id),
    UNIQUE(incident_id, task_id)
);

CREATE INDEX IF NOT EXISTS idx_tasks_incident ON dai_tasks_failed(incident_id);

-- =============================================================================
-- TABLE: dai_polling_state
-- Description: État du polling pour éviter doublons
-- =============================================================================
CREATE TABLE IF NOT EXISTS dai_polling_state (
    release_id TEXT PRIMARY KEY,
    last_status TEXT,
    last_polled_at TIMESTAMP,
    poll_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,          -- Pour circuit breaker
    next_poll_at TIMESTAMP
);

-- =============================================================================
-- TABLE: dai_circuit_breaker
-- Description: État circuit breaker pour API DAI
-- =============================================================================
CREATE TABLE IF NOT EXISTS dai_circuit_breaker (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- Single row
    state TEXT DEFAULT 'closed',            -- closed, open, half_open
    failure_count INTEGER DEFAULT 0,
    last_failure_at TIMESTAMP,
    opened_at TIMESTAMP,
    last_success_at TIMESTAMP
);

-- Init circuit breaker
INSERT OR IGNORE INTO dai_circuit_breaker (id, state) VALUES (1, 'closed');

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Vue: incidents DAI actifs
CREATE VIEW IF NOT EXISTS v_dai_active_incidents AS
SELECT 
    id,
    release_title,
    release_status,
    status,
    error_category,
    failed_task_title,
    detected_at,
    CAST((julianday('now') - julianday(detected_at)) * 24 * 60 AS INTEGER) as age_minutes
FROM dai_incidents
WHERE release_status IN ('IN_PROGRESS', 'FAILED', 'FAILING', 'PAUSED')
  AND status != 'resolved'
ORDER BY detected_at DESC;

-- Vue: stats releases
CREATE VIEW IF NOT EXISTS v_dai_stats AS
SELECT 
    date(detected_at) as date,
    COUNT(*) as total_incidents,
    SUM(CASE WHEN release_status = 'FAILED' THEN 1 ELSE 0 END) as failed,
    SUM(CASE WHEN release_status = 'COMPLETED' THEN 1 ELSE 0 END) as resolved,
    AVG(processing_time_ms) as avg_processing_ms
FROM dai_incidents
WHERE detected_at > datetime('now', '-30 days')
GROUP BY date(detected_at);

-- Vue: dashboard unifié (ADO + DAI)
CREATE VIEW IF NOT EXISTS v_unified_incidents AS
SELECT 
    id,
    'ado' as source,
    pipeline_name as title,
    build_url as url,
    status,
    error_category,
    detected_at,
    bug_id
FROM incidents
WHERE detected_at > datetime('now', '-7 days')

UNION ALL

SELECT 
    id,
    'dai' as source,
    release_title as title,
    release_url as url,
    status,
    error_category,
    detected_at,
    bug_id
FROM dai_incidents
WHERE detected_at > datetime('now', '-7 days')

ORDER BY detected_at DESC;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- Trigger: track status changes
CREATE TRIGGER IF NOT EXISTS trg_dai_status_change
AFTER UPDATE OF release_status ON dai_incidents
WHEN OLD.release_status != NEW.release_status
BEGIN
    UPDATE dai_incidents 
    SET previous_status = OLD.release_status,
        status_changed_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
    
    -- Snapshot
    INSERT INTO dai_release_snapshots (release_id, release_status)
    VALUES (NEW.release_id, NEW.release_status);
END;

-- Trigger: auto-resolve when COMPLETED
CREATE TRIGGER IF NOT EXISTS trg_dai_auto_resolve
AFTER UPDATE OF release_status ON dai_incidents
WHEN NEW.release_status = 'COMPLETED' AND OLD.status != 'resolved'
BEGIN
    UPDATE dai_incidents 
    SET status = 'resolved',
        resolved_at = CURRENT_TIMESTAMP,
        resolution_type = 'auto_completed'
    WHERE id = NEW.id;
END;
