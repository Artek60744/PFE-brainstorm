# PLAN D'EXÉCUTION - Cleanup Audit Findings

**Date création** : 2026-04-21  
**Scope** : Complet (CRITICAL + MAJOR + MINOR)  
**Durée estimée** : 9-12 heures  
**Priorité** : URGENT (blocker Sprint 1)  
**Status** : 🔴 NOT STARTED

---

## 📋 RÉSUMÉ EXÉCUTIF

Audit trouvé **37 problèmes** répartis en :
- 🔴 **3 CRITICAL** (blocker Sprint 1)
- 🟡 **12 MAJOR** (avant Sprint 1A)
- 🟢 **20+ MINOR** (nice-to-have)

**Ce plan** : Tasklists détaillées par fichier + ordre d'exécution recommandé.

**Décisions confirmées** :
- ✅ PROJECT.md → ARCHIVE (trop vieux)
- ✅ MCP-CONFIGURATION.md → Full template + schema
- ✅ ADR-016 → Create (Dashboard timing)
- ✅ Teams only (ADR-004)
- ✅ Bot = draft creation (no build restart)

---

## 🚀 PHASES D'EXÉCUTION

---

# PHASE 1 : CRITICAL FIXES (1-2h)
**Status** : 🔴 NOT STARTED  
**Blocker** : Sprint 1A cannot start without this  
**Deadline** : ASAP

## [CRIT-1] Clarify Teams (artifacts/00-CONTEXTE-PROJET.md)

**File** : `artifacts/00-CONTEXTE-PROJET.md`  
**Problem** : Says "Slack / Teams" but ADR-004 decided Teams only  
**Decision** : Assume Teams (from ADR-004-canal-teams.md)

### Tasklist

- [ ] **Read** : `artifacts/00-CONTEXTE-PROJET.md` (full file)
- [ ] **Find** : Line with "Slack / Teams (boutons interactifs)"
- [ ] **Edit** : Remove "Slack /" → Keep "Teams (boutons interactifs)"
- [ ] **Verify** : No other "Slack" mentions in file
- [ ] **Cross-check** : Verify ADR-004 says "Teams" (yes)
- [ ] **Commit** : `docs(fix): remove Slack, confirm Teams-only (ADR-004)`

### Notes
- ADR-004 (2024-01) : "Teams (canal dédié équipe DevOps)" ✅
- No other file conflicts on this

---

## [CRIT-2] Create artifacts/MCP-CONFIGURATION.md

**File** : `artifacts/MCP-CONFIGURATION.md` (NEW)  
**Purpose** : Template pour MCP servers (resolve BLOCKERS.md Q1-Q6)  
**Decision** : Full template + JSON schema

### Tasklist

- [ ] **Create** : New file `artifacts/MCP-CONFIGURATION.md`
- [ ] **Add section** : "Digital.ai Release MCP Server"
  - [ ] Server URL format
  - [ ] Authentication (token vs cert)
  - [ ] Port expected
  - [ ] Heartbeat interval
  - [ ] Sample config
- [ ] **Add section** : "Azure DevOps MCP Server"
  - [ ] Server URL format
  - [ ] PAT token location
  - [ ] ADO organization name
  - [ ] Sample config
- [ ] **Add section** : "Activation Checklist"
  - [ ] [ ] MCP server started?
  - [ ] [ ] Network accessible from dashboard?
  - [ ] [ ] Auth credentials validated?
  - [ ] [ ] Health endpoint responding?
- [ ] **Add section** : "JSON Schema Examples"
  - [ ] Response format for list_releases
  - [ ] Response format for get_build
- [ ] **Add section** : "Troubleshooting"
  - [ ] Connection timeout
  - [ ] Auth failed
  - [ ] Rate limits
- [ ] **Reference** : Link to BLOCKERS.md (Q1, Q2, Q4)
- [ ] **Commit** : `docs(mcp): create MCP-CONFIGURATION.md template`

### Template Structure

```markdown
# MCP Configuration Guide

## Digital.ai Release MCP Server

### Configuration Template
```yaml
dai_mcp_server:
  url: "https://digital-ai-mcp.isagri.local"
  port: 8443
  auth:
    type: "token"  # or "cert"
    token_var: "DAI_MCP_TOKEN"
  heartbeat:
    interval_seconds: 60
    timeout_seconds: 10
```

## Azure DevOps MCP Server

### Configuration Template
```yaml
ado_mcp_server:
  url: "https://ado-mcp.isagri.local"
  port: 8443
  auth:
    type: "pat"
    pat_var: "ADO_MCP_PAT"
    org_name: "isagri"
```

## Activation Checklist

### Before Sprint 1A

- [ ] MCP Digital.ai server running?
- [ ] MCP ADO server running?
- [ ] Network routes configured?
- [ ] Credentials in env vars?
- [ ] Health endpoints responding?

## Resolves BLOCKERS

- Q1: MCP DAI server URL + auth → **See config above**
- Q2: MCP ADO server URL + auth → **See config above**
- Q4: OpenClaw token → **See BLOCKERS.md for answer**

## JSON Schema Examples

### Digital.ai Release Response
```json
{
  "releases": [
    {
      "id": "Applications/Release123",
      "title": "Production v1.2.3",
      "status": "IN_PROGRESS",
      "phases": []
    }
  ]
}
```

### Azure DevOps Response
```json
{
  "builds": [
    {
      "id": 12345,
      "buildNumber": "20260421.1",
      "status": "completed",
      "result": "failed"
    }
  ]
}
```
```

