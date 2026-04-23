# Conventions de Documentation

Règles à respecter pour maintenir cohérence et clarté du projet.

---

## 📋 Nommage des fichiers

### Tracking Files (root level)
- `ROADMAP.md` — Plan complet (4 sprints)
- `TODO.md` — Checklist rapide
- `BLOCKERS.md` — Questions ouvertes
- `LANGGRAPH-CONTEXT.md` — Mémoire agent
- `TRACKING-INDEX.md` — Index navigation
- `QUICK-START.txt` — Guide démarrage (ASCII art ok)
- `CONVENTIONS.md` — This file

### Sessions (dans `sessions/`)
- Format : `SESSION-YYYY-MM-DD.md`
- Exemple : `SESSION-2026-04-21.md`
- Contenu : Contexte, décisions, blockers, prochaines étapes

### Architecture Decision Records (dans `decisions/`)
- Format : `ADR-NNN-nom-descriptif.md`
- Numérotation : Séquentielle (ADR-010, ADR-011, ..., ADR-015)
- Exemple : `ADR-012-trust-boundary.md`

### Agents (dans `agents/`)
- Format : `AGENT-ROLE.md` (MAJUSCULES)
- Exemples : `AGENT-ARCHITECTE.md`, `AGENT-DEVOPS.md`

### Code (dans `artifacts/`)
- Python : `*.py` (snake_case)
- SQL : `schema.sql`, `schema_dai.sql`
- HTML : `templates.html`, `*.html`
- Config : `.yaml`, `.env.example`

---

## 📝 Format Markdown Standard

### Structure générale
```markdown
# Titre principal (H1)

**Statut** : [✅ Complete | 🟡 In Progress | 🔴 Blocked]

---

## Section (H2)

### Subsection (H3)

Contenu paragraphe (normal)

**Bold** pour emphasis
`code inline` pour refs

```

### Tableaux
```markdown
| Col 1 | Col 2 | Col 3 |
|-------|-------|-------|
| Data  | Data  | Data  |
```

### Listes
```markdown
- Item 1
- Item 2
  - Sous-item 2.1
  - Sous-item 2.2
```

### Checklists
```markdown
- [ ] Not done
- [x] Done
```

### Code blocks
````markdown
```python
# Python code
def hello():
    pass
```

```sql
-- SQL code
SELECT * FROM incidents;
```
````

---

## 🎯 Statuts et Symboles

| Status | Symbol | Meaning |
|--------|--------|---------|
| Complete | ✅ | Finished, tested |
| In Progress | 🟡 | Currently working |
| Blocked | 🔴 | Waiting on dependency |
| Not Started | ❌ | Not begun |
| Unknown | ❓ | Needs clarification |

### Couleurs alternatives (si pas d'emoji)
- Complete → [DONE]
- In Progress → [WIP]
- Blocked → [BLOCKED]

---

## 📊 Template Session

**Copier après chaque session** :

```markdown
## Session YYYY-MM-DD

**Sprint** : [Sprint N name]
**Durée estimée** : Xh
**Durée réelle** : Yh

### Contexte
- What we were working on
- Key decisions needed

### Accompli
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Blockers rencontrés
- Issue A (impact: ..., next: ...)
- Issue B (impact: ..., next: ...)

### Prochaines étapes
- Task X (next session)
- Task Y (next session)

### Décisions prises
- Decision 1 (creates ADR-XXX if important)
- Decision 2

### Notes
- Any learnings, gotchas, or observations
```

---

## 🔤 Conventions Langue

### Français partout (sauf technical terms)
- Commentaires code : français
- Docstrings Python : français
- Commits Git : français
- Docs markdown : français

### Terms spécialisés (anglais)
- `MCP` (Model Context Protocol)
- `RPAE` (Read-Plan-Approve-Execute)
- `DAI` (Digital.ai Release) ← ou "Digital.ai"
- `ADO` (Azure DevOps) ← ou "Azure DevOps"
- `MTTR` (Mean Time To Resolution)
- `CI/CD` (Continuous Integration/Deployment)

### Exemples corrects
```markdown
✅ "L'agent OpenClaw suit le pattern RPAE pour diagnostiquer l'incident"
✅ "DAI = Digital.ai Release (polling toutes les 60s)"
✅ "Le webhook ADO appelle /webhook/ado sur le dashboard"

❌ "L'agent OpencLaw suit le pattern rpae"
❌ "digital.ai release = DAI" (format incohérent)
❌ "l'agent ade créé le bug" (mauvaise abréviation)
```

---

## 🔗 Références Croisées

### Linking ADRs
```markdown
Voir [ADR-012](../../decisions/ADR-012-trust-boundary.md) pour rationale.
```

### Linking Sprints
```markdown
Voir [Sprint 1A](ROADMAP.md#sprint-1-mcp-integration) pour détails.
```

### Linking Sessions
```markdown
Cf. [Session 2026-04-21](sessions/SESSION-2026-04-21.md) pour contexte.
```

### Linking Code
```markdown
Implémentation dans `artifacts/dashboard/app.py:42`
```

---

## 📋 Checklist avant commit

- [ ] Orthographe/grammaire OK
- [ ] Liens corrects (pas de 404)
- [ ] Statuts à jour (✅/🟡/🔴)
- [ ] Dates YYYY-MM-DD (ISO)
- [ ] Code examples syntaxiquement corrects
- [ ] Numérotation ADRs séquentielle
- [ ] Références croisées validées

---

## 🔄 Mise à jour Workflow

### Après chaque session
```
1. Créer sessions/SESSION-YYYY-MM-DD.md
2. Mettre à jour TODO.md (cocher tasks complétées)
3. Mettre à jour BLOCKERS.md (résolutions)
4. Commit avec message: "docs(session): YYYY-MM-DD"
```

### Nouveau blocker
```
1. Ajouter à BLOCKERS.md (numéro Q, description)
2. Assigner owner + ETA
3. Commit: "docs(blockers): add Q-N question"
```

### Nouvelle décision tech
```
1. Créer decisions/ADR-NNN-nom.md
2. Référencer dans ROADMAP.md (section "Decision" ou "Why")
3. Commit: "docs(adr): ADR-NNN decision name"
```

---

**Framework version** : v1.0 | **Last updated** : 2026-04-21 | **Status** : Active
