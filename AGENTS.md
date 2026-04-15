# AGENTS.md — Guide pour Agents IA

## Contexte du Projet

Ce dépôt contient la planification d'un PFE (Projet de Fin d'Études) visant à évaluer dans quelle mesure un agent IA avec le pattern **Read-Plan-Approve-Execute (RPAE)** peut réduire le MTTR des incidents DevOps.

- **Entreprise** : Isagri | **Établissement** : UniLaSalle (programme RIOC)
- **Stack cible** : OpenClaw + MCP + Azure DevOps + Digital.ai Release + Slack/Teams
- **Phase actuelle** : Planification (pré-implémentation)

## Build / Test / Lint

Ce dépôt est **documentation-only** pour le moment. Aucun système de build, test ou lint n'est configuré.

| Action | Commande | Notes |
|--------|----------|-------|
| Vérifier les fichiers Markdown | `ls *.md agents/**/*.md` | Tous les documents sont en `.md` |
| Exécuter un test futur | _À définir_ | Le code n'existe pas encore |

Quand le code sera ajouté (semaines 1-3), les commandes seront documentées ici.

## Conventions de Documentation

### Langue
- **Français** pour tous les documents et commentaires
- Terminologie technique en anglais si pas d'équivalent français établi

### Nommage des Fichiers
- Préfixe numérique zero-padded : `00-`, `01-`, `07-`, etc.
- Kebab-case en majuscules : `00-CONTEXTE-PROJET.md`
- Agents dans `agents/` : `01-AGENT-ARCHITECTE.md`

### Format Markdown
- Titres : `#`, `##`, `###` avec espaces après les `#`
- Listes : tiret `-` avec espace
- Checklists : `- [ ]` et `- [x]`
- Tableaux pour données structurées (décisions, risques, backlog)
- Blocs de code avec langage spécifié : `` ```python ``
- Diagrammes ASCII dans des blocs de code

### Structure des Documents
1. Titre avec `#`
2. Sections avec `##`
3. Sous-sections avec `###`
4. Séparateurs `---` entre sections majeures
5. Tableaux récapitulatifs quand pertinent

## Agents et Rôles

Le dossier `agents/` définit 6 personas IA :

| Agent | Fichier | Rôle |
|-------|---------|------|
| Architecte | `agents/01-AGENT-ARCHITECTE.md` | Architecture technique, composants, interfaces |
| DevOps | `agents/02-AGENT-DEVOPS.md` | CI/CD, scénarios d'incidents, patterns |
| Sécurité | `agents/03-AGENT-SECURITE.md` | Gouvernance, secrets, audit |
| Produit | `agents/04-AGENT-PRODUIT.md` | Personas, UX, KPIs, valeur business |
| Recherche | `agents/05-AGENT-RECHERCHE/` | État de l'art, rédaction mémoire |
| Critique | `agents/06-AGENT-CRITIQUE.md` | Contre-arguments, attaque d'hypothèses |

## Règles Cursor / Copilot

Aucun fichier `.cursorrules`, `.cursor/rules/`, ou `.github/copilot-instructions.md` n'existe. Les conventions ci-dessus font office de règles.

## Contraintes Critiques

1. **Pas de bac à sable** : tout test d'écriture doit utiliser le mode **dry-run** en production
2. **Validation tuteur obligatoire** avant toute écriture réelle en production
3. **Préfixe `[OPENCLAW-TEST]`** sur tous les work items de test
4. **Zéro action sans approbation humaine** (sauf niveau 1 auto-approuvé)
5. **Objectif MTTR** : réduire de 50% le temps d'analyse primaire d'échec de pipeline

## Stack Technique Cible

| Composant | Technologie |
|-----------|-------------|
| Agent IA | OpenClaw (open-source, mémoire persistante, Heartbeat) |
| Intégration | Model Context Protocol (MCP) |
| CI/CD | Azure DevOps Pipelines |
| Release | Digital.ai Release (via MCP officiel) |
| Approbation | Slack / Teams (boutons interactifs) |
| Auth | MCP Microsoft server |
| Audit | Azure DevOps Work Items comments |
| BDD (POC) | SQLite → PostgreSQL (V2) |
| Dashboard | Streamlit ou FastAPI + HTMX |
| VCS | Git |

## Backlog et Priorisation

Voir `09-BACKLOG.md` pour le backlog complet avec priorisation MoSCoW.

- **MVP** (S1-S15) : Cycle RPAE sur échecs de pipeline ADO
- **V1** (S16-S20) : + Digital.ai + Dashboard + Mesure MTTR
- **V2** (post-PFE) : Industrialisation

## Quand le Code Sera Ajouté

- Suivre les conventions existantes du langage/framework choisi
- Tests unitaires obligatoires pour toute logique métier
- Mode dry-run implémenté avant toute logique d'écriture
- Journal d'audit pour chaque action de l'agent
- Préfixe `[OPENCLAW-TEST]` sur les ressources de test