---

## [CRIT-3] Fix E4 Backlog Scope (artifacts/09-BACKLOG.md)

**File** : `artifacts/09-BACKLOG.md`  
**Problem** : E4 says "Bot relances pipelines" but ADR-009 says "diagnostic only"  
**Decision** : Bot = draft creation only (not build restart)

### Tasklist

- [ ] **Read** : `artifacts/09-BACKLOG.md` (full Epic 4 section)
- [ ] **Find** : Line with "Si approuvée est un retry → Pipeline relancé via MCP"
- [ ] **Edit** : Change to "Bot CAN create draft work item, CANNOT restart pipeline"
- [ ] **Add note** : Reference ADR-009 (diagnostic system)
- [ ] **Verify** : Scope aligns with "read-only + draft creation" (no execution)
- [ ] **Cross-check** : ADR-009 says "notification Teams" (yes, correct)
- [ ] **Commit** : `docs(fix): clarify E4 bot scope = draft creation only`

### Expected Change

**Before** :
```
E4. Si approuvée est un retry
    → Pipeline relancé via MCP
    → Notification Teams (result)
```

**After** :
```
E4. Si approuvée est création de work item
    → Draft bug créé via OpenClaw (trust boundary)
    → Lien pré-rempli dans Teams
    → Humain crée execution (pas bot)
    
Reference: ADR-009, session 2026-04-16
```

---

# PHASE 2 : MAJOR DOCUMENT UPDATES (2-3h)
**Status** : 🔴 NOT STARTED  
**Blocker** : Before Sprint 1A  
**Can run parallel with Phase 3**

## [MAJ-1] Archive PROJECT.md (decision: DELETE)

**File** : `PROJECT.md`  
**Problem** : Outdated (January 2024, missing ADRs 009-015)  
**Decision** : Archive → delete from root, keep as backup

### Tasklist

- [ ] **Create directory** : `ARCHIVE/`
- [ ] **Copy** : `PROJECT.md` → `ARCHIVE/PROJECT-2024-01-backup.md`
- [ ] **Add header** : "⚠️ HISTORICAL DOCUMENT (archived 2026-04-21)"
- [ ] **Delete** : `PROJECT.md` from root
- [ ] **Create** : `ARCHIVED-DOCS.md` (index of archived files)
  - [ ] List what's archived and why
  - [ ] Link to active replacement (ROADMAP.md)
- [ ] **Update** : `README.md` (add note: "See ROADMAP.md for current project status")
- [ ] **Commit** : `docs(archive): move PROJECT.md to ARCHIVE/ (obsolete, use ROADMAP.md)`

### ARCHIVED-DOCS.md Content

```markdown
# Archived Documentation

## PROJECT.md (archived 2026-04-21)

**Why archived** : Outdated (January 2024)
- Missing ADRs 009-015
- Says "Streamlit or FastAPI" (ADR-010 decided FastAPI)
- Status: "Planification" (actually Phase 2 - Implementation)

**Use instead** : 
- Current status → ROADMAP.md
- Architecture → OPENCLAW-CONTEXT.md
- Full decisions → decisions/ADR-*.md

**Backup location** : ARCHIVE/PROJECT-2024-01-backup.md

---

## How to retrieve old PROJECT.md

```bash
git show HEAD~1:PROJECT.md
```
```

---

## [MAJ-2] Update README.md (add ADRs 009-015)

**File** : `README.md`  
**Problem** : ADR table only shows 001-008  
**Goal** : Complete ADR table to 015

### Tasklist

- [ ] **Read** : `README.md` (find ADR table)
- [ ] **Find** : ADR table section
- [ ] **Add rows** : ADRs 009-015
  - [ ] ADR-009: Système diagnostic
  - [ ] ADR-010: FastAPI + HTMX
  - [ ] ADR-011: Polling HTMX
  - [ ] ADR-012: Trust boundary
  - [ ] ADR-013: Diagnostic séquentiel
  - [ ] ADR-014: Polling DAI
  - [ ] ADR-015: Pas corrélation MVP
- [ ] **Verify** : All ADR files exist in decisions/
- [ ] **Commit** : `docs(readme): add ADRs 009-015 to table`

### Expected Result

```markdown
| # | Décision | Date | Statut |
|----|----------|------|--------|
| ADR-001 | Framework OpenClaw | Jan 2024 | Accepté |
| ... |
| ADR-008 | Mesure MTTR manuelle | Jan 2024 | Accepté |
| ADR-009 | Système diagnostic | Apr 2026 | Accepté |
| ADR-010 | FastAPI + HTMX | Apr 2026 | Accepté |
| ADR-011 | Polling HTMX | Apr 2026 | Accepté |
| ADR-012 | Trust boundary | Apr 2026 | Accepté |
| ADR-013 | Diagnostic séquentiel | Apr 2026 | Accepté |
| ADR-014 | Polling DAI | Apr 2026 | Accepté |
| ADR-015 | Pas corrélation MVP | Apr 2026 | Accepté |
```

