# ADR-006 : Mémoire par Pipeline

## Statut
**Accepté**

## Date
Janvier 2024

## Contexte
L'agent doit diagnostiquer les erreurs de pipeline en s'appuyant sur l'historique. La question est : comment organiser cette mémoire ?

Options considérées :
1. Base globale (toutes les erreurs ensemble)
2. Base par pipeline (erreurs spécifiques à chaque pipeline)
3. Base de patterns (types d'erreurs, pas instances)

## Décision
Utiliser une **mémoire par pipeline** avec prise en compte des **dépendances entre pipelines**.

## Justification

### Pourquoi par pipeline ?
| Approche | Avantage | Inconvénient |
|----------|----------|--------------|
| Globale | Simple | Bruit, corrélations fausses |
| Par pipeline | Contexte précis | Plus complexe |
| Patterns | Généralisation | Perd le contexte spécifique |

**Argument clé** : Une erreur sur le pipeline A n'a pas la même signification que la même erreur sur le pipeline B. Le contexte du pipeline (dépendances, historique, fréquence) est essentiel au diagnostic.

### Architecture de la mémoire
```
┌─────────────────────────────────────────────────────────┐
│                    Memory Store                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Pipeline A                    Pipeline B                │
│  ┌─────────────────┐          ┌─────────────────┐       │
│  │ Erreurs         │          │ Erreurs         │       │
│  │ Contexte        │───────▶  │ Contexte        │       │
│  │ Résolutions     │ dépend   │ Résolutions     │       │
│  └─────────────────┘          └─────────────────┘       │
│           │                            │                 │
│           └────────────┬───────────────┘                │
│                        ▼                                 │
│              ┌─────────────────┐                        │
│              │ Corrélation     │                        │
│              │ Cross-pipeline  │                        │
│              └─────────────────┘                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Modèle de données
```yaml
pipeline_memory:
  pipeline_id: "build-api-v2"
  errors:
    - signature: "hash123"
      first_seen: "2024-01-10"
      occurrences: 5
      context:
        stage: "build"
        error_type: "compilation"
        affected_files: ["src/api/handler.ts"]
      resolutions:
        - action: "retry"
          success_rate: 0.8
        - action: "clear_cache"
          success_rate: 0.95
  dependencies:
    - pipeline_id: "build-common-lib"
      type: "upstream"
    - pipeline_id: "deploy-api"
      type: "downstream"
```

### Algorithme de diagnostic
1. Chercher dans l'historique du **même pipeline** (priorité haute)
2. Chercher dans les **pipelines dépendants** (priorité moyenne)
3. Chercher dans la **base globale** (priorité basse)

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Complexité d'implémentation | Commencer simple (pipeline_id + erreur) |
| Dépendances complexes | Ajouter progressivement |
| Volume de données | Rétention 90 jours par défaut |

## Conséquences
- Schéma de BDD plus complexe
- Meilleure précision des diagnostics
- Possibilité de détecter les cascades d'erreurs

## Historique du débat

### Position initiale AGENT-CRITIQUE
> "Une base d'erreurs historiques n'est utile que si les erreurs sont récurrentes."

### Réponse
La mémoire par pipeline ajoute le contexte qui manquait. Les erreurs sont corrélées au pipeline spécifique, pas à une base globale bruitée.

## Références
- Discussion : AGENT-ARCHITECTE, AGENT-DEVOPS, AGENT-CRITIQUE
- Pattern : Context-aware memory
