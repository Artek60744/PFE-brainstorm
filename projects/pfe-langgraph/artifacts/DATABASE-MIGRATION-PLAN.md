# Database Migration Plan: SQLite → PostgreSQL

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: V2 Planning  
**Owner**: Architecture + DevOps team

---

## Overview

This document outlines the **migration strategy** from SQLite (MVP) to PostgreSQL (V2+), ensuring data integrity, backward compatibility, and zero downtime.

### Timeline

- **MVP (S1-S15)**: SQLite only
- **V1 Transition (S16-S20)**: PostgreSQL deployed, SQLite mirrored (fallback)
- **V2 Migration (Post-PFE)**: Full cutover to PostgreSQL

---

## Part 1: SQLite MVP Architecture

### File Location
```
projects/pfe-openclaw/artifacts/dashboard/
├── openclaw.db           # Main incident database
├── schema.sql            # ADO incidents schema
└── schema_dai.sql        # DAI releases schema
```

### Current Tables

```sql
-- ADO Incidents
CREATE TABLE incidents_ado (
  id INTEGER PRIMARY KEY,
  build_id INTEGER NOT NULL,
  pipeline_name TEXT,
  failure_reason TEXT,
  logs TEXT,
  created_at DATETIME,
  custom_fields JSON
);

-- DAI Releases
CREATE TABLE releases_dai (
  id INTEGER PRIMARY KEY,
  release_id TEXT NOT NULL,
  status TEXT,
  failing_tasks TEXT,  -- JSON
  created_at DATETIME
);

-- Audit Trail
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  action TEXT,
  work_item_id INTEGER,
  actor TEXT,
  custom_fields JSON,
  timestamp DATETIME
);
```

---

## Part 2: PostgreSQL V2 Architecture

### Connection String
```
postgresql://openclaw_user:${PG_PASSWORD}@postgres.isagri.internal:5432/openclaw_prod
```

### Enhanced Schema (V2)

```sql
-- Replace SQLite with PostgreSQL
CREATE TABLE incidents_ado (
  id SERIAL PRIMARY KEY,
  build_id INTEGER NOT NULL UNIQUE,
  pipeline_name VARCHAR(255),
  failure_reason TEXT,
  logs TEXT,  -- Consider: jsonb if structured logs
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  custom_fields JSONB,  -- PostgreSQL JSONB for better querying
  INDEX idx_build_id (build_id),
  INDEX idx_pipeline_name (pipeline_name),
  INDEX idx_created_at (created_at)
);

CREATE TABLE releases_dai (
  id SERIAL PRIMARY KEY,
  release_id VARCHAR(255) NOT NULL UNIQUE,
  status VARCHAR(50),
  failing_tasks JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_release_id (release_id),
  INDEX idx_status (status)
);

CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  action VARCHAR(100),
  work_item_id INTEGER,
  actor VARCHAR(255),
  custom_fields JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_work_item_id (work_item_id),
  INDEX idx_timestamp (timestamp),
  PARTITION BY RANGE (timestamp)  -- For scalability
);

-- Partition strategy for audit_log
CREATE TABLE audit_log_2026_q2 PARTITION OF audit_log
  FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');
```

### Advantages

- **JSONB indexes**: Faster queries on custom fields
- **Better concurrency**: Row-level locks vs SQLite table locks
- **Partitioning**: Archive old audit logs to separate tables
- **Backup/Recovery**: Point-in-time recovery, streaming replication
- **Scalability**: Handle 10x+ load increase

---

## Part 3: Migration Strategy

### Phase 1: PostgreSQL Deployment (S16-S17)

**Steps**:

1. **Infrastructure Setup**
   ```bash
   # Deploy PostgreSQL instance (managed service: Azure PostgreSQL or RDS)
   # Configure: backup, SSL, replication, monitoring
   # Create database: openclaw_prod
   # Create user: openclaw_user (read-write permissions)
   ```

2. **Schema Creation**
   ```bash
   # Run migration script
   psql -h postgres.isagri.internal -U openclaw_user -d openclaw_prod -f schema_pg.sql
   ```