---

## [MAJ-3] Update ROADMAP.md (align Phase/Sprint naming)

**File** : `ROADMAP.md`  
**Problem** : Says "Phase 2 - Implémentation" but should say "Sprint 1-4"  
**Goal** : Uniformise nomenclature

### Tasklist

- [ ] **Read** : `ROADMAP.md` (section "Statut global")
- [ ] **Find** : "Phase 2 - Implémentation"
- [ ] **Edit** : Change to "Sprint 1-4 Implementation"
- [ ] **Find** : All "Phase" references
- [ ] **Replace** : "Phase" → "Sprint" (where applicable)
- [ ] **Verify** : No confusion between "Sprint" and original "Phase 0-6" from PROJECT.md
- [ ] **Add section** : "Sprint-Phase Mapping (Historical)"
  - [ ] Sprint 1 = originally Phase 1 (Read)
  - [ ] Sprint 2 = originally Phase 2 (Plan)
  - [ ] Etc.
- [ ] **Commit** : `docs(roadmap): align Phase/Sprint naming (use Sprint 1-4)`

### Expected Change

**Before** :
```markdown
**Statut global** : Phase 2 - Implémentation des composants
```

**After** :
```markdown
**Statut global** : Sprint 1-4 Implementation (Historical: Phase 1-4)

### Sprint-Phase Mapping
- Sprint 1 (Read) = historically Phase 1 (S4-S6)
- Sprint 2 (Plan) = historically Phase 2 (S7-S9)
- Sprint 3 (Approve) = historically Phase 3 (S10-S12)
- Sprint 4 (Execute) = historically Phase 4 (S13-S15)
```

---

## [MAJ-4] Rename sessions/2026-04-16 (SESSION- prefix)

**File** : `sessions/2026-04-16-diagnostic-architecture.md`  
**Problem** : Missing SESSION- prefix (convention violation)  
**Goal** : Rename to SESSION-2026-04-16-diagnostic.md

### Tasklist

- [ ] **Check** : File exists at `sessions/2026-04-16-diagnostic-architecture.md`
- [ ] **Read** : File contents (full)
- [ ] **Create** : `sessions/SESSION-2026-04-16-diagnostic.md` with same content
- [ ] **Delete** : Old file `2026-04-16-diagnostic-architecture.md`
- [ ] **Verify** : Both SESSION files now follow SESSION- prefix
- [ ] **Commit** : `docs(sessions): rename to SESSION- prefix convention`

### Expected Structure

```
sessions/
├── SESSION-2026-04-16-diagnostic.md       (renamed)
├── SESSION-2026-04-21.md                  (existing)
└── SESSION-*.md                           (future)
```

---

## [MAJ-5] Create artifacts/TECH-STACK.md (centralize)

**File** : `artifacts/TECH-STACK.md` (NEW)  
**Purpose** : Single source of truth for tech stack  
**Goal** : Reduce duplication (appears in 6 files)

### Tasklist

- [ ] **Create** : `artifacts/TECH-STACK.md`
- [ ] **Add section** : "Core Framework"
  - [ ] OpenClaw (agent framework)
  - [ ] MCP (Model Context Protocol)
- [ ] **Add section** : "Integration Platforms"
  - [ ] Azure DevOps (via MCP)
  - [ ] Digital.ai Release (via MCP)
  - [ ] Microsoft Teams (webhooks + approvals)
- [ ] **Add section** : "Dashboard"
  - [ ] FastAPI (backend)
  - [ ] HTMX (frontend)
  - [ ] SQLite (POC) → PostgreSQL (V2)
- [ ] **Add section** : "Decision History"
  - [ ] ADR-010 : FastAPI + HTMX chosen
  - [ ] ADR-014 : Polling strategy for DAI
  - [ ] ADR-012 : Trust boundary (no ADO tokens)
- [ ] **Add section** : "Constraints"
  - [ ] No sandbox (dry-run only)
  - [ ] Zero execution without approval
- [ ] **Reference this file from** :
  - [ ] PROJECT.md → "See artifacts/TECH-STACK.md"
  - [ ] project.yaml → "See artifacts/TECH-STACK.md"
  - [ ] OPENCLAW-CONTEXT.md → Link to this
  - [ ] README.md → Link to this
- [ ] **Commit** : `docs(tech): create TECH-STACK.md as source of truth`

---

# PHASE 3 : NEW DOCUMENTATION (3-4h)
**Status** : 🔴 NOT STARTED  
**Can run parallel with Phase 1-2**

## [DOC-1] Create artifacts/ADO-CUSTOM-FIELDS-ISAGRI.md

**File** : `artifacts/ADO-CUSTOM-FIELDS-ISAGRI.md` (NEW)  
**Purpose** : Document Isagri custom fields for MCP ADO integration  
**Gap** : Never specified, blocking MCP ADO client implementation

### Tasklist

- [ ] **Research** : Ask DevOps Isagri for custom fields list
- [ ] **Create** : `artifacts/ADO-CUSTOM-FIELDS-ISAGRI.md`
- [ ] **Add section** : "Custom Fields Registry"
  - [ ] Field name, type, required, sample value
  - [ ] Format example (JSON schema)
