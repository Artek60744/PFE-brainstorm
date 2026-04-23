# Open Questions & Blockers

**Track des blockers + clarifications à résoudre avant implémentation.**

Last updated : 2026-04-21

---

## 🔴 Blockers Critiques (Sprint 1)

### Q1: MCP Digital.ai Release Server Accessible?
- **Status** : ❌ UNKNOWN
- **Impact** : Blocks entire Sprint 1A
- **Needed for** : `dai_client.py` implementation
- **Action** : DevOps Isagri → verify MCP server running + network access
- **Resolution** : MCP Digital.ai server URL + auth credentials (token/cert)

### Q2: MCP Azure DevOps Server Accessible?
- **Status** : ❌ UNKNOWN
- **Impact** : Blocks Sprint 1B (ADO polling fallback)
- **Needed for** : `ado_heartbeat.py` + create_bug calls
- **Action** : DevOps Isagri → verify MCP ADO server running
- **Resolution** : MCP ADO server URL + ADO PAT token

### Q3: ADO Webhook URL Configured?
- **Status** : ❌ NOT SET
- **Impact** : Sprint 1B (ADO webhook won't fire if not configured)
- **Needed for** : Real webhook events to Dashboard
- **Action** : DevOps Isagri → register webhook URL in ADO
  - Webhook URL : `https://dashboard.openclaw.isagri/webhook/ado`
  - Events : `build.complete`, `release.deployment.stage.*`
  - Retry policy : exponential backoff
- **Resolution** : Webhook successfully firing to Dashboard

---

## 🟡 Blockers Medium (Sprint 2-3)

### Q4: LangGraph Deployment URL & Token
- **Status** : ❌ UNKNOWN
- **Impact** : Blocks Sprint 3 (trust boundary implementation)
- **Needed for** : Dashboard → LangGraph StateGraph calls for bug creation
- **Action** : LangGraph owner → provide deployment details
  - URL (localhost:8001 for dev, prod URL for staging)
  - API token for auth
- **Resolution** : Trust boundary client can authenticate to LangGraph

### Q5: Isagri SSO / LDAP Available?
- **Status** : 🟡 PARTIAL (placeholder in code)
- **Impact** : Sprint 3 auth, medium priority
- **Needed for** : Dashboard authentication + role mapping
- **Action** : Infra Isagri → provide LDAP/SSO config
  - LDAP server URL
  - Base DN, user search filter
  - Group mapping (DevOps, Support, Manager)
- **Resolution** : SSO working, dashboard protected

### Q6: Teams Integration Setup
- **Status** : ❌ NOT CONFIGURED
- **Impact** : Notifications won't send (Sprint 1+)
- **Needed for** : Teams alerts + RPAE approval thread
- **Action** : Isagri → register Teams app (OAuth)
  - App ID, App Password
  - Webhook URL for notifications
- **Resolution** : Teams receiving dashboard notifications

---

## ❓ Design Clarifications

### Q7: Correlation ADO↔DAI in MVP?
- **Decision** : ADR-015 → NO, V2 feature
- **Status** : ✅ LOCKED
- **Notes** : Two separate incident views for now (ADO tab + DAI tab)

### Q8: Diagnostic Scope (Sprint 2)
- **Current** : Sequential analysis (collect logs → extract errors → format report)
- **Open** : Should OpenClaw call external services (Sentry, DataDog, etc.)?
- **Assumption** : MVP = ADO logs only, no external integrations
- **Needed** : Confirm with DevOps team

### Q9: Approval Workflow in Teams
- **Current** : Manual click in Teams thread
- **Open** : Should there be auto-approval for L1 rules?
  - E.g., "restart build if < 3 times today"
- **Needed** : Define L1 auto-approve rules with PM

### Q10: Historic Incidents Backload?
- **Current** : Dashboard starts polling from "now"
- **Open** : Should we load historic incidents from ADO?
- **Needed** : Clarify scope (last 30 days? last 100 builds?)

---

## 📋 Pre-Implementation Checklist

Before starting Sprint 1A, **must have answers to**:

- [ ] Q1: MCP DAI server accessible (URL, auth)
- [ ] Q2: MCP ADO server accessible (URL, auth)
- [ ] Q3: ADO webhook URL registered
- [ ] Q4: LangGraph deployment info
- [ ] Q5: Isagri SSO/LDAP config
- [ ] Q6: Teams app registered (ID, password, webhook)

**If not all answered** → Block Sprint 1, escalate to tuteur.

---

## Resolution Log

### ✅ Resolved

*None yet*

### 🟡 In Progress

| Question | Owner | ETA | Notes |
|----------|-------|-----|-------|
| Q1-Q6 | Isagri DevOps | ? | Waiting for infra details |

---

**Status** : 6/6 blockers open | **Sprint readiness** : 0% | **Next review** : Before Sprint 1A start
