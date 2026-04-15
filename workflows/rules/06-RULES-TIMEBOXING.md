# RULES-TIMEBOXING

## Principe

Le timeboxing impose des limites de temps strictes à chaque étape d'un workflow pour éviter les discussions infinies et garantir la productivité des débats.

---

## Durées par défaut

### Étapes de workflow

| Étape | Durée par défaut | Maximum | Notes |
|-------|------------------|---------|-------|
| Cadrage MANAGER | 5 min | 10 min | Reformulation + sélection d'agents |
| Proposition initiale ACTOR | 10 min | 15 min | Première version complète |
| Critique CRITIC | 5 min | 10 min | Analyse + score + suggestions |
| Révision ACTOR | 5 min | 10 min | Intégration des critiques |
| Synthèse MANAGER | 10 min | 15 min | Consolidation finale |

### Workflows complets

| Workflow | Durée cible | Maximum absolu |
|----------|-------------|----------------|
| Brainstorm Idées | 30 min | 45 min |
| Design Architecture | 45 min | 60 min |
| Revue Sécurité | 30 min | 45 min |
| Planification Projet | 45 min | 60 min |
| Rétrospective | 30 min | 45 min |
| Résolution Conflit | 20 min | 30 min |
| Validation Livrable | 20 min | 30 min |

---

## Règles de timeboxing

### 1. Le temps est non-négociable
- Quand le temps est écoulé, l'étape se termine
- Pas de "encore 5 minutes"
- Le MANAGER est le gardien du temps

### 2. Qualité dans le temps imparti
- Mieux vaut une proposition incomplète à temps qu'une proposition parfaite en retard
- Les points non traités sont reportés, pas ignorés

### 3. Signaux temporels
Le MANAGER annonce :
- **Début** : "Étape X commence, durée : Y minutes"
- **Mi-temps** : "Il reste Z minutes"
- **Fin imminente** : "1 minute restante, concluez"
- **Fin** : "Temps écoulé, passons à l'étape suivante"

### 4. Dépassement exceptionnel
Un dépassement est autorisé uniquement si :
- Le MANAGER l'approuve explicitement
- La raison est documentée
- Le temps est pris sur le buffer, pas sur les étapes suivantes

---

## Buffer et imprévus

### Allocation du buffer

| Workflow | Durée active | Buffer | Total |
|----------|--------------|--------|-------|
| 30 min | 25 min | 5 min | 30 min |
| 45 min | 35 min | 10 min | 45 min |
| 60 min | 50 min | 10 min | 60 min |

### Utilisation du buffer
- Dépassement d'une étape critique
- Question imprévue nécessitant une clarification
- Problème technique (pas une excuse récurrente)

### Ce qui ne justifie PAS d'utiliser le buffer
- "Je n'ai pas fini ma réflexion"
- "Je veux ajouter un dernier point"
- "On n'a pas tout couvert"

---

## Adaptation du timeboxing

### Facteurs d'ajustement

| Facteur | Ajustement |
|---------|------------|
| Sujet complexe (architecture critique, sécurité) | +25% |
| Sujet simple (revue mineure, clarification) | -25% |
| Équipe nombreuse (> 4 agents) | +25% |
| Première utilisation du workflow | +50% (apprentissage) |
| Workflow rodé | -25% |

### Exemples

- Design Architecture complexe : 45 min × 1.25 = ~56 min → arrondir à 60 min
- Revue simple : 30 min × 0.75 = ~22 min → arrondir à 20 min

---

## Gestion des retards

### Si une étape dépasse son temps

1. **Stop immédiat** : Le MANAGER interrompt
2. **Sauvegarde de l'état** : Noter où on en est
3. **Choix** :
   - Option A : Utiliser le buffer pour terminer (si critique)
   - Option B : Passer à l'étape suivante avec l'état partiel
   - Option C : Reporter et planifier une nouvelle session

### Si le workflow complet dépasse son temps

1. **Pas de prolongation automatique**
2. **Synthèse partielle** : Le MANAGER produit une synthèse de ce qui a été couvert
3. **Documentation des points restants** : Liste explicite des sujets non traités
4. **Planification de suite** : Si nécessaire, nouvelle session planifiée

---

## Chronomètres et rappels

### Format des annonces

```
[TEMPS] Étape "Proposition initiale" - Début (10 min)
[TEMPS] Étape "Proposition initiale" - Mi-temps (5 min restantes)
[TEMPS] Étape "Proposition initiale" - Dernière minute
[TEMPS] Étape "Proposition initiale" - Terminée
```

### Indicateurs visuels (si interface le permet)

| Temps restant | Indicateur |
|---------------|------------|
| > 50% | Vert |
| 25-50% | Jaune |
| < 25% | Rouge |
| Dépassé | Rouge clignotant |

---

## Anti-patterns temporels

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Parkinsonnisme | Le travail s'étend pour remplir le temps | Fixer des durées courtes, itérer |
| Perfectionnisme | Ne jamais terminer | "Done is better than perfect" |
| Discussion tangente | Dévier du sujet | MANAGER recadre immédiatement |
| Attente passive | Un agent ne répond pas | Timeout + passage au suivant |
| Négociation de temps | "Encore 5 minutes" | Refuser systématiquement |

---

## Métriques temporelles

### À suivre

| Métrique | Cible | Alerte si |
|----------|-------|-----------|
| Respect du timebox | > 90% des étapes | < 80% |
| Utilisation du buffer | < 50% en moyenne | > 75% |
| Workflows terminés à temps | > 95% | < 90% |
| Temps moyen par workflow | ±10% de la cible | > 25% de déviation |

### Analyse

- Si les timeboxes sont systématiquement dépassés : les durées sont trop courtes → ajuster
- Si les timeboxes sont systématiquement sous-utilisés : les durées sont trop longues → ajuster
- Si un agent dépasse toujours : problème de cadrage ou de scope

---

## Exemple de planning minuté

### Workflow : Design Architecture (45 min)

| Temps | Étape | Durée |
|-------|-------|-------|
| 0:00 | Cadrage MANAGER | 5 min |
| 0:05 | Proposition ARCHITECTE | 10 min |
| 0:15 | Revue DEVOPS | 5 min |
| 0:20 | Revue SECURITE | 5 min |
| 0:25 | Critique CRITIC | 5 min |
| 0:30 | Révision ARCHITECTE | 5 min |
| 0:35 | Synthèse MANAGER | 10 min |
| 0:45 | **FIN** | - |

Buffer intégré : 5 min réparties sur les étapes flexibles (proposition, synthèse).