- [ ] **Add section** : "MCP Impact"
  - [ ] How custom fields affect MCP queries
  - [ ] Sample query with custom fields
- [ ] **Add section** : "Implementation Checklist"
  - [ ] [ ] Custom fields confirmed by DevOps
  - [ ] [ ] Schema validated
  - [ ] [ ] MCP client updated
- [ ] **Note** : Mark as "PLACEHOLDER - waiting Isagri input"
- [ ] **Commit** : `docs(ado): add custom fields template (placeholder)`

### Template Structure

```markdown
# ADO Custom Fields - Isagri

## Custom Fields Registry

| Field Name | Type | Required | Sample | Notes |
|------------|------|----------|--------|-------|
| `environment` | string | Yes | prod, staging | Deployment target |
| `affected_systems` | array | No | [sys1, sys2] | Impacted services |
| `root_cause` | text | No | API timeout | Investigation notes |

## MCP Query Impact

```python
# Query with custom fields
query = """
    SELECT [System.Id], [Custom.Environment], [Custom.RootCause]
    FROM WorkItems
    WHERE [System.State] = 'Failed'
"""
```

## Status

- [ ] Custom fields confirmed by DevOps
- [ ] Schema validated
- [ ] MCP client updated

**Waiting on** : Isagri DevOps team
**BLOCKERS.md ref** : Implement after Q1-Q2 resolved
```

---

## [DOC-2] Create artifacts/DATABASE-MIGRATION-PLAN.md

**File** : `artifacts/DATABASE-MIGRATION-PLAN.md` (NEW)  
**Purpose** : SQLite (POC) → PostgreSQL (V2) migration strategy  
**Gap** : Never documented, blocking V2 roadmap

### Tasklist

- [ ] **Create** : `artifacts/DATABASE-MIGRATION-PLAN.md`
- [ ] **Add section** : "Schema Changes (v1 → v2)"
  - [ ] Compare schema.sql (SQLite) vs future schema.sql (PostgreSQL)
  - [ ] Identify breaking changes
- [ ] **Add section** : "Migration Strategy"
  - [ ] Backup strategy
  - [ ] Data transformation rules
  - [ ] Downtime estimate
- [ ] **Add section** : "Migration Scripts"
  - [ ] SQL export script
  - [ ] PostgreSQL import script
  - [ ] Data validation script
- [ ] **Add section** : "Rollback Plan"
  - [ ] How to revert if migration fails
  - [ ] Time estimate
- [ ] **Add section** : "Testing Checklist"
  - [ ] [ ] Data integrity validated
  - [ ] [ ] Queries performance tested
  - [ ] [ ] Rollback tested
- [ ] **Note** : Mark as "FUTURE (V2 roadmap)"
- [ ] **Commit** : `docs(db): create migration plan (SQLite → PostgreSQL)`

### Template Structure

```markdown
# Database Migration Plan

## Schema Changes

### v1 (SQLite) → v2 (PostgreSQL)

| Table | Change | Migration |
|-------|--------|-----------|
| incidents | Add `correlation_id` | ALTER TABLE |
| diagnostic | Add `source_system` | ALTER TABLE |
| audit | Rename `timestamp` → `created_at` | UPDATE |

## Migration Steps

1. Backup SQLite database
2. Export data from SQLite
3. Create PostgreSQL schema
4. Import data (with transformations)
5. Validate data integrity
6. Cutover
7. Monitor

## Rollback

If migration fails:
```bash
# Within 1 hour: restore from backup
```

## Timeline

- Sprint 3: Testing on staging
- Sprint 4: Production migration (planned downtime: 30min)
```

---

## [DOC-3] Create artifacts/TEAMS-WEBHOOK-SETUP.md

**File** : `artifacts/TEAMS-WEBHOOK-SETUP.md` (NEW)  
**Purpose** : Step-by-step Teams webhook registration  
**Gap** : ADR-004 mentions it, but no setup guide (BLOCKERS Q6)

### Tasklist

- [ ] **Create** : `artifacts/TEAMS-WEBHOOK-SETUP.md`
- [ ] **Add section** : "Prerequisites"
  - [ ] Azure AD account
  - [ ] Teams admin access
  - [ ] Dashboard URL
- [ ] **Add section** : "Step 1: Create Azure AD App"
  - [ ] Azure portal link
  - [ ] Permissions required
  - [ ] Screenshot example
- [ ] **Add section** : "Step 2: Create Incoming Webhook"
  - [ ] Teams channel selection
  - [ ] Webhook URL generation
  - [ ] Webhook secret
- [ ] **Add section** : "Step 3: Configure Dashboard"
  - [ ] Webhook URL in env var
  - [ ] Secret in env var
  - [ ] Test notification
- [ ] **Add section** : "Step 4: Test"
  - [ ] Sample payload
  - [ ] Expected response
  - [ ] Troubleshooting
- [ ] **Add section** : "Troubleshooting"
  - [ ] "Webhook not firing" →
  - [ ] "Permission denied" →
- [ ] **Commit** : `docs(teams): add webhook setup guide`

### Template Structure

