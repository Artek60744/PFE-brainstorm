# ADR-003 : SQLite pour le POC, PostgreSQL pour V2

## Statut
**Accepté**

## Date
Janvier 2024

## Contexte
L'agent nécessite une base de données pour :
- Stocker l'historique des erreurs par pipeline
- Maintenir le journal d'audit des actions
- Gérer la mémoire contextuelle de l'agent

Le choix doit équilibrer simplicité (POC) et scalabilité (production).

## Décision
- **POC (V1)** : SQLite avec mode WAL
- **Production (V2)** : Migration vers PostgreSQL

Avec une **interface Repository abstraite** pour faciliter la migration.

## Justification

### SQLite pour le POC
| Critère | Avantage |
|---------|----------|
| Déploiement | Fichier unique, pas de serveur |
| Maintenance | Zéro configuration |
| Performance | Suffisant pour volumes POC |
| Backup | Copie de fichier simple |

### PostgreSQL pour V2
| Critère | Avantage |
|---------|----------|
| Concurrence | Multi-connexions native |
| Scalabilité | Volumes production |
| Fonctionnalités | Full-text search, JSONB |

### Architecture
```
┌─────────────────────────────────────┐
│         OpenClaw Agent              │
└──────────────┬──────────────────────┘
               │
      ┌────────▼────────┐
      │   Repository    │  ← Interface abstraite
      │    Interface    │
      └────────┬────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌────────┐          ┌────────────┐
│ SQLite │ (POC)    │ PostgreSQL │ (V2)
└────────┘          └────────────┘
```

## Stratégie de mémoire
**Mémoire par pipeline** : Les erreurs sont corrélées par pipeline en priorité, puis globalement.

| Champ | Description |
|-------|-------------|
| pipeline_id | Identifiant du pipeline |
| error_signature | Hash de l'erreur |
| context | Contexte de l'erreur (JSON) |
| resolution | Résolution appliquée |
| dependencies | Pipelines dépendants |

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Concurrence SQLite limitée | Mode WAL + mutex applicatif |
| Migration V2 complexe | Interface Repository abstraite |
| Schéma évolue pendant POC | Migrations versionnées |

## Conséquences
- Code découplé de la base de données
- Migration V2 facilitée
- Complexité légèrement accrue (abstraction)

## Alternatives considérées
| Alternative | Raison du rejet |
|-------------|-----------------|
| PostgreSQL dès le POC | Overhead de setup inutile |
| MongoDB | Pas de valeur ajoutée pour ce cas |
| Fichiers JSON | Pas de requêtes complexes |

## Références
- Discussion : AGENT-ARCHITECTE, AGENT-CRITIQUE
- Pattern : Repository Pattern
