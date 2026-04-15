# WF-PLANIFICATION-PROJET

## Objectif
Débattre de la roadmap, du backlog et des priorités d'un projet. Produire :
- Un backlog priorisé (MoSCoW ou équivalent)
- Un planning avec jalons et dépendances
- Une estimation des risques de planning
- Une définition claire du MVP

---

## Agents impliqués
- **MANAGER-DEBAT** (orchestrateur)
- **AGENT-PRODUIT** (lead — valeur métier, priorisation)
- **AGENT-ARCHITECTE** (complexité technique, dépendances)
- **AGENT-DEVOPS** (contraintes opérationnelles, environnements)
- **AGENT-CRITIQUE** (réalisme des estimations, risques)

---

## Étapes

### 1. [MANAGER-DEBAT] Cadrage
- Reformule les objectifs du projet
- Identifie les contraintes :
  - Budget et ressources disponibles
  - Échéances fixes (dates de livraison, soutenance, etc.)
  - Dépendances externes (équipes, validations, accès)
- Définit l'horizon de planification (MVP, V1, V2)
- Rappelle les KPIs de succès

### 2. [AGENT-PRODUIT] Proposition de backlog
- Liste les fonctionnalités/tâches identifiées
- Priorise avec MoSCoW :
  - **Must have** : Indispensable au MVP
  - **Should have** : Important mais contournable
  - **Could have** : Nice-to-have si temps disponible
  - **Won't have** : Hors scope de cette version
- Justifie chaque priorisation par la valeur métier
- Propose une définition du MVP (scope minimal)

### 3. [AGENT-ARCHITECTE] Estimation technique
- Évalue la complexité de chaque item (T-shirt sizing : XS, S, M, L, XL)
- Identifie les dépendances techniques entre items
- Signale les items à risque technique élevé
- Propose un ordre d'implémentation optimal (dépendances + risques d'abord)
- Alerte sur les items sous-estimés

### 4. [AGENT-DEVOPS] Contraintes opérationnelles
- Identifie les besoins en environnements (dev, staging, prod)
- Estime le temps de setup infrastructure
- Signale les dépendances externes (accès, credentials, validations)
- Propose des jalons techniques (environnement prêt, pipeline fonctionnel, etc.)
- Évalue la capacité de l'équipe (disponibilité réelle)

### 5. [AGENT-CRITIQUE] Challenge du planning
- Questionne le réalisme des estimations
- Identifie les risques de planning :
  - Dépendances externes non maîtrisées
  - Items sous-estimés
  - Absence de buffer pour les imprévus
- Vérifie que le MVP est réellement minimal
- Propose des alternatives (réduire le scope, paralléliser, etc.)
- Attribue un score de confiance au planning (1-5)

### 6. [BOUCLE ACTOR/CRITIC — 2 tours]
- **Tour 1** : AGENT-PRODUIT révise le backlog et le planning en intégrant les retours
- AGENT-CRITIQUE évalue la révision
- **Tour 2** : AGENT-PRODUIT finalise
- AGENT-CRITIQUE donne son évaluation finale

### 7. [MANAGER-DEBAT] Synthèse
- Valide le backlog priorisé final
- Produit le planning avec jalons :
  - Dates clés
  - Livrables par jalon
  - Responsables
- Documente les risques de planning et mitigations
- Définit les critères de go/no-go pour chaque jalon

---

## Livrables attendus

| Livrable | Format | Responsable |
|----------|--------|-------------|
| Backlog priorisé | Tableau MoSCoW avec estimations | PRODUIT |
| Définition du MVP | Liste des items Must Have | PRODUIT |
| Graphe de dépendances | Liste ou diagramme | ARCHITECTE |
| Planning jalons | Tableau (jalon, date, livrables, responsable) | MANAGER |
| Matrice des risques planning | Tableau (risque, impact, proba, mitigation) | MANAGER |
| Critères go/no-go | Checklist par jalon | MANAGER |

---

## Conditions d'arrêt
- Maximum 2 tours de débat Actor/Critic
- Si score de confiance CRITIQUE < 3 : revoir le scope ou les échéances
- Le planning doit inclure au minimum 20% de buffer pour les imprévus

---

## Template de backlog

| ID | Item | Description | Priorité | Complexité | Dépendances | Responsable | Jalon |
|----|------|-------------|----------|------------|-------------|-------------|-------|
| 1 | ... | ... | Must | M | - | ... | MVP |
| 2 | ... | ... | Should | L | 1 | ... | V1 |

---

## Template de planning jalons

| Jalon | Date | Livrables | Critères go/no-go | Risques |
|-------|------|-----------|-------------------|---------|
| MVP | Sxx | Liste... | Checklist... | Liste... |
| V1 | Sxx | Liste... | Checklist... | Liste... |

---

## Règles de priorisation

1. **Impact MTTR > Effort** : Prioriser les items à fort impact sur l'objectif principal
2. **Risques techniques d'abord** : Dérisquer tôt les items incertains
3. **Dépendances bloquantes d'abord** : Débloquer les items dépendants
4. **MVP minimal** : Résister à la tentation d'ajouter du "nice-to-have" au MVP
5. **Buffer obligatoire** : 20% minimum pour les imprévus
