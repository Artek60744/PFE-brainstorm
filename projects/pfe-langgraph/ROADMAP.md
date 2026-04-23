# Roadmap Implémentation LangGraph Dashboard

**Statut global** : Phase 2 - Implémentation des composants

**Dernière mise à jour** : 2026-04-23

**Note** : OpenClaw remplacé par LangGraph + APScheduler (ADR-017, 2026-04-23)

---

## 📋 Vue d'ensemble

```
[COMPLÉTÉ] Architecture & Décisions (ADR-010 à 015)
[COMPLÉTÉ] Schémas BD (ADO + DAI)
[COMPLÉTÉ] Dashboard skeleton (FastAPI + HTMX)
[EN COURS] Intégration MCP
[À FAIRE] Pipeline diagnostique
[À FAIRE] Auth & Sécurité
[À FAIRE] Tests & Deployment
```

---

## 🎯 Priorités par Sprint

### Sprint 1: MCP Integration (Next)
**Effort** : 2-3 sessions | **Risque** : Moyen (API DAI + ADO complexes)

#### A. Digital.ai Release - Client MCP
**Fichier** : `artifacts/dashboard/dai_client.py`
- [ ] Remplacer MCP stub par vrais appels
- [ ] Implémenter : `list_releases()`, `get_release()`, `list_tasks()`
- [ ] Gérer erreurs réseau & timeouts (circuit breaker existant)
- [ ] Tests: appels réels sur environnement Isagri
- **Dépend de** : MCP server Digital.ai accessible
- **ADR** : ADR-019 (polling adaptatif)
- **ADR** : ADR-019 (polling adaptatif)

#### A. Azure DevOps - Webhook Handler
**Fichier** : `artifacts/dashboard/ado_webhook.py`
- [ ] Route FastAPI : `POST /webhook/ado`
- [ ] Parser payload ADO (build complete, release stage failure)
- [ ] Insérer incident dans BD (déduplication par build_id)
- [ ] Notifier Teams (canal `#devops-incidents`)
- [ ] Trigger LangGraph Read node
- **Dépend de** : Webhook ADO configuré en production
- **ADR** : ADR-018

#### B. Azure DevOps - Polling Fallback
**Fichier** : `artifacts/dashboard/ado_heartbeat.py`
- [ ] Polling builds (15min, adapter selon SLA)
- [ ] Polling releases via REST ADO
- [ ] Déduplication par build_id vs webhook
- [ ] Même circuit breaker que DAI
- **Dépend de** : MCP ADO server disponible
- **ADR** : ADR-018

**Tasks**:
```python
# Pseudo
1. GET /ado/builds?status=failed&recent=1h
2. GET /ado/releases?status=failed&recent=1h
3. Corréler avec incidents existants (avoid duplicates)
4. Mettre à jour statut incident
```

---

### Sprint 2: Diagnostic Pipeline (Après MCP)
**Effort** : 2 sessions | **Risque** : Élevé (logique métier complexe)
- **ADR** : ADR-020 (HTMX adaptatif pour affichage diagnostic)

#### A. Incident Analysis Engine
**Fichier** : `artifacts/dashboard/diagnostic.py`
- [ ] Implémenter `analyze_incident(incident_id)` séquentiel
- [ ] Étapes :
  1. Collecter logs ADO build
  2. Extraire erreurs (regex + patterns)
  3. Corréler avec DAI releases (V2 seulement?)
  4. Générer rapport diagnostic
  5. Formater pour Teams + Dashboard
- [ ] Stocker diagnostic en BD
- [ ] Pas de sub-agents LLM (gardé simple MVP)

#### B. Correlation Engine (V2 Future)
**Fichier** : `artifacts/dashboard/correlate.py` (skeleton)
- [ ] ADO build failure → DAI release impact mapping
- [ ] Doc : quand implémenter, conditions success
- **Status** : Placeholder only pour MVP

---

### Sprint 3: Auth & Sécurité (Parallèle)
**Effort** : 1-2 sessions | **Risque** : Critique (trust boundary)

#### A. Trust Boundary Implementation
**Fichier** : `artifacts/dashboard/trust.py`
- [ ] Dashboard n'a PAS token ADO
- [ ] Au lieu : call LangGraph StateGraph (localhost:8001) pour créer bugs
- [ ] Implémenter client LangGraph
- [ ] Validation : token + audit log
- **ADR** : ADR-012 référence

