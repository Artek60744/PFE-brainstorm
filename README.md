# Brainstorm Framework

Un framework modulaire pour orchestrer des sessions de brainstorming IA multi-agents.

---

## Concept

Ce framework permet de structurer des débats entre agents IA spécialisés pour produire des documents et décisions de haute qualité. Il sépare :

- **Le moteur** (`core/`) : Workflows, règles et templates réutilisables
- **Les projets** (`projects/`) : Contexte, agents et résultats spécifiques

```
┌─────────────────────────────────────────────────────────────┐
│                      FRAMEWORK                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   core/                          projects/                   │
│   ┌──────────────┐              ┌──────────────┐            │
│   │  workflows/  │              │ projet-1/    │            │
│   │  rules/      │───────────▶  │   agents/    │            │
│   │  templates/  │              │   artifacts/ │            │
│   └──────────────┘              │   decisions/ │            │
│                                  └──────────────┘            │
│                                  ┌──────────────┐            │
│                                  │ projet-2/    │            │
│                                  │   ...        │            │
│                                  └──────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Structure

```
brainstorming/
├── README.md                 # Ce fichier
├── AGENTS.md                 # Configuration globale pour les outils IA
├── core/                     # Moteur du framework (réutilisable)
│   ├── workflows/            # Workflows de débat
│   ├── rules/                # Règles de comportement
│   ├── templates/            # Templates d'agents
│   └── project-template/     # Template pour nouveau projet
└── projects/                 # Projets de brainstorming
    └── pfe-openclaw/         # Exemple : PFE OpenClaw
        ├── project.yaml      # Configuration technique
        ├── PROJECT.md        # Description narrative
        ├── agents/           # Agents spécialisés
        ├── artifacts/        # Livrables
        ├── decisions/        # ADR
        └── sessions/         # Historique des sessions
```

---

## Quick Start

### 1. Créer un nouveau projet

```bash
# Copier le template
cp -r core/project-template projects/mon-projet

# Créer les dossiers
mkdir -p projects/mon-projet/{agents,artifacts,decisions,sessions}

# Renommer les fichiers
cd projects/mon-projet
mv project.yaml.template project.yaml
mv PROJECT.md.template PROJECT.md
mv README.md.template README.md

# Éditer la configuration
vim project.yaml
vim PROJECT.md
```

### 2. Créer les agents

```bash
# Copier les templates nécessaires
cp core/templates/TPL-ARCHITECTE.md projects/mon-projet/agents/AGENT-ARCHITECTE.md
cp core/templates/TPL-CRITIQUE.md projects/mon-projet/agents/AGENT-CRITIQUE.md

# Personnaliser selon le contexte du projet
vim projects/mon-projet/agents/AGENT-ARCHITECTE.md
```

### 3. Choisir un workflow

| Besoin | Workflow |
|--------|----------|
| Explorer une idée | `WF-BRAINSTORM-IDEES` |
| Concevoir une architecture | `WF-DESIGN-ARCHI` |
| Planifier un projet | `WF-PLANIFICATION` |
| Auditer la sécurité | `WF-REVUE-SECURITE` |
| Analyser une phase passée | `WF-RETROSPECTIVE` |
| Valider un livrable | `WF-VALIDATION-LIVRABLE` |

### 4. Exécuter le débat

Suivre les étapes du workflow choisi avec les agents sélectionnés.

### 5. Documenter les résultats

```bash
# Synthèse de session
vim projects/mon-projet/sessions/2024-01-15-sujet.md

# Décision (ADR)
vim projects/mon-projet/decisions/ADR-001-decision.md

