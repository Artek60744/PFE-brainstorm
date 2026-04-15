# WF-RESOLUTION-CONFLIT

## Objectif
Arbitrer quand les agents ne convergent pas après les tours de débat standard. Produire :
- Une synthèse des positions divergentes
- Une analyse des arguments de chaque partie
- Une décision argumentée
- Un plan de suivi si la décision est risquée

---

## Agents impliqués
- **MANAGER-DEBAT** (arbitre final)
- **Agents en conflit** (ceux qui divergent)
- **AGENT-CRITIQUE** (analyse neutre des arguments)

---

## Déclencheurs

Ce workflow est activé quand :
1. Score CRITIQUE < 3 après le maximum de tours Actor/Critic
2. Deux agents ou plus maintiennent des positions incompatibles
3. Un agent demande explicitement une escalade
4. Le MANAGER détecte une impasse dans le débat

---

## Étapes

### 1. [MANAGER-DEBAT] Constat d'impasse
- Résume le contexte du débat
- Identifie le point précis de divergence
- Liste les agents impliqués et leurs positions
- Déclare officiellement l'escalade

### 2. [AGENTS EN CONFLIT] Exposé final
Chaque agent expose sa position finale en 3 parties :
```
## Ma position
[Énoncé clair et concis]

## Mes arguments principaux (max 3)
1. [Argument 1 + preuve/source]
2. [Argument 2 + preuve/source]
3. [Argument 3 + preuve/source]

## Pourquoi je rejette la position adverse
[Réfutation structurée]

## Ce que je concède
[Points où l'adversaire a raison]

## Risque si ma position n'est pas retenue
[Impact concret]
```

### 3. [AGENT-CRITIQUE] Analyse neutre
Le CRITIQUE analyse chaque position sans prendre parti :
```
## Synthèse du conflit
[Résumé objectif]

## Analyse de la position A
| Argument | Validité (1-5) | Faiblesse potentielle |
|----------|----------------|----------------------|

## Analyse de la position B
| Argument | Validité (1-5) | Faiblesse potentielle |
|----------|----------------|----------------------|

## Points de convergence possibles
[Ce sur quoi les deux parties pourraient s'accorder]

## Options de compromis
1. [Compromis 1]
2. [Compromis 2]

## Recommandation
[Position A / Position B / Compromis X]
Justification : [...]
```

### 4. [MANAGER-DEBAT] Tentative de compromis
- Propose un compromis basé sur l'analyse du CRITIQUE
- Demande aux agents en conflit s'ils acceptent
- Si accepté : documenter et clore
- Si refusé : passer à l'arbitrage

### 5. [MANAGER-DEBAT] Arbitrage final
Si aucun compromis n'est accepté :
```
## Décision
[Position retenue ou nouvelle synthèse]

## Justification
[Pourquoi cette décision]

## Ce que chaque partie gagne
- Agent A : [...]
- Agent B : [...]

## Ce que chaque partie concède
- Agent A : [...]
- Agent B : [...]

## Risques de cette décision
| Risque | Mitigation |
|--------|------------|

## Plan de suivi
[Comment vérifier que la décision était bonne]
```

### 6. [MANAGER-DEBAT] Documentation
- Archive le débat complet pour référence future
- Note les leçons apprises pour éviter ce type de conflit
- Met à jour les règles si le conflit révèle un manque

---

## Livrables attendus

| Livrable | Format | Responsable |
|----------|--------|-------------|
| Exposés des positions | Markdown structuré | Agents en conflit |
| Analyse neutre | Tableau comparatif | CRITIQUE |
| Décision finale | Document argumenté | MANAGER |
| Plan de suivi | Actions + échéances | MANAGER |
| Archive du débat | Document complet | MANAGER |

---

## Conditions d'arrêt
- Le MANAGER tranche toujours (pas de blocage infini)
- La décision est documentée et non révisable dans la même session
- Un plan de suivi est obligatoire pour les décisions risquées

---

## Règles d'arbitrage

### Critères de décision du MANAGER
1. **Réversibilité** : Préférer la décision la plus facilement réversible
2. **Impact** : Minimiser l'impact négatif maximal
3. **Données** : Favoriser la position avec le plus de données factuelles
4. **Consensus** : Une décision acceptée par tous est préférable à une décision optimale rejetée
5. **Vélocité** : En cas d'incertitude égale, choisir la décision la plus rapide à tester

### Ce que le MANAGER ne doit pas faire
- Trancher sans écouter toutes les parties
- Ignorer l'analyse du CRITIQUE
- Prendre une décision par défaut (inaction)
- Laisser des ambiguïtés dans la décision

---

## Escalade vers l'humain

Dans certains cas, le MANAGER doit escalader vers l'humain :
- Décision impliquant un engagement budgétaire significatif
- Décision ayant un impact de sécurité critique
- Décision politique ou éthique
- Absence de consensus ET risque élevé

Format de l'escalade :
```
## Escalade requise

### Contexte
[Résumé du débat]

### Options
1. [Option A] — Défenseurs : [Agents] — Risque : [...]
2. [Option B] — Défenseurs : [Agents] — Risque : [...]

### Recommandation des agents
[Position majoritaire ou CRITIQUE]

### Ce dont nous avons besoin
[Information ou décision demandée à l'humain]
```
