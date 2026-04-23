-- =============================================================================
-- OPENCLAW DASHBOARD - SCHÉMA SQLITE MVP
-- =============================================================================
-- Version: 1.0
-- Date: Avril 2026
-- Références: ADR-003, ADR-009, ADR-010
-- =============================================================================

PRAGMA journal_mode = WAL;          -- Write-Ahead Logging pour concurrence
PRAGMA foreign_keys = ON;           -- Intégrité référentielle
PRAGMA busy_timeout = 5000;         -- 5s timeout si lock

-- =============================================================================
-- TABLE: incidents
-- Description: Incidents pipeline détectés par OpenClaw
-- =============================================================================
CREATE TABLE IF NOT EXISTS incidents (
    -- Identifiants
    id TEXT PRIMARY KEY,                    -- UUID v4
    pipeline_id TEXT NOT NULL,              -- ID pipeline ADO
    pipeline_name TEXT NOT NULL,            -- Nom lisible
    build_id TEXT NOT NULL,                 -- ID build ADO
    build_number TEXT,                      -- Numéro build (#123)
    build_url TEXT,                         -- Lien vers ADO
    
    -- État
    status TEXT NOT NULL DEFAULT 'detecting',
    -- Values: detecting, collecting, extracting, correlating, analyzing, formatting, ready, failed
    
    -- Contexte Git
    commit_id TEXT,
    commit_message TEXT,
    commit_author TEXT,
    commit_author_email TEXT,
    branch_name TEXT,
    files_changed TEXT,                     -- JSON array ["file1.cs", "file2.ts"]
    
    -- Erreur
    error_category TEXT,                    -- compilation, test, package, deployment, timeout, resource
    error_signature TEXT,                   -- Fingerprint pour déduplication
    error_excerpt TEXT,                     -- Extrait log (max 2000 chars)
    error_line_number INTEGER,              -- Ligne principale erreur
    
    -- Diagnostic
    diagnostic_markdown TEXT,               -- Diagnostic formaté Markdown
    diagnostic_json TEXT,                   -- Diagnostic structuré JSON
    root_cause TEXT,                        -- Cause racine identifiée
    impact_level TEXT,                      -- low, medium, high, critical
    recommendations TEXT,                   -- JSON array de recommandations
    
    -- Bug proposal
    bug_title TEXT,                         -- Titre suggéré
    bug_description TEXT,                   -- Description suggérée (Markdown)
    bug_assignee TEXT,                      -- Assignation suggérée
    bug_priority TEXT,                      -- Priorité suggérée (1-4)
    bug_area_path TEXT,                     -- Area path ADO
    
    -- Actions
    teams_notified_at TIMESTAMP,            -- NULL si pas notifié
    bug_created_at TIMESTAMP,               -- NULL si pas créé
    bug_id TEXT,                            -- ID work item ADO créé
    bug_url TEXT,                           -- URL work item ADO
    created_by_user TEXT,                   -- User qui a créé le bug
    
    -- Feedback
    feedback TEXT,                          -- useful, not_useful, partial
    feedback_comment TEXT,
    feedback_at TIMESTAMP,
    feedback_by_user TEXT,
    
    -- Debouncing
    notification_group_id TEXT,             -- Group pour debounce
    occurrence_count INTEGER DEFAULT 1,     -- Occurrences dans groupe
    
    -- Timestamps
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    collecting_at TIMESTAMP,
    extracting_at TIMESTAMP,
    correlating_at TIMESTAMP,
    analyzing_at TIMESTAMP,
    formatting_at TIMESTAMP,
    ready_at TIMESTAMP,
    failed_at TIMESTAMP,
    
    -- Metadata
    openclaw_version TEXT,
    processing_time_ms INTEGER,             -- Temps total diagnostic
    llm_tokens_used INTEGER,
    
    -- Constraints
    UNIQUE(pipeline_id, build_id)
);

-- Index pour queries fréquentes
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_pipeline ON incidents(pipeline_id, detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_incidents_detected ON incidents(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_incidents_debounce ON incidents(pipeline_id, error_signature, detected_at);
CREATE INDEX IF NOT EXISTS idx_incidents_category ON incidents(error_category);

-- =============================================================================
-- TABLE: pipeline_history
-- Description: Historique erreurs par pipeline (pour corrélation)
-- =============================================================================
CREATE TABLE IF NOT EXISTS pipeline_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id TEXT NOT NULL,
    error_signature TEXT NOT NULL,
    error_category TEXT,
    first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    occurrence_count INTEGER DEFAULT 1,
    resolution_pattern TEXT,                -- Comment c'était résolu avant
    avg_resolution_time_min INTEGER,
    
    UNIQUE(pipeline_id, error_signature)
);

CREATE INDEX IF NOT EXISTS idx_history_pipeline ON pipeline_history(pipeline_id);
CREATE INDEX IF NOT EXISTS idx_history_signature ON pipeline_history(error_signature);

-- =============================================================================
-- TABLE: pipeline_dependencies
-- Description: Dépendances entre pipelines
-- =============================================================================
CREATE TABLE IF NOT EXISTS pipeline_dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upstream_pipeline_id TEXT NOT NULL,
    downstream_pipeline_id TEXT NOT NULL,
    dependency_type TEXT DEFAULT 'triggers', -- triggers, uses_artifact, same_repo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(upstream_pipeline_id, downstream_pipeline_id)
);

CREATE INDEX IF NOT EXISTS idx_deps_upstream ON pipeline_dependencies(upstream_pipeline_id);
CREATE INDEX IF NOT EXISTS idx_deps_downstream ON pipeline_dependencies(downstream_pipeline_id);

-- =============================================================================
-- TABLE: audit_log
-- Description: Journal d'audit des actions
-- =============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action TEXT NOT NULL,                   -- create_bug, approve, reject, feedback
    incident_id TEXT REFERENCES incidents(id),
    user_id TEXT,
    user_email TEXT,
    user_name TEXT,
    details TEXT,                           -- JSON avec détails action
    ip_address TEXT,
    user_agent TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_incident ON audit_log(incident_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(timestamp DESC);

-- =============================================================================
-- TABLE: dashboard_sessions
-- Description: Sessions utilisateurs dashboard (auth simple)
-- =============================================================================
CREATE TABLE IF NOT EXISTS dashboard_sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_email TEXT,
    user_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_expires ON dashboard_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON dashboard_sessions(user_id);

-- =============================================================================
-- TABLE: metrics
-- Description: Métriques pour monitoring
-- =============================================================================
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    labels TEXT                             -- JSON {"pipeline": "X", "category": "Y"}
);

CREATE INDEX IF NOT EXISTS idx_metrics_name_time ON metrics(metric_name, timestamp DESC);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Vue: incidents actifs (non résolus)
CREATE VIEW IF NOT EXISTS v_active_incidents AS
SELECT 
    id,
    pipeline_name,
    build_number,
    status,
    error_category,
    detected_at,
    CAST((julianday('now') - julianday(detected_at)) * 24 * 60 AS INTEGER) as age_minutes
FROM incidents
WHERE status NOT IN ('ready', 'failed') OR bug_id IS NULL
ORDER BY detected_at DESC;

-- Vue: stats par pipeline
CREATE VIEW IF NOT EXISTS v_pipeline_stats AS
SELECT 
    pipeline_id,
    pipeline_name,
    COUNT(*) as total_incidents,
    SUM(CASE WHEN bug_id IS NOT NULL THEN 1 ELSE 0 END) as bugs_created,
    AVG(processing_time_ms) as avg_processing_time_ms,
    MAX(detected_at) as last_incident_at
FROM incidents
GROUP BY pipeline_id, pipeline_name;

-- Vue: incidents récents pour dashboard
CREATE VIEW IF NOT EXISTS v_recent_incidents AS
SELECT 
    id,
    pipeline_name,
    build_number,
    build_url,
    status,
    error_category,
    root_cause,
    impact_level,
    detected_at,
    ready_at,
    bug_id,
    bug_url,
    feedback
FROM incidents
WHERE detected_at > datetime('now', '-7 days')
ORDER BY detected_at DESC
LIMIT 100;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- Trigger: update pipeline_history on new incident
CREATE TRIGGER IF NOT EXISTS trg_update_pipeline_history
AFTER INSERT ON incidents
WHEN NEW.error_signature IS NOT NULL
BEGIN
    INSERT INTO pipeline_history (pipeline_id, error_signature, error_category)
    VALUES (NEW.pipeline_id, NEW.error_signature, NEW.error_category)
    ON CONFLICT(pipeline_id, error_signature) DO UPDATE SET
        last_seen_at = CURRENT_TIMESTAMP,
        occurrence_count = occurrence_count + 1;
END;

-- Trigger: log status changes
CREATE TRIGGER IF NOT EXISTS trg_log_status_change
AFTER UPDATE OF status ON incidents
BEGIN
    UPDATE incidents SET
        collecting_at = CASE WHEN NEW.status = 'collecting' THEN CURRENT_TIMESTAMP ELSE collecting_at END,
        extracting_at = CASE WHEN NEW.status = 'extracting' THEN CURRENT_TIMESTAMP ELSE extracting_at END,
        correlating_at = CASE WHEN NEW.status = 'correlating' THEN CURRENT_TIMESTAMP ELSE correlating_at END,
        analyzing_at = CASE WHEN NEW.status = 'analyzing' THEN CURRENT_TIMESTAMP ELSE analyzing_at END,
        formatting_at = CASE WHEN NEW.status = 'formatting' THEN CURRENT_TIMESTAMP ELSE formatting_at END,
        ready_at = CASE WHEN NEW.status = 'ready' THEN CURRENT_TIMESTAMP ELSE ready_at END,
        failed_at = CASE WHEN NEW.status = 'failed' THEN CURRENT_TIMESTAMP ELSE failed_at END
    WHERE id = NEW.id;
END;

-- =============================================================================
-- SAMPLE DATA (pour tests)
-- =============================================================================

-- Uncomment pour insérer données test
/*
INSERT INTO incidents (id, pipeline_id, pipeline_name, build_id, build_number, build_url, status, error_category, error_signature, diagnostic_markdown, root_cause, impact_level)
VALUES 
    ('test-001', 'pipe-123', 'Backend-Build', 'build-456', '#1234', 'https://dev.azure.com/...', 'ready', 'compilation', 'CS0246-missing-ref', '## Diagnostic\n\nErreur de compilation...', 'Référence NuGet manquante', 'high'),
    ('test-002', 'pipe-124', 'Frontend-Build', 'build-457', '#567', 'https://dev.azure.com/...', 'analyzing', 'test', 'jest-timeout', NULL, NULL, NULL),
    ('test-003', 'pipe-123', 'Backend-Build', 'build-458', '#1235', 'https://dev.azure.com/...', 'detecting', NULL, NULL, NULL, NULL, NULL);
*/