# Livrable
vim projects/mon-projet/artifacts/mon-document.md
```

---

## Composants du Core

### Workflows
| Workflow | Description | Durée |
|----------|-------------|-------|
| [WF-BRAINSTORM-IDEES](core/workflows/WF-BRAINSTORM-IDEES.md) | Explorer une idée | 30 min |
| [WF-DESIGN-ARCHI](core/workflows/WF-DESIGN-ARCHI.md) | Concevoir une architecture | 45 min |
| [WF-REVUE-SECURITE](core/workflows/WF-REVUE-SECURITE.md) | Auditer la sécurité | 30 min |
| [WF-PLANIFICATION](core/workflows/WF-PLANIFICATION.md) | Planifier un projet | 45 min |
| [WF-RETROSPECTIVE](core/workflows/WF-RETROSPECTIVE.md) | Analyser une phase | 30 min |
| [WF-RESOLUTION-CONFLIT](core/workflows/WF-RESOLUTION-CONFLIT.md) | Arbitrer un désaccord | 20 min |
| [WF-VALIDATION-LIVRABLE](core/workflows/WF-VALIDATION-LIVRABLE.md) | Valider avant livraison | 20 min |

### Règles
| Règle | Description |
|-------|-------------|
| [RULES-DEBAT-GENERAL](core/rules/RULES-DEBAT-GENERAL.md) | Principes de base |
| [RULES-ACTOR-CRITIC](core/rules/RULES-ACTOR-CRITIC.md) | Pattern proposition/critique |
| [RULES-MANAGER-ROUTING](core/rules/RULES-MANAGER-ROUTING.md) | Sélection des agents |
| [RULES-ESCALADE](core/rules/RULES-ESCALADE.md) | Escalade vers l'humain |
| [RULES-FORMAT-SORTIE](core/rules/RULES-FORMAT-SORTIE.md) | Standards de formatage |
| [RULES-TIMEBOXING](core/rules/RULES-TIMEBOXING.md) | Gestion du temps |

### Templates d'agents
| Template | Rôle |
|----------|------|
| [TPL-ARCHITECTE](core/templates/TPL-ARCHITECTE.md) | Architecture technique |
| [TPL-DEVOPS](core/templates/TPL-DEVOPS.md) | CI/CD, Infrastructure |
| [TPL-PRODUCT-OWNER](core/templates/TPL-PRODUCT-OWNER.md) | Valeur métier |
| [TPL-TESTEUR-QA](core/templates/TPL-TESTEUR-QA.md) | Qualité, Tests |
| [TPL-SECOPS](core/templates/TPL-SECOPS.md) | Sécurité |
| [TPL-FINOPS](core/templates/TPL-FINOPS.md) | Coûts |
| [TPL-CHERCHEUR](core/templates/TPL-CHERCHEUR.md) | Recherche |
| [TPL-DATA-ENGINEER](core/templates/TPL-DATA-ENGINEER.md) | Données |
| [TPL-CRITIQUE](core/templates/TPL-CRITIQUE.md) | Devil's advocate |
| [TPL-MANAGER-DEBAT](core/templates/TPL-MANAGER-DEBAT.md) | Orchestration |

---

## Projets Existants

| Projet | Description | Statut |
|--------|-------------|--------|
| [pfe-openclaw](projects/pfe-openclaw/) | Agent IA RPAE pour réduction MTTR | Actif |

---

## Principes

### Séparation des responsabilités
- **Core** : Logique métier du brainstorming (stable)
- **Projects** : Contexte et résultats (variable)

### Pattern Actor-Critic
- **Actors** : Agents producteurs qui proposent
- **Critic** : Agent qui challenge et améliore
- **Manager** : Orchestre et synthétise

### Extensibilité
- Ajouter de nouveaux workflows
- Créer de nouvelles règles
- Définir de nouveaux templates d'agents

### Documentation
- Chaque décision est un ADR
- Chaque session a une synthèse
- Chaque projet est auto-documenté

---

## Contribuer

### Ajouter un workflow
1. Créer `core/workflows/WF-NOUVEAU.md`
2. Suivre la structure existante
3. Ajouter au README de `core/workflows/`

### Ajouter un template d'agent
1. Créer `core/templates/TPL-NOUVEAU.md`
2. Suivre `STRUCTURE-TEMPLATE.md`
3. Ajouter au README de `core/templates/`

### Ajouter une règle
1. Créer `core/rules/RULES-NOUVELLE.md`
2. Documenter les cas d'usage
3. Ajouter au README de `core/rules/`
