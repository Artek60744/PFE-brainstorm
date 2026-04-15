# ADR-002 : MCP comme Protocole d'Intégration

## Statut
**Accepté**

## Date
Janvier 2024

## Contexte
L'agent doit s'intégrer avec plusieurs systèmes externes :
- Azure DevOps (pipelines, work items, PRs)
- Digital.ai Release (releases, environnements)
- Teams (notifications, approbations)

Un protocole d'intégration standardisé est nécessaire pour éviter de développer des connecteurs custom pour chaque système.

## Décision
Utiliser **MCP (Model Context Protocol)** comme protocole d'intégration principal.

## Justification

### Avantages
| Critère | MCP | API REST directe |
|---------|-----|------------------|
| Standardisation | Protocole émergent | Chaque API différente |
| Serveurs existants | Microsoft (ADO), Digital.ai | N/A |
| Interopérabilité | Oui | Non |
| Maintenance | Par les éditeurs | Par nous |

### Serveurs MCP disponibles
- **MCP Microsoft** : Azure DevOps (lecture + écriture wit_*)
- **MCP Digital.ai Release** : Releases, environnements, approbations

### Écriture confirmée
Le serveur MCP Microsoft supporte les opérations d'écriture :
- `wit_create_work_item` — Création de tickets
- `wit_add_work_item_comment` — Commentaires d'audit
- `wit_update_work_item` — Mise à jour

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| MCP est un standard récent | Fallback API REST si nécessaire |
| Champs personnalisés Isagri | Test en S4 avec wit_create_work_item |
| Limitations d'écriture | Skills custom OpenClaw en fallback |

## Conséquences
- L'architecture utilise MCP comme couche d'abstraction
- Moins de code d'intégration à maintenir
- Dépendance aux serveurs MCP des éditeurs

## Alternatives considérées
| Alternative | Raison du rejet |
|-------------|-----------------|
| API REST directe | Plus de maintenance, moins standard |
| Webhooks uniquement | Pas de lecture proactive |
| GraphQL | Non supporté par ADO/Digital.ai |

## Références
- Discussion : AGENT-ARCHITECTE
- Validation : AGENT-CRITIQUE (MIS À JOUR après vérification MCP Digital.ai)
