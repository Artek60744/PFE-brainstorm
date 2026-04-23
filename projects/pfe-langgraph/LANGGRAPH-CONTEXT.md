# LangGraph Context - PFE Integration

**Purpose** : Mémoire partagée pour agent LangGraph qui gère incidents DevOps via RPAE pattern.

**Last sync** : 2026-04-23

**Note** : OpenClaw remplacé par LangGraph + APScheduler (ADR-017)

---

## 🎯 Mission

Implémenter **Read-Plan-Approve-Execute** (RPAE) agent via LangGraph + MCP, pour **réduire MTTR incidents DevOps** chez Isagri.

**Hypothèse PFE** : Agent structuré peut diminuer temps analyse primaire de **50%**.

---

## 🔗 Sources

| Type | Lien | Notes |
|------|------|-------|
| Architecture | `projects/pfe-langgraph/README.md` | Vue générale + liens |
| Décisions | `projects/pfe-langgraph/decisions/ADR-*.md` | Tous les choix tech (17 ADRs) |
| Dashboard | `projects/pfe-langgraph/artifacts/dashboard/` | UI + backend MVP |
| Agents humains | `projects/pfe-langgraph/agents/` | Rôles brainstorming (6 agents) |
| Roadmap | `projects/pfe-langgraph/ROADMAP.md` | Implementation checklist |
| Sessions | `projects/pfe-langgraph/sessions/` | Logs historiques |
| Tech Stack | `projects/pfe-langgraph/artifacts/TECH-STACK.md` | Stack centralisée |
| Blockers | `projects/pfe-langgraph/BLOCKERS.md` | Questions ouvertes (Q1-Q7 résolus) |

---

## 🏗️ Architecture Générale

```
┌─────────────────────────────────────────┐
│   Azure DevOps                          │
│   (Build + Release failures)            │
└────────────┬────────────────────────────┘
             │ Webhook
             ▼
┌─────────────────────────────────────────┐
│   Dashboard (FastAPI + HTMX)            │
│   - RPAE UI (Read-Plan-Approve-Execute) │
│   - Incident list + detail              │
│   - Diagnostic display                  │
└────────────┬────────────────────────────┘
             │ (no ADO token)
             ▼
┌─────────────────────────────────────────┐
│   LangGraph StateGraph (RPAE)           │
│   - Read: Diagnostic, logs, context     │
│   - Plan: Options for resolution        │
│   - Approve: Wait for human in Teams    │
│   - Execute: Create bug, trigger fix    │
│                                         │
│   Heartbeat: APScheduler                │
│   Memory: SqliteSaver                   │
└────────────┬────────────────────────────┘
             │ MCP calls
      ┌──────┴──────┐
      ▼             ▼
  ADO APIs      DAI Release APIs
  (via MCP)     (via MCP)
```

---

## 🎬 Happy Path : Incident Response

```
1. ADO build fails
   ↓
2. Webhook → Dashboard (incident created)
   ↓
3. Dashboard displays on Teams pin
   ↓
4. DevOps opens dashboard → reviews diagnostic
   ↓
5. Clicks "Start RPAE" → LangGraph reads incident
   ↓
6. LangGraph StateGraph generates plan (options):
   - Restart build
   - Revert commit
   - Scale service
   - Manual escalation
   ↓
7. LangGraph awaits approval in Teams thread
   ↓
8. DevOps approves → LangGraph executes (create bug + notify)
   ↓
9. Dashboard updates status → incident closed/in-progress
```

---

## 🔐 Security Constraints

**Trust Boundary** (ADR-012):
- Dashboard is **untrusted** (internet-facing)
- Dashboard has **NO ADO token**
- Dashboard calls LangGraph (localhost:8001) to create bugs
- LangGraph validates + audits all actions
- Result: Centralized audit trail, no token exposure

**Auth** :
- Dashboard: SSO (Isagri AD/LDAP)
- LangGraph: Internal token (deployment secret)
- Teams: OAuth app registered

---

## 📊 Data Model