```markdown
# Teams Webhook Setup Guide

## Prerequisites

- Azure AD account with Teams admin privileges
- Dashboard URL (e.g., https://dashboard.openclaw.isagri/)
- (BLOCKERS.md Q6 : Waiting for setup confirmation)

## Step 1: Create Azure AD App

1. Go to https://portal.azure.com
2. Select "Azure Active Directory" → "App registrations"
3. Click "New registration"
4. Fill in:
   - Name: "OpenClaw Dashboard"
   - Supported account types: "Accounts in this organizational directory"
5. Click "Register"

## Step 2: Create Incoming Webhook

1. Go to Microsoft Teams
2. Select channel: #devops-incidents
3. Click "..." (options) → "Connectors"
4. Search for "Incoming Webhook"
5. Click "Configure"
6. Name: "OpenClaw Incidents"
7. Click "Create"
8. Copy webhook URL → save in `TEAMS_WEBHOOK_URL` env var

## Step 3: Configure Dashboard

```bash
# In .env or environment
TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/webhookb2/..."
TEAMS_WEBHOOK_SECRET="your-secret"
```

## Step 4: Test

```bash
curl -X POST $TEAMS_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test message from OpenClaw"
  }'
```

Expected response: `1`

## Troubleshooting

### Webhook not firing
- [ ] URL is correct?
- [ ] Network firewall allows outbound to webhook.office.com?
- [ ] Secret is correct?

### Permission denied
- [ ] User has Teams admin role?
- [ ] Channel exists?
```

---

## [DOC-4] Create artifacts/SSO-LDAP-CONFIG.md

**File** : `artifacts/SSO-LDAP-CONFIG.md` (NEW)  
**Purpose** : Isagri AD/LDAP integration template  
**Gap** : BLOCKERS Q5, never specified

### Tasklist

- [ ] **Research** : Ask DevOps Isagri for LDAP details
- [ ] **Create** : `artifacts/SSO-LDAP-CONFIG.md`
- [ ] **Add section** : "LDAP Server Configuration"
  - [ ] Server URL
  - [ ] Base DN
  - [ ] Bind account
- [ ] **Add section** : "User Search Filter"
  - [ ] Filter template
  - [ ] Examples
- [ ] **Add section** : "Group to Role Mapping"
  - [ ] DevOps group → role mapping
  - [ ] Support group → role mapping
  - [ ] Manager group → role mapping
- [ ] **Add section** : "Dashboard Configuration"
  - [ ] Flask-LDAP example
  - [ ] ENV vars needed
- [ ] **Add section** : "Testing Checklist"
  - [ ] [ ] Connection works?
  - [ ] [ ] User search works?
  - [ ] [ ] Groups resolved?
- [ ] **Note** : Mark as "PLACEHOLDER - waiting Isagri input"
- [ ] **Commit** : `docs(auth): add SSO/LDAP config template`

### Template Structure

```markdown
# Isagri SSO/LDAP Configuration

## LDAP Server Details

```yaml
ldap:
  server: "ldap.isagri.local"
  port: 389
  base_dn: "dc=isagri,dc=local"
  bind_dn: "cn=openclaw,ou=services,dc=isagri,dc=local"
  bind_password_var: "LDAP_BIND_PASSWORD"
```

## User Search Filter

```
(&(objectClass=person)(uid={username}))
```

## Group to Role Mapping

| LDAP Group | Dashboard Role | Permissions |
|------------|----------------|-------------|
| devops | DevOps | Create/approve incidents |
| support | Support | View incidents |
| managers | Manager | Escalate to management |

## Dashboard Configuration

```python
# In Flask app
from flask_ldap3_login import LDAP3LoginManager

ldap_manager = LDAP3LoginManager(app)
app.config['LDAP_HOST'] = os.getenv('LDAP_SERVER')
app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN')
```

## Status

- [ ] LDAP server confirmed by DevOps
- [ ] Groups confirmed
- [ ] Dashboard updated

**Waiting on** : Isagri DevOps team
```

---

## [DOC-5] Create artifacts/APPROVAL-LEVELS.md

**File** : `artifacts/APPROVAL-LEVELS.md` (NEW)  
**Purpose** : Define L1/L2/L3 auto-approval criteria  
**Gap** : PROJECT.md says "L1 auto-approved" but never defined

### Tasklist

- [ ] **Create** : `artifacts/APPROVAL-LEVELS.md`
- [ ] **Add section** : "Level 1 - Auto-approved"
  - [ ] Criteria examples
  - [ ] By incident type
  - [ ] By impact
- [ ] **Add section** : "Level 2 - Single Approval"
  - [ ] Criteria examples
  - [ ] Who can approve
  - [ ] Response time SLA
- [ ] **Add section** : "Level 3 - Dual Approval"
  - [ ] Criteria examples
  - [ ] Who must approve
  - [ ] Response time SLA
- [ ] **Add section** : "Decision Matrix"
  - [ ] Table: Incident type × Severity → Level
- [ ] **Add section** : "Implementation"
  - [ ] Dashboard code impact
  - [ ] Teams notification impact
- [ ] **Commit** : `docs(approval): define L1/L2/L3 approval levels`

### Template Structure