3. **Connect Dashboard (Dual-Write)**
   ```python
   # Modified dashboard code (Phase 1 only)
   if os.getenv("ENABLE_POSTGRES") == "true":
       # Write to both SQLite (fallback) and PostgreSQL (primary)
       sqlite_db.write(incident)
       postgres_db.write(incident)
       
       # Read from PostgreSQL
       return postgres_db.read(incident_id)
   else:
       # MVP: SQLite only
       return sqlite_db.read(incident_id)
   ```

### Phase 2: Data Migration (S18)

**Zero-Downtime Approach**:

1. **Export SQLite → PostgreSQL**
   ```python
   import sqlite3
   import psycopg2
   
   # Connect to both
   sqlite_conn = sqlite3.connect('openclaw.db')
   pg_conn = psycopg2.connect("postgresql://...")
   
   # Migrate incidents_ado
   sqlite_cursor = sqlite_conn.cursor()
   pg_cursor = pg_conn.cursor()
   
   sqlite_cursor.execute("SELECT * FROM incidents_ado")
   for row in sqlite_cursor.fetchall():
       pg_cursor.execute(
           "INSERT INTO incidents_ado VALUES (%s, %s, ...)",
           row
       )
   pg_conn.commit()
   ```

2. **Verify Row Counts**
   ```bash
   # SQLite
   sqlite3 openclaw.db "SELECT COUNT(*) FROM incidents_ado;"
   
   # PostgreSQL
   psql -c "SELECT COUNT(*) FROM incidents_ado;"
   
   # Must match exactly
   ```

3. **Full Cutover** (S19)
   ```python
   # Disable SQLite fallback, PostgreSQL becomes primary
   ENABLE_POSTGRES = true
   SQLITE_FALLBACK = false
   ```

### Phase 3: Cleanup (S20)

- Keep SQLite as offline backup for 3 months
- Archive to cold storage (S3, GCS)
- Monitor PostgreSQL stability before deletion

---

## Part 4: Backup & Recovery Strategy

### PostgreSQL Backups

```yaml
backup_strategy:
  full_backup: "Daily at 02:00 UTC"
  incremental_backup: "Every 6 hours"
  retention: "30 days for daily, 7 years for monthly"
  
  point_in_time_recovery: "Enabled"
  replication: "Streaming replication to standby"
  
  disaster_recovery:
    rto: "15 minutes"  # Recovery Time Objective
    rpo: "5 minutes"   # Recovery Point Objective
```

### Verification Script

```sql
-- Monthly verification (add to monitoring)
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check replication lag
SELECT 
  now() - pg_last_xact_replay_time() AS replication_lag;
```

---

## Part 5: Rollback Plan

If PostgreSQL fails, fallback to SQLite:

```python
try:
    result = postgres_db.query(incident_id)
except PostgresConnectionError:
    logger.warning("PostgreSQL unavailable, falling back to SQLite")
    result = sqlite_db.query(incident_id)
    # Alert ops team
    alert_ops("PostgreSQL connection failed")
```

---

## Part 6: Cost & Resource Estimate

| Component | MVP (SQLite) | V2 (PostgreSQL) | Cost Diff |
|-----------|------------|-----------------|-----------|
| Database | Local file | Managed service | +$200-500/mo |
| Backup | Git + local | Automated + geo-replicated | +$50-100/mo |
| Monitoring | None | Included in service | Neutral |
| **Total Monthly** | ~$0 | ~$250-600 | +$250-600 |

---

## Part 7: Success Criteria

- [ ] PostgreSQL instance deployed and accessible
- [ ] SQLite → PostgreSQL data migration completed (100% match)
- [ ] Dual-write phase tested and stable (S18)
- [ ] Full cutover validated (S19)
- [ ] Recovery procedure tested and documented
- [ ] Backup automation verified
- [ ] Monitoring and alerting configured

---

## References

- [PostgreSQL Best Practices](https://www.postgresql.org/docs/)
- [Schema Design for Analytics](https://dataedo.com/blog/postgresql-json-vs-jsonb)
- [Azure PostgreSQL Documentation](https://docs.microsoft.com/en-us/azure/postgresql/)

---

**Status**: Planning phase (not started)  
**Timeline**: S16-S20 (post-MVP)  
**Owner**: DevOps + DBA  
**Next Step**: Reserve PostgreSQL instance budget before S15
