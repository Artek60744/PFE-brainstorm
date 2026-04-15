# Brainstorm Framework — Core

Ce dossier contient le **moteur** du framework de brainstorming IA. Il est indépendant des projets et peut être réutilisé pour n'importe quel brainstorm.

---

## Structure

```
core/
├── workflows/          # Workflows de débat (le "quoi")
├── rules/              # Règles de débat (le "comment")
├── templates/          # Templates d'agents (le "qui")
└── project-template/   # Template pour créer un nouveau projet
```

---

## Composants

### Workflows (`workflows/`)

Les workflows définissent les **étapes** d'un type de débat.

| Workflow | Description | Durée |
|----------|-------------|-------|
| [WF-BRAINSTORM-IDEES](workflows/WF-BRAINSTORM-IDEES.md) | Explorer une idée | 30 min |
| [WF-DESIGN-ARCHI](workflows/WF-DESIGN-ARCHI.md) | Concevoir une architecture | 45 min |
| [WF-REVUE-SECURITE](workflows/WF-REVUE-SECURITE.md) | Auditer la sécurité | 30 min |
| [WF-PLANIFICATION](workflows/WF-PLANIFICATION.md) | Planifier un projet | 45 min |
| [WF-RETROSPECTIVE](workflows/WF-RETROSPECTIVE.md) | Analyser une phase passée | 30 min |
| [WF-RESOLUTION-CONFLIT](workflows/WF-RESOLUTION-CONFLIT.md) | Arbitrer un désaccord | 20 min |
| [WF-VALIDATION-LIVRABLE](workflows/WF-VALIDATION-LIVRABLE.md) | Valider avant livraison | 20 min |

### Règles (`rules/`)

Les règles définissent les **comportements** attendus pendant les débats.

| Règle | Description |
|-------|-------------|
| [RULES-DEBAT-GENERAL](rules/RULES-DEBAT-GENERAL.md) | Principes de base |
| [RULES-ACTOR-CRITIC](rules/RULES-ACTOR-CRITIC.md) | Pattern proposition/critique |
| [RULES-MANAGER-ROUTING](rules/RULES-MANAGER-ROUTING.md) | Sélection des agents |
| [RULES-ESCALADE](rules/RULES-ESCALADE.md) | Quand escalader vers l'humain |
| [RULES-FORMAT-SORTIE](rules/RULES-FORMAT-SORTIE.md) | Standards de formatage |
| [RULES-TIMEBOXING](rules/RULES-TIMEBOXING.md) | Gestion du temps |

### Templates (`templates/`)

Les templates définissent les **rôles** génériques des agents.

| Template | Rôle | Type |
|----------|------|------|
| [TPL-ARCHITECTE](templates/TPL-ARCHITECTE.md) | Architecture technique | Actor |
| [TPL-DEVOPS](templates/TPL-DEVOPS.md) | CI/CD, Infrastructure | Actor |
| [TPL-PRODUCT-OWNER](templates/TPL-PRODUCT-OWNER.md) | Valeur métier | Actor |
| [TPL-TESTEUR-QA](templates/TPL-TESTEUR-QA.md) | Qualité, Tests | Actor |
| [TPL-SECOPS](templates/TPL-SECOPS.md) | Sécurité | Actor |
| [TPL-FINOPS](templates/TPL-FINOPS.md) | Coûts | Actor |
| [TPL-CHERCHEUR](templates/TPL-CHERCHEUR.md) | Recherche | Actor |
| [TPL-DATA-ENGINEER](templates/TPL-DATA-ENGINEER.md) | Données | Actor |
| [TPL-CRITIQUE](templates/TPL-CRITIQUE.md) | Devil's advocate | Critic |
| [TPL-MANAGER-DEBAT](templates/TPL-MANAGER-DEBAT.md) | Orchestration | Manager |

---

## Comment Utiliser

### 1. Créer un nouveau projet

```bash
cp -r core/project-template projects/mon-projet
cd projects/mon-projet
# Éditer project.yaml et PROJECT.md
```

### 2. Sélectionner un workflow

Choisir le workflow adapté au type de question :
- Idée floue → `WF-BRAINSTORM-IDEES`
- Conception → `WF-DESIGN-ARCHI`
- Planification → `WF-PLANIFICATION`

### 3. Instancier les agents

Créer les agents du projet en s'inspirant des templates :
```bash
cp core/templates/TPL-ARCHITECTE.md projects/mon-projet/agents/AGENT-ARCHITECTE.md
# Personnaliser pour le contexte du projet
```

### 4. Exécuter le débat

Suivre les étapes du workflow choisi avec les agents sélectionnés.

### 5. Documenter les résultats

- Synthèses → `projects/mon-projet/sessions/`
- Décisions → `projects/mon-projet/decisions/`
- Livrables → `projects/mon-projet/artifacts/`

---

## Principes du Framework

### Séparation des responsabilités
- **Workflows** : Définissent le processus
- **Rules** : Définissent les comportements
- **Templates** : Définissent les rôles
- **Projects** : Contiennent les résultats

### Extensibilité
- Ajouter de nouveaux workflows
- Créer de nouvelles règles
- Définir de nouveaux templates d'agents

### Réutilisabilité
- Le `core/` est identique pour tous les projets
- Seuls les `projects/` varient