#### B. SSO Integration (Isagri)
**Fichier** : `artifacts/dashboard/auth.py`
- [ ] Remplacer placeholder SSO
- [ ] Intégration AD/LDAP Isagri
- [ ] Roles : DevOps, Support, Manager
- [ ] Restrict dashboard à rôles approuvés

#### C. Audit Logging
**Fichier** : `artifacts/dashboard/audit.py`
- [ ] Log all dashboard actions (view, create, approve)
- [ ] Schema : audit table (existant dans schema.sql)
- [ ] Compliance : qui, quoi, quand, pourquoi

---

### Sprint 4: Tests & Deployment
**Effort** : 1-2 sessions | **Risque** : Moyen

#### A. Unit Tests
**Fichier** : `tests/test_*.py`
- [ ] DAI client (mock MCP)
- [ ] ADO webhook parser
- [ ] Diagnostic engine
- [ ] Auth middleware

#### B. E2E Tests
**Fichier** : `tests/e2e_dashboard.py`
- [ ] Incident creation (webhook)
- [ ] Dashboard display
- [ ] Diagnostic generation
- [ ] Teams notification

#### C. Deployment Config
**Fichier** : `deploy/`
- [ ] Docker compose (dev + staging)
- [ ] ENV vars (ADO token, DAI URL, Teams webhook)
- [ ] DB migrations (SQLite → PostgreSQL roadmap)
- [ ] Health checks

---

## 📁 Structure des fichiers

```
artifacts/dashboard/
├── app.py                 # Main FastAPI (existant)
├── schema.sql             # ADO incidents (existant)
├── schema_dai.sql         # DAI incidents (existant)
├── templates.html         # HTMX views (existant)
│
├── dai_heartbeat.py       # DAI polling (existant + stub MCP)
├── dai_client.py          # [SPRINT 1] DAI MCP integration
│
├── ado_webhook.py         # [SPRINT 1] ADO webhook handler
├── ado_heartbeat.py       # [SPRINT 1] ADO polling fallback
│
├── diagnostic.py          # [SPRINT 2] Incident analysis engine
├── correlate.py           # [SPRINT 2] Correlation skeleton
│
├── trust.py               # [SPRINT 3] Trust boundary + OpenClaw client
├── auth.py                # [SPRINT 3] SSO + roles
├── audit.py               # [SPRINT 3] Audit logging
│
└── tests/
    ├── test_dai_client.py
    ├── test_ado_webhook.py
    ├── test_diagnostic.py
    ├── e2e_dashboard.py
    └── conftest.py        # Shared fixtures
```

---

## ⚠️ Blockers & Dépendances

| Blocker | Status | Dépend de | ETA |
|---------|--------|-----------|-----|
| MCP Digital.ai server accessible | 🔴 ? | Infra Isagri | ? |
| MCP ADO server configuré | 🔴 ? | Infra Isagri | ? |
| Webhook ADO production | 🔴 Placeholder | DevOps Isagri | ? |
| Token LangGraph valide (test) | 🔴 ? | LangGraph deploy | ? |
| SSO Isagri accessible | 🔴 Placeholder | Infra Isagri | ? |

---

## 📊 Métriques de complétion

- **Définition de fait** :
  - Code commit + review ✅
  - Tests passants ✅
  - Docs actualisées ✅
  - Incident approuvé (tuteur / PM)

- **Tracking** :
  - Sessions : logs dans `sessions/SESSION-YYYY-MM-DD.md`
  - ADRs : une par décision tech importante
  - Artifacts : versionnés, tagged par sprint

---

## 🔄 Template mise à jour après chaque session

```markdown
## Session YYYY-MM-DD

**Sprint** : [Sprint N]
**Durée estimée** : Xh

### Accompli
- [ ] Task 1
- [ ] Task 2

### Blockers rencontrés
- Issue X (impact: ..., next: ...)

### Prochaines étapes
- Task 3
- Task 4

### Décisions prises
- ADR-XXX : ...
```

---

## 📞 Points de contact

- **Architecte** : Validation design
- **DevOps** : Webhook ADO, MCP server access
- **Sécurité** : Trust boundary, SSO, audit
- **Tuteur** : Approbation MVPs avant production