```markdown
# Approval Levels

## Level 1 - Auto-approved (No human needed)

### Criteria

- Incident type: Build restart
- Same pipeline as last 3 days
- Count today < 3 restarts
- No critical impact services

### Example

"Build restart pipeline-ci on main (4th restart, stopped)"
→ Auto-approved by OpenClaw

## Level 2 - Single Approval

### Criteria

- Incident type: Create diagnostic comment
- Unknown root cause
- Medium impact
- Response needed < 30min

### Example

"Investigate API timeout (unknown root cause)"
→ Requires: 1 DevOps approval
→ Notification: Teams channel

## Level 3 - Dual Approval

### Criteria

- Incident type: Production deployment
- High/critical impact
- Breaking changes
- Requires: 2 approvals (DevOps + Manager)

### Example

"Deploy production hotfix (breaking change)"
→ Requires: 1 DevOps + 1 Manager
→ Notification: #escalations channel

## Decision Matrix

| Incident Type | P1 | P2 | P3 |
|---------------|----|----|-----|
| Build restart | L1 | L1 | L1 |
| API timeout | L2 | L2 | L1 |
| Prod deployment | L3 | L2 | L1 |
| Config change | L3 | L3 | L2 |
```

---

## [DOC-6] Create decisions/ADR-016-dashboard-timing.md

**File** : `decisions/ADR-016-dashboard-timing.md` (NEW)  
**Purpose** : Officially decide Dashboard MVP timing (resolve confusion S7 vs S13)  
**Decision** : Dashboard S7-S9 (Sprint 2, Plan phase)

### Tasklist

- [ ] **Create** : `decisions/ADR-016-dashboard-timing.md`
- [ ] **Add section** : "Status"
  - [ ] Status: "Accepted"
  - [ ] Date: 2026-04-21
  - [ ] Author: OpenClaw team
- [ ] **Add section** : "Context"
  - [ ] Confusion between S7 vs S13 timings
  - [ ] PLAN vs EXECUTE phase questions
  - [ ] Dashboard MVP requirement
- [ ] **Add section** : "Decision"
  - [ ] Dashboard MVP created in Sprint 2 (S7-S9)
  - [ ] Part of "Plan" phase (not Execute)
- [ ] **Add section** : "Rationale"
  - [ ] Needed to display diagnostic results
  - [ ] MVP scope: Read + list incidents + display diagnosis
  - [ ] Approval UI added in Sprint 3 (Approve phase)
  - [ ] Execution UI added in Sprint 4 (Execute phase)
- [ ] **Add section** : "Consequences"
  - [ ] Dashboard development starts earlier (S7)
  - [ ] Parallel with diagnostic engine
  - [ ] HTMX polling framework in place by S9
- [ ] **Add section** : "Alternatives Considered"
  - [ ] S13 (Execute phase) → Too late, diagnostic data nowhere to display
  - [ ] Streamlit POC → Rejected per ADR-010
- [ ] **Update** : README.md (add ADR-016 row)
- [ ] **Update** : ROADMAP.md (reference ADR-016 in Sprint 2 section)
- [ ] **Commit** : `docs(adr): ADR-016 dashboard MVP timing (S7-S9, Sprint 2)`

### Template Structure

```markdown
# ADR-016: Dashboard MVP Timing

**Status** : Accepted  
**Date** : 2026-04-21  
**Author** : OpenClaw team

## Context

Confusion about when Dashboard MVP should be built:

- PLAN says: S7-S9 (Sprint 2, Plan phase)
- BACKLOG says: S13-S15 (Sprint 4, Execute phase)
- **Question** : Which is correct?

**Analysis** :
- Dashboard is needed to DISPLAY diagnostic results
- If built in S13, diagnostic (S10-S12) has nowhere to display
- ADR-005 says "MVP obligatoire" but doesn't specify WHEN

## Decision

**Dashboard MVP created in Sprint 2 (S7-S9)**

Sprint 2 = "Plan" phase. Dashboard MVP includes:
- Incident list view
- Incident detail view
- Display diagnostic results
- No approval UI yet (added Sprint 3)

## Rationale

1. **Dependency** : Diagnostics need display (S10+ blocked if no UI)
2. **MVP scope** : Read-only display of diagnostic, not action-taking
3. **Phasing** :
   - Sprint 2: Display diagnostics (Plan phase)
   - Sprint 3: Approval UI (Approve phase)
   - Sprint 4: Execute buttons (Execute phase)

## Consequences

- Dashboard development starts S7 (Sprint 2)
- Parallel with diagnostic engine development
- HTMX polling infrastructure in place by S9

## Alternatives

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| S7 (Sprint 2) | Displays diagnostics | Dev effort | **CHOSEN** |
| S13 (Sprint 4) | Later timing | Nowhere to display results | Rejected |

## References

- ADR-010: FastAPI + HTMX choice (board tech)
- ADR-009: Diagnostic system design
- ROADMAP.md: Sprint 2 section

---

**Next step** : Start Dashboard MVP development in Sprint 2A
```

---

# PHASE 4 : BACKLOG + AGENTS REFINEMENT (1h)
**Status** : 🔴 NOT STARTED  
**Before Sprint 1A**

## [REF-1] Update artifacts/09-BACKLOG.md

