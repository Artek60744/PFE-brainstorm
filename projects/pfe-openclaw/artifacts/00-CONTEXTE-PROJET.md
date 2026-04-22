# Contexte du Projet PFE

## Titre
**Dans quelle mesure un agent IA avec Read-Plan-Approve-Execute peut-il réduire le MTTR des incidents DevOps ?**

## Contexte
- **Type** : Projet de Fin d'Études - Ingénierie DevOps
- **Durée** : 6 mois
- **Entreprise** : Isagri
- **Établissement** : UniLaSalle

## Stack Technique
| Composant | Technologie |
|-----------|-------------|
| Agent IA | OpenClaw (open-source, mémoire persistante, Heartbeat) |
| Protocole d'intégration | Model Context Protocol (MCP) |
| CI/CD | Azure DevOps Pipelines |
| Orchestration de Release | Digital.ai Release (via serveur MCP officiel) |
| Canal d'approbation | Teams (boutons interactifs, canal dédié) |
| Authentification | Serveur MCP Microsoft (délégation standardisée) |
| Audit | Commentaires automatiques dans Azure DevOps Work Items |
| Environnement de test | Production uniquement (pas de bac à sable) — mode dry-run obligatoire |

## Architecture Cible
```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Agent                           │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐ │
│  │   Read    │→ │   Plan    │→ │  Approve  │→ │ Execute  │ │
│  │ (MCP)     │  │ (Diagnostic│  │ (Teams)   │  │ (MCP)    │ │
│  └───────────┘  └───────────┘  └───────────┘  └──────────┘ │
│         ↑              ↑             ↑              ↑       │
│         └──────────────┴─────────────┴──────────────┘       │
│                        Heartbeat (surveillance continue)     │
└─────────────────────────────────────────────────────────────┘
         │              │             │              │
         ▼              ▼             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌─────────┐ ┌──────────────┐
│ Azure DevOps │ │ Digital.ai   │ │ Humain  │ │ Azure DevOps │
│ (via MCP)    │ │ Release      │ │ (via    │ │ (via MCP)    │
│              │ │ (Skill custom│ │  Teams) │ │              │
│ - Logs       │ │  ou MCP)     │ │         │ │ - Tickets    │
│ - Work Items │ │              │ │         │ │ - Commentaires│
│ - Pipelines  │ │ - Releases   │ │         │ │ - Audit trail│
└──────────────┘ └──────────────┘ └─────────┘ └──────────────┘
```

## Objectif Principal
**Réduire de 50% le temps humain passé sur l'analyse primaire d'un échec de pipeline** lors du prochain PI Planning.

## Phasage des Capacités de l'Agent
| Phase | Capacité | Description |
|-------|----------|-------------|
| Phase 1 | **Diagnostic** | Détection d'échec de pipeline, lecture des logs, identification de la cause racine |
| Phase 2 | **Release Notes** | Analyse des blocages de release, génération de rapports contextuels |
| Phase 3 | **Correction** | Proposition de correctifs avec validation humaine (RPAE strict) |

## Dashboard Agent
Un dashboard maintenu par l'agent depuis lequel on peut suivre :
- Pipelines en cours (Azure DevOps + Digital.ai Release)
- Suivi des erreurs avec archive BDD des erreurs précédentes
- Aide à la résolution avec contexte historique

## Évaluation
- **Quantitative** : Réduction du MTTR mesurée sur les incidents traités
- **Qualitative** : Confiance de l'équipe Isagri envers l'autonomie d'OpenClaw
