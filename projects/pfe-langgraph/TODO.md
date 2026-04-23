# TODO LangGraph Dashboard

**Quick reference** pour tasks in-flight. Détail complet → `ROADMAP.md`

**Note** : OpenClaw remplacé par LangGraph + APScheduler (ADR-017, 2026-04-23)

## Sprint 1 : MCP Integration

### A. DAI Client
**File** : `artifacts/dashboard/dai_client.py`
- [ ] Replace MCP stub with real calls
- [ ] `list_releases()`
- [ ] `get_release(id)`
- [ ] `list_tasks(release_id)`
- [ ] Error handling (circuit breaker)
- [ ] Test on Isagri staging

### B. ADO Webhook
**File** : `artifacts/dashboard/ado_webhook.py`
- [ ] FastAPI route `POST /webhook/ado`
- [ ] Parse ADO payload (build, release)
- [ ] Insert incident into DB
- [ ] Notify Teams
- [ ] Link to OpenClaw

### C. ADO Polling (Fallback)
**File** : `artifacts/dashboard/ado_heartbeat.py`
- [ ] Poll builds (15min interval)
- [ ] Poll releases
- [ ] Deduplicate vs. webhook
- [ ] Circuit breaker

---

## Sprint 2 : Diagnostic Pipeline

### A. Analysis Engine
**File** : `artifacts/dashboard/diagnostic.py`
- [ ] Sequential analysis (no sub-agents)
- [ ] Collect ADO logs
- [ ] Extract errors (regex)
- [ ] Generate report
- [ ] Store in DB

### B. Correlation (V2 skeleton)
**File** : `artifacts/dashboard/correlate.py`
- [ ] Placeholder only
- [ ] Doc when to implement

---

## Sprint 3 : Auth & Security

### A. Trust Boundary
**File** : `artifacts/dashboard/trust.py`
- [ ] Dashboard calls LangGraph (no ADO token)
- [ ] LangGraph StateGraph creates bugs
- [ ] Audit trail

### B. SSO (Isagri)
**File** : `artifacts/dashboard/auth.py`
- [ ] Replace placeholder
- [ ] AD/LDAP integration
- [ ] Roles (DevOps, Support, Manager)

### C. Audit Log
**File** : `artifacts/dashboard/audit.py`
- [ ] Log all actions
- [ ] Who, what, when, why

---

## Sprint 4 : Tests & Deploy

### A. Unit Tests
**Dir** : `tests/`
- [ ] DAI client
- [ ] ADO webhook
- [ ] Diagnostic
- [ ] Auth

### B. E2E Tests
**File** : `tests/e2e_dashboard.py`
- [ ] Webhook → Incident → Dashboard
- [ ] Teams notification
- [ ] Diagnostic generation

### C. Deployment
**Dir** : `deploy/`
- [ ] Docker compose
- [ ] ENV config
- [ ] DB migrations
- [ ] Health checks

---

## Blockers

- 🔴 MCP servers accessible? (Isagri infra)
- 🔴 ADO webhook URL? (DevOps setup)
- 🟡 LangGraph token (for trust boundary tests)

---

**Last updated** : 2026-04-21 | **Status** : Planning complete, ready for Sprint 1A
