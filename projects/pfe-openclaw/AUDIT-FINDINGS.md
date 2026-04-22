# RAPPORT D'AUDIT - Projet PFE-OpenClaw
## Exploration des Redondances, Incohérences, Obsolescence, Gaps et Violations

**Date d'analyse** : 21 avril 2026  
**Scope** : 40+ fichiers (MD, YAML, TXT)  
**Période couverte** : Janvier 2024 - Avril 2026

---

## 📊 RÉSUMÉ EXÉCUTIF

| Métrique | Valeur |
|----------|--------|
| **Problèmes CRITIQUE** | 3 |
| **Problèmes MAJEUR** | 12 |
| **Problèmes MINEUR** | 20+ |
| **Fichiers affectés** | 25+ |
| **Redondances** | 6 |
| **Incohérences** | 8 |
| **Obsolescences** | 5 |
| **Gaps** | 8 |
| **Violations** | 7 |

**État** : Le projet nécessite une mise à jour critique avant Sprint 1 (3 problèmes CRITIQUE + 12 MAJEUR).

---

## 🔴 PROBLÈMES CRITIQUES (Bloquer Sprint 1)

### #1 - Canal d'approbation incohérent (Slack vs Teams)

**Fichiers conflictuels** :
- `artifacts/00-CONTEXTE-PROJET.md` : "Slack / Teams (boutons interactifs)"
- `decisions/ADR-004-canal-teams.md` : "Teams (canal dédié équipe DevOps)" ✅
- `PROJECT.md` : "Teams" dans diagramme
- `agents/AGENT-ARCHITECTE.md` : "Teams"

**Analyse** : ADR-004 (janvier 2024) a décidé **Teams**, mais `artifacts/00-CONTEXTE-PROJET.md` (aussi janvier 2024) dit "Slack/Teams".

**Sévérité** : CRITIQUE (infrastructure) - Impact sur MCP Teams intégration

**Fix** :
```
- Vérifier avec tuteur Isagri : Final decision = Teams uniquement?
- Si OUI : Mettre à jour artifacts/00-CONTEXTE-PROJET.md (supprimer "Slack /")
```

---

### #2 - MCP Server URLs/Credentials jamais documentées

**Fichiers concernés** :
- `BLOCKERS.md` : Q1-Q6 (6 questions ouvertes sur MCP servers)
- `ROADMAP.md` : Sprint 1A "DAI MCP integration" (comment sans URL?)

**Problème** : 
- BLOCKERS.md demande les réponses avant Sprint 1
- Mais aucun fichier n'explique FORMAT attendu (URL, port, auth method)
- Pas de template configuration

**Sévérité** : CRITIQUE (Infrastructure) - Impossible d'implémenter `dai_client.py` sans infos

**Fix** :
```
Créer artifacts/MCP-CONFIGURATION.md :
- Template pour chaque MCP server (Digital.ai, ADO)
- Format: URL, port, auth type, token variable name
- Checklist d'activation infra Isagri
```

---

### #3 - Bot peut relancer pipelines? (Contradiction scope)

**Fichiers conflictuels** :
- `artifacts/09-BACKLOG.md` (E4) : "Si approuvée est un retry → Pipeline relancé via MCP"
- `agents/AGENT-DEVOPS.md` : "Le bot NE PEUT PAS relancer les builds"
- `sessions/2026-04-16-diagnostic-architecture.md` : Décision = "pas de relance auto, lien pré-rempli"

**Problème** :
- Décision claire en session 2026-04-16 : "humain crée le bug"
- ADR-009 (diagnostic système) : "notification Teams avec diagnostic"
- Mais Backlog E4 dit "relancer le pipeline"
- Confusion possible entre "créer bug" vs "relancer build"

