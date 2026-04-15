# WF-VALIDATION-LIVRABLE

## Objectif
Effectuer une revue finale d'un document, code ou artefact avant soumission officielle. Produire :
- Une checklist de validation complétée
- Une liste des problèmes à corriger (bloquants et non-bloquants)
- Un verdict clair (Approuvé / À réviser / Rejeté)
- Une version annotée du livrable si nécessaire

---

## Agents impliqués
- **MANAGER-DEBAT** (orchestrateur)
- **Agent expert du domaine** (selon le type de livrable)
- **AGENT-CRITIQUE** (revue finale)
- **AGENT-PRODUIT** (si livrable orienté utilisateur)

---

## Types de livrables et agents associés

| Type de livrable | Agent lead | Agents support |
|------------------|------------|----------------|
| Architecture/Design | ARCHITECTE | DEVOPS, SECURITE |
| Code | DEVOPS | ARCHITECTE, SECURITE |
| Documentation | PRODUIT | ARCHITECTE |
| Plan de projet | PRODUIT | ARCHITECTE, DEVOPS |
| Rapport de sécurité | SECURITE | ARCHITECTE |
| Mémoire/Article | RECHERCHE | PRODUIT |

---

## Étapes

### 1. [MANAGER-DEBAT] Cadrage
- Identifie le type de livrable et sélectionne les agents
- Rappelle les critères de qualité attendus
- Définit le niveau de revue :
  - **Light** : Vérification rapide, focus sur les bloquants
  - **Standard** : Revue complète avec suggestions
  - **Deep** : Revue exhaustive, chaque détail compte
- Fixe la deadline de revue

### 2. [AGENT EXPERT] Revue technique
L'agent expert du domaine effectue une revue selon la checklist appropriée :

```
## Revue de [NOM DU LIVRABLE]

### Critères obligatoires (bloquants si KO)
- [ ] [Critère 1]
- [ ] [Critère 2]

### Critères recommandés (non-bloquants)
- [ ] [Critère 1]
- [ ] [Critère 2]

### Problèmes identifiés
| # | Type | Description | Localisation | Sévérité | Suggestion |
|---|------|-------------|--------------|----------|------------|

### Verdict intermédiaire
[OK / À corriger / Rejet]
```

### 3. [AGENT-CRITIQUE] Revue transverse
Le CRITIQUE vérifie les aspects non couverts par l'expert :
- Cohérence globale
- Clarté et lisibilité
- Complétude (rien n'est oublié)
- Alignement avec les objectifs initiaux
- Formatage et présentation

```
## Revue critique

### Points forts
- [...]

### Points à améliorer
| # | Aspect | Problème | Impact | Suggestion |
|---|--------|----------|--------|------------|

### Questions non résolues
- [...]

### Score de qualité : X/5
```

### 4. [MANAGER-DEBAT] Consolidation
- Fusionne les retours de l'expert et du CRITIQUE
- Classe les problèmes :
  - **P0 Bloquant** : Doit être corrigé avant soumission
  - **P1 Important** : Devrait être corrigé si possible
  - **P2 Mineur** : Nice-to-fix
  - **P3 Suggestion** : Pour amélioration future
- Rend le verdict final

### 5. [SI RÉVISION] Boucle de correction
- Le créateur du livrable corrige les P0 et P1
- Une revue rapide (Light) valide les corrections
- Maximum 2 boucles de correction

### 6. [MANAGER-DEBAT] Verdict final
```
## Verdict de validation

### Livrable : [NOM]
### Date : [DATE]
### Réviseurs : [LISTE]

### Statut : [APPROUVÉ / APPROUVÉ AVEC RÉSERVES / REJETÉ]

### Résumé
[2-3 phrases sur la qualité globale]

### Problèmes résiduels acceptés
| # | Problème | Justification de l'acceptation |
|---|----------|--------------------------------|

### Conditions de la validation
[Si APPROUVÉ AVEC RÉSERVES : conditions à respecter]

### Prochaines étapes
[Actions post-validation]
```

---

## Livrables attendus

| Livrable | Format | Responsable |
|----------|--------|-------------|
| Checklist complétée | Markdown | EXPERT |
| Liste des problèmes | Tableau priorisé | MANAGER |
| Revue critique | Analyse + score | CRITIQUE |
| Verdict final | Document signé | MANAGER |
| Version annotée (si rejet) | Livrable avec commentaires | EXPERT |

---

## Conditions d'arrêt
- Tout P0 non corrigé = rejet automatique
- Maximum 2 boucles de correction
- Après 2 rejets : escalade vers l'humain

---

## Checklists par type de livrable

### Checklist Document technique
- [ ] Titre clair et descriptif
- [ ] Objectif énoncé en introduction
- [ ] Structure logique (sections numérotées)
- [ ] Diagrammes lisibles et légendés
- [ ] Tableaux correctement formatés
- [ ] Pas de TODO ou placeholder restant
- [ ] Liens et références fonctionnels
- [ ] Orthographe et grammaire correctes
- [ ] Version et date indiquées

### Checklist Code
- [ ] Code compile/exécute sans erreur
- [ ] Tests passent (si applicables)
- [ ] Pas de secrets en dur
- [ ] Commentaires sur les parties complexes
- [ ] Nommage cohérent et lisible
- [ ] Pas de code mort ou commenté
- [ ] Dépendances documentées
- [ ] README à jour

### Checklist Architecture
- [ ] Diagrammes C4 complets et cohérents
- [ ] Tous les composants justifiés
- [ ] Interfaces clairement définies
- [ ] Risques documentés avec mitigations
- [ ] Décisions argumentées (ADR)
- [ ] Alignement avec les contraintes

### Checklist Plan de projet
- [ ] Objectifs SMART
- [ ] Backlog priorisé avec estimations
- [ ] Jalons avec dates et livrables
- [ ] Risques documentés
- [ ] Buffer de 20% minimum
- [ ] Responsables assignés

---

## Niveaux de sévérité

| Niveau | Description | Impact sur validation |
|--------|-------------|----------------------|
| P0 | Bloquant — erreur critique | Rejet si non corrigé |
| P1 | Important — problème significatif | Doit être corrigé ou justifié |
| P2 | Mineur — amélioration souhaitée | Peut être ignoré avec justification |
| P3 | Suggestion — pour le futur | Informatif uniquement |
