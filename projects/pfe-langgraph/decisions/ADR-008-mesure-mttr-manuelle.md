# ADR-008 : Mesure MTTR Manuelle

## Statut
**Accepté**

## Date
Janvier 2024

## Contexte
L'objectif du PFE est de réduire le MTTR (Mean Time To Repair) de 50%. Pour mesurer cet objectif, il faut :
1. Établir une baseline (MTTR actuel)
2. Mesurer le MTTR après implémentation
3. Comparer les deux

**Problème** : Azure DevOps ne fournit pas de métrique MTTR directement extractible.

## Décision
Utiliser une **mesure manuelle combinée** :
1. Chronométrage manuel de 10-15 incidents
2. Delta Work Items ADO (création → résolution)

## Justification

### Pourquoi pas d'extraction automatique ?
| Méthode | Problème |
|---------|----------|
| API Azure DevOps | Pas de champ "temps de résolution incident" |
| Métriques pipelines | Mesurent le temps de build, pas de diagnostic |
| Work Items | Pas de workflow standardisé "incident" |

### Méthode proposée

#### 1. Chronométrage manuel (baseline)
| Étape | Description |
|-------|-------------|
| Sélection | 10-15 incidents variés (simples et complexes) |
| Chronomètre | Temps entre détection et résolution |
| Catégories | Par type d'incident (build, deploy, config) |

#### 2. Delta Work Items (après agent)
| Champ | Utilisation |
|-------|-------------|
| Created Date | Début de l'incident |
| Resolved Date | Fin de l'incident |
| Delta | MTTR approximatif |

#### 3. Croisement des sources
```
MTTR estimé = (Chronométrage manuel + Delta Work Items) / 2
```

### Tableau de mesure
| Incident | Type | MTTR Avant | MTTR Après | Gain |
|----------|------|------------|------------|------|
| #1 | Build simple | 15 min | 8 min | 47% |
| #2 | Build complexe | 45 min | 20 min | 56% |
| #3 | Déploiement | 30 min | 25 min | 17% |
| ... | ... | ... | ... | ... |
| **Moyenne** | - | **30 min** | **18 min** | **40%** |

### Objectif réaliste
| Cible initiale | Analyse réaliste |
|----------------|------------------|
| 50% de réduction | Ambitieux mais maintenu comme objectif |
| | Résultats analysés honnêtement |
| | Différenciation par type d'incident |

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Biais de sélection des incidents | Échantillon varié, critères documentés |
| Chronométrage imprécis | Deux sources croisées |
| Objectif 50% non atteint | Analyse honnête des résultats |

## Conséquences
- Processus de mesure plus lourd
- Résultats moins "scientifiques" mais réalistes
- Section méthodologique importante dans le mémoire

## Protocole de mesure

### Phase Baseline (S3)
1. Identifier 10-15 incidents passés
2. Reconstituer les temps (logs, Work Items, témoignages)
3. Catégoriser par type
4. Calculer MTTR moyen par catégorie

### Phase Mesure (S18-22)
1. Chronométrer les incidents traités avec l'agent
2. Extraire les deltas Work Items
3. Comparer avec la baseline
4. Analyser les écarts par type

### Livrable
Rapport avec :
- Méthodologie détaillée
- Données brutes
- Analyse par type d'incident
- Conclusion honnête sur l'objectif 50%

## Références
- Discussion : AGENT-DEVOPS, AGENT-PRODUIT, AGENT-CRITIQUE
- Validation : Tuteur (objectif 50% maintenu comme cible)