### Incidents (ADO-sourced)
```sql
incidents(
  id, 
  build_id, release_id,     -- ADO references
  status (new/in_progress/diagnostic_ready),
  severity (P1/P2/P3),
  created_at, updated_at,
  diagnostic_id (FK)
)

diagnostics(
  id,
  incident_id,
  error_msg, stack_trace, logs,
  analysis (correlations, root_cause_guess),
  created_at
)
```

### DAI Releases (polling-sourced)
```sql
dai_incidents(
  id,
  release_id,
  phase, task,
  status,
  last_polled_at,
  circuit_breaker_state
)
```

---

## 🔄 MCP Integrations

### Digital.ai Release (Polling)
- **Frequency** : 60s normal, 15s during incident, 5min off-peak
- **Operations** : list_releases, get_release, list_tasks
- **Stub location** : `artifacts/dashboard/dai_heartbeat.py`
- **Real client** : `artifacts/dashboard/dai_client.py` (TODO Sprint 1A)

### Azure DevOps (Webhook + Polling)
- **Webhook** : Build/Release complete events → Dashboard
- **Polling** : Fallback if webhook fails
- **Operations** : get_build_log, get_release_info, create_bug
- **Stub location** : `artifacts/dashboard/ado_webhook.py` (TODO Sprint 1B)

---

## ⚙️ Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Architecture | ✅ Complete | 6 ADRs documented |
| Dashboard skeleton | ✅ Complete | FastAPI + HTMX base |
| DB schema (ADO) | ✅ Complete | 7 tables + views |
| DB schema (DAI) | ✅ Complete | 5 tables + circuit breaker |
| DAI MCP stub | ✅ Complete | Needs real API calls |
| ADO webhook stub | 🟡 Partial | Routes defined, parser TODO |
| Diagnostic engine | 🔴 Not started | Logic not implemented |
| Trust boundary | 🔴 Not started | LangGraph StateGraph needed |
| Auth (SSO) | 🔴 Placeholder | Isagri LDAP not available |
| Tests | 🔴 Not started | Unit + E2E needed |

---

## 🚦 Next Sprint (1A : DAI MCP Client)

**Goal** : Replace MCP stub with real Digital.ai Release API calls

**Tasks** :
1. Implement `dai_client.py` with real MCP calls
2. Add error handling (circuit breaker already in place)
3. Test on Isagri staging environment
4. Update `dai_heartbeat.py` to use new client
5. Verify polling works 60s interval

**Blockers** :
- 🔴 MCP Digital.ai server must be accessible from dashboard
- 🔴 Authentication (token/cert) for MCP server

**Owner** : Architecte (LangGraph agent)

---

## 📋 Design Decisions to Remember

| Decision | ADR | Rationale |
|----------|-----|-----------|
| LangGraph StateGraph (not OpenClaw) | ADR-017 | StateGraph natif pour RPAE, persistance intégrée, MIT license |
| FastAPI + HTMX (not Streamlit) | ADR-010 | UI control, native APIs, simple |
| Polling with HTMX (not SSE) | ADR-011 | Stateless, firewall-friendly, robust |
| Dashboard without ADO token | ADR-012 | Trust boundary, audit centralized |
| Sequential diagnostic (no sub-agents) | ADR-013 | Simple debug, no LLM contention |
| DAI polling 60s (no webhooks) | ADR-014 | No webhook option available |
| No ADO↔DAI correlation MVP | ADR-015 | Effort vs. value, V2 feature |

---

## 📞 Communication

- **Dashboard issues** : Check `ROADMAP.md` Sprint 1-4 sections
- **Agent behavior** : See agents/*.md for role definitions
- **Tech debt** : Log in session markdown after each session
- **Blockers** : Update ROADMAP.md "Blockers & Dépendances" section

---

## 🎓 PFE Constraints

1. ✅ **Pas de sandbox** → Dry-run mode mandatory in production
2. ✅ **Validation tuteur** before any real writes
3. ✅ **Prefix `[OPENCLAW-TEST]`** on test work items
4. ✅ **Zero action without approval** (except L1 auto-approved)
5. 🎯 **Objective MTTR** : -50% primary analysis time

---

**Context file version** : 1.0 | **Framework** : RPAE + MCP | **Status** : Ready for Sprint 1A
