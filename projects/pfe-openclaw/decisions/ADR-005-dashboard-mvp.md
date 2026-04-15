# ADR-005 : Dashboard MVP Obligatoire

## Statut
**Accepté** — Requirement non reportable

## Date
Janvier 2024

## Contexte
Le projet nécessite une interface de visualisation pour :
- Suivre les pipelines en cours
- Afficher les erreurs par pipeline avec contexte historique
- Montrer les dépendances entre pipelines
- Permettre à l'équipe de comprendre ce que fait l'agent

Initialement, le dashboard était considéré comme optionnel. Après débat, il a été reclassé comme **requirement MVP obligatoire**.

## Décision
Le dashboard est un **livrable MVP non reportable** avec un scope strict :
- Tableau des pipelines
- Filtres par statut/projet
- Contexte des erreurs par pipeline
- Visualisation des dépendances

## Justification

### Pourquoi obligatoire ?
| Argument | Réponse |
|----------|---------|
| "C'est du scope creep" | Non, c'est la valeur unique du projet |
| "L'équipe a déjà des dashboards" | Oui, mais pas la corrélation historique |
| "Ça prend trop de temps" | Scope strict, technologies simples |

### Valeur unique
Le dashboard apporte une information qu'aucun outil existant ne fournit :
- **Corrélation contextuelle** : erreurs actuelles vs historiques
- **Vue par pipeline** : pas une vue globale, mais spécifique
- **Dépendances** : quel pipeline affecte quel autre

### Scope MVP strict
| Inclus | Exclu |
|--------|-------|
| Tableau des pipelines | Graphiques complexes |
| Filtres basiques | Analytics avancés |
| Contexte par erreur | Machine learning |
| Dépendances simples | Prédiction |

### Stack technique
| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| Streamlit | Rapide, Python | Moins flexible |
| FastAPI + HTMX | Léger, moderne | Plus de code |

Décision : Choix libre selon préférence, priorité à la livraison.

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Complexité > temps | Scope strict, pas de feature creep |
| Maintenance | Auto-maintenu par l'agent si possible |
| Adoption faible | Impliquer l'équipe DevOps dès la conception |

## Conséquences
- Le dashboard est un livrable de la semaine 13
- L'équipe DevOps doit être impliquée dans l'UX
- Le dashboard peut être maintenu par l'agent lui-même

## Historique du débat

### Position initiale AGENT-CRITIQUE
> "Le dashboard n'est-il pas un scope creep ?"

### Résolution
**RÉSOLU** : Le dashboard est un requirement du MVP non reportable. Le risque est que sa complexité dépasse le temps disponible. Mitigation : scope strict.

## Références
- Discussion : AGENT-PRODUIT, AGENT-CRITIQUE, AGENT-ARCHITECTE
- Validation : Consensus après 2 tours de débat
