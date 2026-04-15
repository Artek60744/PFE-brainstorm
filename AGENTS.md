# AGENTS.md — Guide pour Agents IA

## Vue d'ensemble

Ce dépôt est un **framework de brainstorming IA modulaire** qui sépare :
- **Le moteur** (`core/`) : Workflows, règles et templates réutilisables
- **Les projets** (`projects/`) : Contexte, agents et résultats spécifiques à chaque brainstorm

---

## Structure du Dépôt

```
brainstorming/
├── core/                          # Moteur du framework (réutilisable)
│   ├── workflows/                 # Workflows de débat
│   ├── rules/                     # Règles de comportement
│   ├── templates/                 # Templates d'agents génériques
│   └── project-template/          # Template pour nouveau projet
└── projects/                      # Projets de brainstorming
    └── pfe-openclaw/              # Projet PFE actif
        ├── project.yaml           # Configuration technique
        ├── PROJECT.md             # Description narrative
        ├── agents/                # Agents spécialisés
        ├── artifacts/             # Livrables du brainstorming
        ├── decisions/             # ADR (Architecture Decision Records)
        └── sessions/              # Synthèses des sessions
```

---

## Projet Actif : PFE OpenClaw

### Contexte
PFE visant à évaluer si un agent IA avec le pattern **Read-Plan-Approve-Execute (RPAE)** peut réduire le MTTR des incidents DevOps.

- **Entreprise** : Isagri | **Établissement** : UniLaSalle (programme RIOC)
- **Stack** : OpenClaw + MCP + Azure DevOps + Digital.ai Release + Teams
- **Phase** : Planification (pré-implémentation)

### Fichiers du projet
| Type | Chemin |
|------|--------|
| Configuration | `projects/pfe-openclaw/project.yaml` |
| Description | `projects/pfe-openclaw/PROJECT.md` |
| Agents | `projects/pfe-openclaw/agents/` |
| Livrables | `projects/pfe-openclaw/artifacts/` |
| Décisions | `projects/pfe-openclaw/decisions/` |

### Agents du projet PFE

| Agent | Fichier | Rôle |
|-------|---------|------|
| Architecte | `projects/pfe-openclaw/agents/AGENT-ARCHITECTE.md` | Architecture OpenClaw + MCP |
| DevOps | `projects/pfe-openclaw/agents/AGENT-DEVOPS.md` | CI/CD, Azure DevOps |
| Sécurité | `projects/pfe-openclaw/agents/AGENT-SECURITE.md` | Gouvernance, secrets, audit |
| Produit | `projects/pfe-openclaw/agents/AGENT-PRODUIT.md` | KPIs, valeur business |
| Recherche | `projects/pfe-openclaw/agents/AGENT-RECHERCHE/` | État de l'art, mémoire |
| Critique | `projects/pfe-openclaw/agents/AGENT-CRITIQUE.md` | Devil's advocate |

---

## Conventions de Documentation

### Langue
- **Français** pour tous les documents et commentaires
- Terminologie technique en anglais si pas d'équivalent établi

### Nommage des fichiers

| Type | Format | Exemple |
|------|--------|---------|
| Workflow | `WF-NOM.md` | `WF-DESIGN-ARCHI.md` |
| Règle | `RULES-NOM.md` | `RULES-ACTOR-CRITIC.md` |
| Template | `TPL-NOM.md` | `TPL-ARCHITECTE.md` |
| Agent projet | `AGENT-NOM.md` | `AGENT-DEVOPS.md` |
| ADR | `ADR-XXX-nom.md` | `ADR-001-framework-openclaw.md` |

### Format Markdown
- Titres : `#`, `##`, `###` avec espaces après les `#`
- Listes : tiret `-` avec espace
- Checklists : `- [ ]` et `- [x]`
- Tableaux pour données structurées
- Blocs de code avec langage spécifié
- Diagrammes ASCII dans des blocs de code

---

## Contraintes du Projet PFE

1. **Pas de sandbox** : Mode **dry-run** obligatoire en production
2. **Validation tuteur** obligatoire avant toute écriture réelle
3. **Préfixe `[OPENCLAW-TEST]`** sur tous les work items de test
4. **Zéro action sans approbation humaine** (sauf niveau 1 auto-approuvé)
5. **Objectif MTTR** : réduire de 50% le temps d'analyse primaire

---

## Stack Technique (Projet PFE)

| Composant | Technologie |
|-----------|-------------|
| Agent IA | OpenClaw (mémoire persistante, Heartbeat) |
| Intégration | MCP (Model Context Protocol) |
| CI/CD | Azure DevOps Pipelines |
| Release | Digital.ai Release (via MCP) |
| Approbation | Teams (canal dédié DevOps) |
| BDD | SQLite (POC) → PostgreSQL (V2) |
| Dashboard | Streamlit ou FastAPI + HTMX |

---

## Comment Utiliser ce Framework

### Créer un nouveau projet
```bash
cp -r core/project-template projects/mon-projet
mkdir -p projects/mon-projet/{agents,artifacts,decisions,sessions}
cd projects/mon-projet
mv *.template ${%.template}
# Éditer project.yaml et PROJECT.md
```

### Créer des agents
```bash
cp core/templates/TPL-ARCHITECTE.md projects/mon-projet/agents/AGENT-ARCHITECTE.md
# Personnaliser selon le contexte
```

### Choisir un workflow
Voir `core/workflows/README.md` pour la liste complète.

### Documenter les résultats
- Sessions → `projects/mon-projet/sessions/`
- Décisions → `projects/mon-projet/decisions/`
- Livrables → `projects/mon-projet/artifacts/`

---

## Références

- [README principal](README.md) — Vue d'ensemble du framework
- [Core README](core/README.md) — Documentation du moteur
- [Workflows](core/workflows/README.md) — Liste des workflows
- [Templates](core/templates/README.md) — Templates d'agents
- [Projet PFE](projects/pfe-openclaw/README.md) — Index du projet actif