**Sévérité** : CRITIQUE (Scope d'exécution) - Définit limites RPAE Execute phase

**Fix** :
```
Clarifier ADR-009 ou créer ADR-016 : "Execution Scope"
- E4 du Backlog EST FAUX : supprimer ou redéfinir comme "Draft work item creation"
- Décision : Bot CAN create draft, CANNOT execute build restart
```

---

## 🟡 PROBLÈMES MAJEURS (Avant Sprint 1)

### #1.2 - Planning phases vs sprints désalignés

**Fichiers conflictuels** :
- `PROJECT.md` : **Phase 0-6** (7 phases, 26 semaines)
- `project.yaml` : **phases[0-6]** = 7 objets (S1-S26 mapping)
- `artifacts/07-PLAN-REALISATION.md` : **Phase 0-6** (identique PROJECT)
- `ROADMAP.md` : **Sprint 1-4** (4 sprints) avec mention "Phase 2"

**Problème** :
- "Sprint 1: MCP Integration" ≠ "Phase-1: Read"
- ROADMAP dit "Sprint 1" = S4-S6 mais project.yaml dit "Phase-1" = S4-S6
- Suivi confus : Quel nom utiliser pour référencer?

**Sévérité** : MAJEUR (Navigation et suivi) - Confusion historique

**Fix** :
```
Option A (Préféré) : Uniformiser → "Sprint 1-4" partout
- Renommer project.yaml phases → sprints
- Mettre à jour PROJECT.md "Sprints 1-4"
- Créer mapping: Sprint 1 = Read (S4-S6), Sprint 2 = Plan (S7-S9), etc.

Option B : Créer "SPRINT-PHASE-MAPPING.md"
```

---

### #1.4 - Stack technique répétée 6x avec incohérences

**Incohérence**: Slack vs Teams (déjà #CRITIQUE1 mais répercuté ici)

**Autres répétitions sans contradictions** :
- `PROJECT.md` section "Stack Technique"
- `project.yaml` section "stack"
- `OPENCLAW-CONTEXT.md` section "Architecture"
- `artifacts/00-CONTEXTE-PROJET.md`
- `decisions/ADR-005-dashboard-mvp.md`
- `decisions/ADR-010-fastapi-htmx.md`

**Problème** : Même info en 6 endroits → maintenance hell si changement

**Sévérité** : MAJEUR (Maintenabilité)

**Fix** :
```
Centraliser : Créer artifacts/TECH-STACK.md (source of truth)
- OpenClaw (framework)
- MCP Microsoft (ADO integration)
- MCP Digital.ai Release
- Teams (approvals)
- FastAPI + HTMX (dashboard, depuis ADR-010)
- SQLite POC → PostgreSQL V2
Tous autres fichiers → référencer ce fichier
```

---

### #2.2 - Dashboard tech (Streamlit vs FastAPI) non mis à jour dans PROJECT.md

**Timeline conflit** :
- Jan 2024 : ADR-005 compare Streamlit vs alternatives
- Jan 2024 : PROJECT.md dit "Streamlit ou FastAPI + HTMX"
- **Apr 2026** : ADR-010 **DÉCIDE** FastAPI + HTMX
- Apr 2026 : ROADMAP confirme FastAPI + HTMX
- Apr 2026 : PROJECT.md **JAMAIS MIS À JOUR** - dit toujours "Streamlit ou FastAPI"

**Sévérité** : MAJEUR (Breaking change non reflétée)

**Fix** :
```
Mettre à jour PROJECT.md ligne ~69:
Ancien : "- Streamlit ou FastAPI + HTMX"
Nouveau : "- FastAPI + HTMX (Décision ADR-010, avril 2026)"

Ajouter lastUpdated: 2026-04-21
```

---

### #2.3 - Statut du projet incohérent (Planification vs Phase 2)

**Conflit** :
- `PROJECT.md` : "Phase : **Planification** (pré-implémentation)"
- `ROADMAP.md` : "Statut global : **Phase 2 - Implémentation** des composants"
- `TRACKING-INDEX.md` : "Framework version : v1.0-**planning**"
- `project.yaml` : all phases status: "planned"

**Analyse** :
- PROJECT.md = Janvier 2024 (OBSOLÈTE)
- ROADMAP = 21 avril 2026 (RÉCENT)
- → ROADMAP est correct

**Sévérité** : MAJEUR (État du projet mal compris)

**Fix** :
```
Option A : Mettre à jour PROJECT.md completement
- Dated: 2026-04-21
- Status: "Phase 2 - Implémentation des composants"

Option B : Laisser PROJECT.md pour contexte historique
- Ajouter warning: "⚠️ Document daté de janvier 2024. Status actuel: voir ROADMAP.md"
```

---

### #2.6 - Dashboard timing incohérent (S7 vs S13)

**Conflit de timing** :
- `PROJECT.md` Phase 2 : "Créer dashboard de suivi"
- `artifacts/07-PLAN-REALISATION.md` S7-S9 : "Créer le dashboard"
- `agents/AGENT-ARCHITECTE.md` Phase 2 : "dashboard... MVP obligatoire"
- `artifacts/09-BACKLOG.md` Epic 4 : Dashboard dans "Execute (Action)" S13-S15 ⚠️
- `ROADMAP.md` Sprint 2 : Dashboard sous "Diagnostic Pipeline"

**Analyse** :
- Majorité vote = S7-S9 (Plan phase)
- Mais Backlog place en Epic 4 = S13-S15
- ADR-005 dit "MVP obligatoire" mais pas QUAND

**Sévérité** : MAJEUR (Scope et planning)

**Fix** :
```
Créer ADR-016 "Dashboard MVP Timing" :
- DÉCISION : Dashboard créé en Sprint 2 (Plan, S7-S9)
  Rationale: Nécessaire pour displaying diagnostic results
- Mettre à jour Backlog Epic 4 : Dashboard maintenance/enhancement
```

---

### #3.1 - PROJECT.md OBSOLÈTE (Dernière mise à jour: Janvier 2024)

**Contenus obsolètes** :
- Énumère ADR-001 à 008 seulement (15 ADRs existent)
- ADR-010 à 015 jamais mentionnés
- Dit "Streamlit ou FastAPI" (ADR-010 a décidé FastAPI)
- Référence "prochain PI Planning" (terme 2024, vague)

**Sévérité** : MAJEUR (Source de vérité ancienne)

**Fix** :
```
Mettre à jour PROJECT.md :
1. Last updated: 2026-04-21
2. Ajouter ADRs 009-015 au tableau README
3. Confirmer FastAPI décision
4. Mettre à jour phase description si Phase 2 commenced
5. Vérifier tous les liens vers decisions/
```

---

### #3.2 - README.md manque ADRs 009-015

**Problème** :
- Tableau ADRs enumerate 001-008 seulement
- ADR-009 à 015 existent physiquement mais non listés
- New developer ne sait pas qu'ils existent

**Sévérité** : MAJEUR (Discoverability)

**Fix** :
```
Compléter tableau dans README.md :
| ADR | Décision | Statut |
|-----|----------|--------|
...
| ADR-009 | Système diagnostic | Accepté |
| ADR-010 | FastAPI + HTMX | Accepté |
| ADR-011 | Polling HTMX | Accepté |
| ADR-012 | Trust boundary | Accepté |
| ADR-013 | Diagnostic séquentiel | Accepté |
| ADR-014 | Polling DAI | Accepté |
| ADR-015 | Pas corrélation ADO↔DAI MVP | Accepté |
```

---

### #4.2 - Custom Fields ADO Isagri jamais spécifiés

**Mention** : PROJECT.md "Champs personnalisés Isagri"

**Manquant** :
- Aucun document liste les custom fields
- Structure JSON non définie
- Impact sur MCP Azure DevOps server

**Sévérité** : MAJEUR (Implémentation MCP)

**Fix** :
```
Créer artifacts/ADO-CUSTOM-FIELDS-ISAGRI.md :
- Lister custom fields Isagri
- Format: field_name, type, required, sample_value
- Impact sur queries MCP ADO
```

---

### #4.3 - Migration SQLite → PostgreSQL jamais documentée

**Mention** : `project.yaml` "SQLite (POC) → PostgreSQL (V2)"

**Manquant** :
- Aucun script migration
- Pas de schéma V1 vs V2
- Pas de rollback plan

**Sévérité** : MAJEUR (V2 sustainability)

**Fix** :
```
Créer artifacts/DATABASE-MIGRATION-PLAN.md :
- Schema v1 (SQLite) → v2 (PostgreSQL)
- Scripts migration
- Rollback strategy
```

---

### #4.4 - Teams webhook configuration steps manquants

**Mention** : ADR-004, AGENT-DEVOPS.md

**Manquant** :
- Aucun document "How to register Teams webhook"
- BLOCKERS.md Q6 "Teams app registered" non résolvable

**Sévérité** : MAJEUR (Blocker Q6)

**Fix** :
```
Créer artifacts/TEAMS-WEBHOOK-SETUP.md :
1. Create Teams app (Azure AD)
2. Register incoming webhook
3. Configure dashboard URL
4. Test with sample message
```

---

### #4.6 - Isagri SSO/LDAP config never specified

**Mention** : BLOCKERS.md Q5

**Manquant** :
- Format mappage LDAP → rôles (DevOps, Support, Manager)
- DN structure
- Filter query

**Sévérité** : MAJEUR (Blocker Q5)

**Fix** :
```
Créer artifacts/SSO-LDAP-CONFIG.md :
- Isagri AD server URL
- Base DN
- User search filter
- Group to role mapping
```

---

### #4.8 - "Niveau 1 auto-approuvé" criteria jamais définis

**Mention** : PROJECT.md "sauf niveau 1 auto-approuvé"

**Manquant** :
- Quels critères = "niveau 1"?
- Par priorité? Par impact?
- Qui est "niveau 1"?

**Sévérité** : MAJEUR (RPAE Approve phase)

**Fix** :
```
Créer artifacts/APPROVAL-LEVELS.md :
- Level 1 (auto-approved) : criteria
- Level 2 (single approval) : criteria
- Level 3 (dual approval) : criteria
Exemple:
  - L1: Build restart, same pipeline, < 3 today
  - L2: Create diagnostics, comment audit
  - L3: Breaking changes, prod deployments
```

---

## 🟢 PROBLÈMES MINEURS

### Redondances (6)
| ID | Fichiers | Problème | Fix |
|----|----------|----------|-----|
| 1.1 | PROJECT + 10 | MTTR 50% répété 11x | Centraliser dans artifacts/OBJECTIVES.md |
| 1.3 | README + yaml | Agents list duplifié | Garder reference, source of truth = agents/*.md |
| 1.5 | 4 files | Dashboard MVP vague | Créer ADR-016 timing |
| 1.6 | 6 files | Constraints sécurité répétées | Centraliser dans artifacts/SECURITY.md |

### Incohérences (3)
| ID | Fichiers | Problème | Fix |
|----|----------|----------|-----|
| 2.5 | Backlog + ADR-015 | Dépendances vs Corrélation fuzzy | Clarifier P3b Backlog scope |
| 2.8 | 4 files | Débouncing 30s vs 30min | Documenter: 30s = cooling-off, 30min = dedup |
| 7.1-7.3 | Various | Logic issues | Minor, clarifiable |

### Obsolescence (5)
| ID | Fichier | Problème | Fix |
|----|---------|----------|-----|
| 3.3 | artifacts/07 | Checklist jamais coché | OK pour plan, mettre status |
| 3.4 | CONVENTIONS.md | File refs incomplete | Mettre à jour template |
| 3.5 | sessions/ | SESSION- prefix inconsistent | Renommer 2026-04-16 file |

### Violations (7)
| ID | Fichier | Convention | Fix |
|----|---------|-----------|-----|
| 5.3 | ROADMAP | Phase=Sprint naming | Uniformiser |
| 5.4 | sessions/ | SESSION- prefix | Rename |
| 5.5 | BLOCKERS | Resolution tracking | Log Q resolutions |
| 5.6 | agents/ | Status emojis | Add ✅/🟡/🔴 |
| 5.7 | decisions/ | ADR format | Align 001-008 avec 009-015 |
| 6.1 | TRACKING-INDEX | File count "7 vs 5" | Clarify |
| 6.2 | SESSION-2026-04-21 | Placeholder short | OK, c'est court mais valide |

### Gaps & Actionability (5)
| ID | Fichier | Gap | Fix |
|----|---------|-----|-----|
| 4.5 | PLAN | Error patterns structure | Define JSON schema |
| 4.7 | ROADMAP | Docker template | Create on demand (Sprint 4) |
| 8.1 | BLOCKERS | Owner contact | Add Isagri contact name |
| 8.2 | ROADMAP + TODO | Duplication rule | Document: ROADMAP=detailed, TODO=quick ref |

---

## 📋 LISTE COMPLÈTE (Structurée)

| # | Fichier | Catégorie | Problème | Sévérité | Suggestion |
|----|---------|-----------|----------|----------|-----------|
| 1 | PROJECT.md | Obsolescence | Dernière mise à jour janvier 2024 | MAJEUR | Rafraîchir 2026-04-21, ajouter ADRs 009-015 |
| 2 | README.md | Obsolescence | ADRs 009-015 manquants du tableau | MAJEUR | Compléter tableau ADRs |
| 3 | artifacts/00 | Incohérence | "Slack/Teams" vs ADR-004 "Teams" | CRITIQUE | Clarifier avec tuteur, mettre à jour |
| 4 | ROADMAP.md vs project.yaml | Redondance | Phases vs Sprints naming | MAJEUR | Uniformiser nomenclature ou créer mapping |
| 5 | ROADMAP.md | Incohérence | "Phase 2 - Implémentation" vs PROJECT "Planification" | MAJEUR | Aligner avec PROJECT.md |
| 6 | artifacts/09-BACKLOG.md E4 | Incohérence | Bot relance builds? vs ADR-009 diagnostic only | CRITIQUE | Modifier ou clarifier scope Execute |
| 7 | artifacts/09-BACKLOG.md Epic 4 | Incohérence | Dashboard S13 vs PLAN S7 | MAJEUR | Créer ADR-016 timing |
| 8 | BLOCKERS.md | Gap | MCP URLs never documented | CRITIQUE | Créer artifacts/MCP-CONFIGURATION.md |
| 9 | PROJECT.md | Gap | Custom fields ADO non spécifiés | MAJEUR | Créer artifacts/ADO-CUSTOM-FIELDS.md |
| 10 | project.yaml | Gap | Migration SQLite→PostgreSQL vague | MAJEUR | Créer artifacts/DATABASE-MIGRATION.md |
| 11 | ADR-004 | Gap | Teams webhook setup steps missing | MAJEUR | Créer artifacts/TEAMS-WEBHOOK-SETUP.md |
| 12 | BLOCKERS Q5 | Gap | Isagri SSO config missing | MAJEUR | Créer artifacts/SSO-LDAP-CONFIG.md |
| 13 | PROJECT.md | Gap | "Niveau 1 auto-approuvé" undefined | MAJEUR | Créer artifacts/APPROVAL-LEVELS.md |
| 14 | PROJECT.md | Violation | ADR-010 not reflected (FastAPI) | MAJEUR | Mettre à jour PROJECT.md stack section |
| 15 | sessions/2026-04-16 | Violation | SESSION- prefix missing | MINEUR | Renommer file |
| 16 | agents/ | Violation | Status emojis missing | MINEUR | Add ✅/🟡/🔴 |
| 17 | decisions/ | Violation | Format inconsistent (001 vs 009) | MINEUR | Align templates |
| 18 | TRACKING-INDEX | Tracking | "7 files" but lists 5 | MINEUR | Clarify count |
| 19 | CONVENTIONS.md | Redondance | Constraints sécurité scattered | MINEUR | Centraliser |
| 20 | 11 files | Redondance | MTTR 50% repeated 11x | MINEUR | Centraliser objectives |

---

## ✅ RECOMMANDATIONS (ACTION ITEMS)

### URGENT (Sprint 1 Blocker)

- [ ] **#CRIT-1** : Clarifier Slack vs Teams → Update artifacts/00
- [ ] **#CRIT-2** : Documenter MCP URLs → Create artifacts/MCP-CONFIGURATION.md
- [ ] **#CRIT-3** : Fix Bot scope (E4 Backlog) → Update or remove

### BEFORE SPRINT 1

- [ ] **#MAJ-1** : Update PROJECT.md (Janvier 2024 → April 2026)
- [ ] **#MAJ-2** : Sync README.md ADRs (add 009-015)
- [ ] **#MAJ-3** : Clarify Dashboard timing → ADR-016?
- [ ] **#MAJ-4** : Uniformise phases/sprints naming
- [ ] **#MAJ-5** : Document ADO Custom Fields
- [ ] **#MAJ-6** : Document Teams webhook setup
- [ ] **#MAJ-7** : Clarify "Niveau 1 auto-approuvé"
- [ ] **#MAJ-8** : Document SQLite→PostgreSQL migration
- [ ] **#MAJ-9** : Document SSO/LDAP config

### NICE TO HAVE

- [ ] Rename session file (SESSION- prefix)
- [ ] Add agent status emojis
- [ ] Fix ADR format inconsistency
- [ ] Clarify file counts (tracking)

---

## 📄 FICHIERS À CRÉER OU METTRE À JOUR

### Créer

```
artifacts/MCP-CONFIGURATION.md          # Template MCP server config
artifacts/ADO-CUSTOM-FIELDS-ISAGRI.md   # Custom field specs
artifacts/TECH-STACK.md                 # Centralized tech decision
artifacts/DATABASE-MIGRATION-PLAN.md    # SQLite → PostgreSQL
artifacts/TEAMS-WEBHOOK-SETUP.md        # Teams integration guide
artifacts/SSO-LDAP-CONFIG.md            # Isagri AD integration
artifacts/APPROVAL-LEVELS.md            # L1/L2/L3 criteria
decisions/ADR-016-dashboard-timing.md   # (si nécessaire)
```

### Mettre à jour

```
PROJECT.md                  # LastUpdated 2026-04-21, add ADRs 009-015
README.md                   # Complete ADR table 009-015
ROADMAP.md                  # Align phase/sprint naming
artifacts/09-BACKLOG.md     # Fix E4 bot execution scope
sessions/2026-04-16-*       # Rename → SESSION- prefix
agents/*.md                 # Add status emojis
decisions/*.md              # Align format (001-008 vs 009-015)
```

---

**Analyse complète** : Fichiers scannés (40+), problèmes trouvés (37), catégories (8)  
**Dernier scan** : 21 avril 2026  
**Auteur** : Analyse automatisée