**File** : `artifacts/09-BACKLOG.md`  
**Changes** :
1. Fix E4 scope (already done in PHASE 1 CRIT-3)
2. Clarify P3b (dependencies vs correlation)

### Tasklist

- [ ] **Find** : P3b section in Backlog
- [ ] **Find** : "Dépendances vs Corrélation ADO↔DAI" confusion
- [ ] **Edit** : Clarify
  - [ ] Dependencies = task blocking (within DAI)
  - [ ] Correlation = ADO build → DAI release impact (across systems)
  - [ ] MVP: Dependencies only
  - [ ] V2: Correlation feature
- [ ] **Add note** : Reference ADR-015 (no correlation MVP)
- [ ] **Commit** : `docs(backlog): clarify dependencies vs correlation (V2)`

---

## [REF-2] Update agents/*.md (add status emojis)

**Files** : 
- `agents/AGENT-ARCHITECTE.md`
- `agents/AGENT-DEVOPS.md`
- `agents/AGENT-SECURITE.md`
- `agents/AGENT-PRODUIT.md`
- `agents/AGENT-CRITIQUE.md`

### Tasklist

- [ ] **For each agent file** :
  - [ ] Add header with status : e.g., "**Status** : ✅ Active (v1.0)"
  - [ ] Add last update date
  - [ ] Verify role is still accurate
  - [ ] Fix any typos or outdated sections

Example:

```markdown
# AGENT-ARCHITECTE

**Status** : ✅ Active (v1.0)  
**Last Updated** : 2026-04-21  
**Role** : Architecture design + tech decisions

## Responsibilities
...
```

- [ ] **Commit** : `docs(agents): add status + version headers`

---

# PHASE 5 : MINOR HARMONIZATION (1h)
**Status** : 🔴 NOT STARTED  
**Nice-to-have**

## [MIN-1] Align decisions/ format (ADR-001-008 vs 009-015)

**Files** : All ADR files  
**Goal** : Consistent template across all 15 ADRs

### Tasklist

- [ ] **Read** : Sample from ADR-001-008 (template)
- [ ] **Read** : Sample from ADR-009-015 (new template)
- [ ] **Compare** : Find format differences
- [ ] **For each ADR-001-008** :
  - [ ] Check if missing: Context, Decision, Rationale, Consequences
  - [ ] Add missing sections if needed
  - [ ] Use consistent status symbols
- [ ] **For each ADR-009-015** :
  - [ ] Verify all sections present
  - [ ] Consistent status format
- [ ] **Create** : `decisions/ADR-TEMPLATE.md` (standard template)
- [ ] **Commit** : `docs(adr): align format across all ADRs`

### Standard Template

```markdown
# ADR-NNN: Decision Title

**Status** : [Accepted | Proposed | Superseded]  
**Date** : YYYY-MM-DD  
**Author** : [Name/Team]

## Context

[Problem statement]

## Decision

[What was decided]

## Rationale

[Why this decision]

## Consequences

[Impact of decision]

## Alternatives

| Option | Pros | Cons |
|--------|------|------|
| ... | ... | ... |

## References

- [Related ADRs]
- [Related files]
```

---

## [MIN-2] Update CONVENTIONS.md (fix file references)

**File** : `CONVENTIONS.md`  
**Goal** : Complete file references, fix any incomplete sections

### Tasklist

- [ ] **Read** : `CONVENTIONS.md` (full)
- [ ] **Find** : Incomplete template sections
- [ ] **Complete** : Session template example
- [ ] **Complete** : ADR template example
- [ ] **Add section** : "File size guidelines"
  - [ ] ROADMAP.md : ~6-8 KB
  - [ ] TODO.md : ~2-3 KB
  - [ ] ADRs : ~2-4 KB each
- [ ] **Add section** : "Link checking"
  - [ ] How to validate broken links
  - [ ] Tool recommendation
- [ ] **Commit** : `docs(conventions): complete file references + guidelines`

---

## [MIN-3] Fix TRACKING-INDEX.md (file count)

**File** : `TRACKING-INDEX.md`  
**Goal** : Correct "7 files" vs "5 files" confusion

### Tasklist

- [ ] **Read** : `TRACKING-INDEX.md` (statistics section)
- [ ] **Count** : Actually count tracking files
  - [ ] QUICK-START.txt
  - [ ] ROADMAP.md
  - [ ] TODO.md
  - [ ] BLOCKERS.md
  - [ ] OPENCLAW-CONTEXT.md
  - [ ] TRACKING-INDEX.md
  - [ ] CONVENTIONS.md
  - Total: 7 main + 1 session
- [ ] **Update** : Statistics table
- [ ] **Clarify** : "7 tracking files + new session files"
- [ ] **Commit** : `docs(tracking): fix file count (7 + sessions)`

---

# PHASE 6 : VALIDATION + COMMIT (1h)
**Status** : 🔴 NOT STARTED  
**At end of cleanup**

## [VAL-1] Cross-check all links

### Tasklist

- [ ] **Create** : Simple link checker script
- [ ] **Run** : Check all .md files for broken links
- [ ] **Fix** : Any broken references
- [ ] **Verify** : All ADR links work
- [ ] **Verify** : All file references valid
- [ ] **Test** : Navigation from index files (README, TRACKING-INDEX, QUICK-START)

---

