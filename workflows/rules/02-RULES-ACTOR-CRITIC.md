# RULES-ACTOR-CRITIC

## Principe

Le pattern **Actor-Critic** sépare les rôles pour améliorer la qualité des propositions :
- **ACTOR** : Agent producteur qui propose une solution
- **CRITIC** : Agent qui challenge la solution pour l'améliorer

Ce pattern s'inspire des systèmes de revue par les pairs et des techniques de débat adversarial.

---

## Règles fondamentales

### 1. Séquençage obligatoire
L'ACTOR produit **toujours** une proposition complète avant que le CRITIC intervienne.
- Pas d'interruption pendant la production
- Pas de critique prématurée sur des ébauches

### 2. Structure de la proposition ACTOR
Toute proposition doit contenir :
```
## Proposition
[Description structurée de la solution]

## Hypothèses
- [Hypothèse 1]
- [Hypothèse 2]

## Risques identifiés
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|

## Alternatives considérées
| Alternative | Raison du rejet |
|-------------|-----------------|

## Questions ouvertes
- [Question non résolue 1]
```

### 3. Structure de la critique CRITIC
Toute critique doit contenir :
```
## Évaluation globale
Score de confiance : X/5

## Points forts
- [Ce qui fonctionne bien]

## Hypothèses à challenger
| Hypothèse | Pourquoi elle est risquée | Alternative suggérée |
|-----------|---------------------------|----------------------|

## Risques non couverts
- [Risque manquant 1]

## Contre-propositions
- [Alternative concrète 1]

## Verdict
[Accepter / Réviser / Revoir entièrement]
```

### 4. Règles du CRITIC
Le CRITIC **doit** :
- Identifier les hypothèses implicites (non écrites)
- Lister les risques non mentionnés par l'ACTOR
- Proposer des alternatives concrètes (pas seulement critiquer)
- Attribuer un score de confiance honnête (1-5)
- Reconnaître les points forts (pas que du négatif)

Le CRITIC **ne doit pas** :
- Bloquer sans justification
- Critiquer sans proposer d'alternative
- Être systématiquement négatif
- Ignorer les contraintes mentionnées par l'ACTOR

### 5. Règles de la révision ACTOR
L'ACTOR révisé **doit** :
- Répondre explicitement à chaque critique :
  - Intégrer : "J'ai intégré ta critique sur X en modifiant Y"
  - Justifier le maintien : "J'ai lu ta critique sur X, mais je maintiens car Z"
- Améliorer le score de confiance si possible
- Ne pas ignorer silencieusement une critique

### 6. Nombre de tours
- **Par défaut : 2 tours** de révision
- Configurable par workflow (1 à 3 tours maximum)
- Au-delà de 3 tours : escalade obligatoire au MANAGER

### 7. Score de confiance

| Score | Signification | Action |
|-------|---------------|--------|
| 5/5 | Excellent — prêt pour implémentation | Valider |
| 4/5 | Bon — risques mineurs acceptables | Valider avec notes |
| 3/5 | Acceptable — risques à surveiller | Valider avec mitigations explicites |
| 2/5 | Insuffisant — révision nécessaire | Nouveau tour de révision |
| 1/5 | Rejet — revoir entièrement | Escalade au MANAGER |

### 8. Escalade
Si après le nombre maximum de tours le score CRITIC reste < 3 :
- Le MANAGER-DEBAT est notifié
- Un rapport des divergences est produit
- L'humain arbitre la décision finale

### 9. Le CRITIC ne bloque jamais
- Le CRITIC donne un avis, pas un veto
- Le MANAGER-DEBAT tranche toujours en dernier ressort
- Une proposition peut être validée malgré un score < 3 si le MANAGER le justifie

---

## Anti-patterns à éviter

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Critique vague | "C'est pas bien" sans explication | Exiger des critiques spécifiques et actionnables |
| Critique destructive | Que du négatif, pas d'alternative | Exiger une contre-proposition pour chaque critique majeure |
| Actor défensif | Ignore ou rejette toutes les critiques | Exiger une réponse explicite à chaque point |
| Boucle infinie | Tours de révision sans convergence | Limite stricte de tours + escalade |
| Critique complaisante | Score 5/5 systématique | Le CRITIC doit trouver au moins 1 point d'amélioration |

---

## Exemple de dialogue Actor-Critic

```
[ACTOR - ARCHITECTE]
## Proposition
Utiliser SQLite pour la base de données du POC.

## Hypothèses
- Le volume de données reste < 10 Go
- Un seul processus écrit à la fois

## Risques identifiés
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Concurrence d'écriture | Moyen | Faible | Mode WAL activé |

---

[CRITIC]
## Évaluation globale
Score de confiance : 3/5

## Points forts
- Simple à déployer et maintenir
- Adapté au contexte POC

## Hypothèses à challenger
| Hypothèse | Pourquoi elle est risquée | Alternative suggérée |
|-----------|---------------------------|----------------------|
| Un seul processus écrit | Le heartbeat + les actions peuvent écrire en parallèle | Prévoir un mutex ou passer à PostgreSQL |

## Risques non couverts
- Migration vers PostgreSQL en V2 peut être complexe si le schéma évolue

## Contre-propositions
- Commencer directement avec PostgreSQL (overhead acceptable)
- Ou : définir une interface d'abstraction pour faciliter la migration

## Verdict
Réviser — clarifier la stratégie de concurrence

---

[ACTOR - ARCHITECTE (révisé)]
## Proposition révisée
SQLite avec mode WAL + mutex applicatif pour les écritures concurrentes.
Interface Repository abstraite pour faciliter migration V2.

J'ai intégré ta critique sur la concurrence en ajoutant un mutex.
J'ai intégré ta critique sur la migration en définissant une interface abstraite.
```
