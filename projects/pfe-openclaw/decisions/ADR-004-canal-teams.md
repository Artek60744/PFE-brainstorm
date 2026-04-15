# ADR-004 : Teams comme Canal d'Approbation

## Statut
**Accepté**

## Date
Janvier 2024

## Contexte
Le pattern RPAE nécessite une phase d'approbation humaine avant l'exécution. L'agent doit pouvoir :
- Envoyer des demandes d'approbation
- Recevoir les réponses (Approuver/Rejeter)
- Restreindre l'approbation aux personnes autorisées
- Gérer les timeouts

## Décision
Utiliser **Microsoft Teams** avec un **canal dédié à l'équipe DevOps** comme interface d'approbation.

## Justification

### Pourquoi Teams ?
| Critère | Teams | Slack | Email |
|---------|-------|-------|-------|
| Déjà utilisé par Isagri | Oui | Non | Oui |
| Boutons interactifs | Oui | Oui | Non |
| Canal dédié | Oui | Oui | Non |
| Restriction d'accès | Oui (canal) | Oui | Complexe |
| Intégration Microsoft | Native | Non | - |

### Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Teams                              │
│  ┌─────────────────────────────────────────────┐    │
│  │     Canal : #devops-openclaw-approvals      │    │
│  │                                              │    │
│  │  ┌────────────────────────────────────────┐ │    │
│  │  │ [OpenClaw] Demande d'approbation       │ │    │
│  │  │                                        │ │    │
│  │  │ Pipeline: build-api-v2                 │ │    │
│  │  │ Action: Relancer le build              │ │    │
│  │  │ Risque: Faible                         │ │    │
│  │  │                                        │ │    │
│  │  │ [✓ Approuver]  [✗ Rejeter]            │ │    │
│  │  └────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### Niveaux d'approbation
| Niveau | Type d'action | Approbateurs | Timeout |
|--------|---------------|--------------|---------|
| 1 | Informatif (logs, tickets info) | Auto-approuvé | - |
| 2 | Standard (relance, commentaire) | 1 membre DevOps | 30 min |
| 3 | Critique (rollback, config prod) | 2 membres DevOps | 30 min |

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Automation bias (clic sans lire) | Résumé 3 lignes + cooling-off 30s |
| Timeout non respecté | Escalade automatique + annulation |
| Canal saturé | Filtrage par priorité |

## Conséquences
- Intégration avec l'API Teams ou Power Automate
- Formation de l'équipe DevOps sur le canal
- Monitoring des temps de réponse

## Alternatives considérées
| Alternative | Raison du rejet |
|-------------|-----------------|
| Slack | Non utilisé par Isagri |
| Email | Pas de boutons interactifs |
| Interface web dédiée | Développement additionnel |
| Azure DevOps Approvals | Moins flexible |

## Références
- Discussion : AGENT-ARCHITECTE, AGENT-SECURITE
- Validation : Équipe DevOps Isagri