## [VAL-2] Verify ADR consistency

### Tasklist

- [ ] **Check** : All 15 ADRs have consistent format
- [ ] **Check** : All ADRs numbered sequentially (001-015)
- [ ] **Check** : README.md lists all 15
- [ ] **Check** : No duplicates
- [ ] **Verify** : References between ADRs accurate

---

## [VAL-3] Verify file references

### Tasklist

- [ ] **Check** : ROADMAP.md references correct files
- [ ] **Check** : BLOCKERS.md references correct ADRs
- [ ] **Check** : OPENCLAW-CONTEXT.md references correct decisions
- [ ] **Check** : All new files created in correct directories
- [ ] **Verify** : ARCHIVE/ directory exists
- [ ] **Verify** : PROJECT.md archived

---

## [VAL-4] Cleanup and organize commits

### Tasklist

- [ ] **Review** : All commits made (should be ~12-15 commits)
- [ ] **Organize** : Group by theme if needed
- [ ] **Write** : Clear commit messages
- [ ] **Tag** : Completion tag (e.g., `v1.0-audit-cleanup`)

**Commit messages should follow** :
```
docs(PHASE): description

- Bullet point 1
- Bullet point 2

References: AUDIT-FINDINGS.md #CRIT-1, etc.
```

---

## [VAL-5] Create CLEANUP-SUMMARY.md

**File** : `CLEANUP-SUMMARY.md` (NEW)  
**Purpose** : Final summary of what was done

### Tasklist

- [ ] **Create** : `CLEANUP-SUMMARY.md`
- [ ] **Add section** : "What was fixed"
  - [ ] 3 CRITICAL issues
  - [ ] 12 MAJOR issues
  - [ ] 20+ MINOR issues
- [ ] **Add section** : "Files created"
  - [ ] List all 8 new files
- [ ] **Add section** : "Files updated"
  - [ ] List all updated files
- [ ] **Add section** : "Files archived"
  - [ ] PROJECT.md
- [ ] **Add section** : "Metrics"
  - [ ] Time spent
  - [ ] Commits made
  - [ ] Files touched
- [ ] **Commit** : `docs(cleanup): final summary of audit fixes`

---

# 📈 EXECUTION TIMELINE

## Day 1 - Morning (2-3h)

- [ ] **PHASE 1** : CRITICAL fixes (1-2h)
  - [ ] [CRIT-1] Remove Slack from 00-CONTEXTE
  - [ ] [CRIT-2] Create MCP-CONFIGURATION.md
  - [ ] [CRIT-3] Fix E4 bot scope

- [ ] **Start PHASE 3** : New documentation (parallel)
  - [ ] [DOC-1] ADO custom fields template
  - [ ] [DOC-2] Database migration plan

## Day 1 - Afternoon (3-4h)

- [ ] **PHASE 2** : Major document updates (2-3h)
  - [ ] [MAJ-1] Archive PROJECT.md
  - [ ] [MAJ-2] Update README.md (add ADRs)
  - [ ] [MAJ-3] Sync ROADMAP.md naming
  - [ ] [MAJ-4] Rename sessions/2026-04-16

- [ ] **Continue PHASE 3** :
  - [ ] [DOC-3] Teams webhook setup
  - [ ] [DOC-4] SSO/LDAP config
  - [ ] [DOC-5] Approval levels
  - [ ] [DOC-6] ADR-016 dashboard timing

## Day 2 - Morning (2-3h)

- [ ] **PHASE 4** : Backlog refinement (1h)
  - [ ] [REF-1] Fix backlog E4 + P3b
  - [ ] [REF-2] Add agent status emojis

- [ ] **PHASE 5** : Harmonization (1h)
  - [ ] [MIN-1] ADR format consistency
  - [ ] [MIN-2] CONVENTIONS.md updates
  - [ ] [MIN-3] Fix TRACKING-INDEX count

## Day 2 - Afternoon (1-2h)

- [ ] **PHASE 6** : Validation (1h)
  - [ ] [VAL-1] Cross-check links
  - [ ] [VAL-2] ADR consistency
  - [ ] [VAL-3] File references
  - [ ] [VAL-4] Organize commits
  - [ ] [VAL-5] Create CLEANUP-SUMMARY

---

# 🎯 SUCCESS CRITERIA

- [ ] All 37 audit findings addressed
- [ ] No broken links in any .md file
- [ ] All 15 ADRs listed in README.md
- [ ] ROADMAP.md uses consistent "Sprint 1-4" naming
- [ ] All critical issues (CRIT-1, 2, 3) fixed
- [ ] 8 new documentation files created
- [ ] PROJECT.md archived (not deleted)
- [ ] All commits well-documented
- [ ] CLEANUP-SUMMARY.md written

---

# 📝 NOTES

- Each task should be verified before marking ✅
- Commit after each "chunk" (don't batch too many changes)
- Use conventional commit format
- Reference AUDIT-FINDINGS.md in commit messages when applicable
- Ask for clarification if any task is ambiguous

---

**Plan created** : 2026-04-21  
**Status** : Ready for execution  
**Estimated duration** : 9-12 hours  
**Priority** : URGENT (blocker Sprint 1A)

**Next step** : Start PHASE 1 when ready
