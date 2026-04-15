# RULES-ESCALADE

## Principe

L'escalade est le mécanisme par lequel les agents remontent une décision ou un problème vers l'humain quand ils ne peuvent pas le résoudre seuls. Une escalade bien gérée évite les blocages tout en respectant l'autonomie des agents.

---

## Quand escalader

### Escalade obligatoire
Ces situations **doivent** toujours être escaladées :

| Situation | Raison |
|-----------|--------|
| Décision financière significative | L'agent n'a pas l'autorité budgétaire |
| Action en production sans dry-run possible | Risque irréversible |
| Conflit non résolu après WF-RESOLUTION-CONFLIT | Impasse avérée |
| Risque de sécurité P0 sans mitigation | Impact critique |
| Changement de scope majeur | Réalignement stratégique requis |
| Information manquante critique | Impossible de continuer sans |
| Doute éthique ou légal | Hors compétence de l'agent |

### Escalade recommandée
Ces situations **devraient** être escaladées sauf urgence :

| Situation | Raison |
|-----------|--------|
| Score CRITIQUE < 2 sur une décision clé | Confiance insuffisante |
| Dépassement de délai prévisible | Réajustement du planning |
| Découverte d'un risque non anticipé | Mise à jour de la stratégie |
| Besoin de validation externe | Approbation hors périmètre |

### Escalade optionnelle
Ces situations **peuvent** être escaladées selon le contexte :

| Situation | Raison |
|-----------|--------|
| Décision réversible à faible impact | Information de l'humain |
| Choix entre deux options équivalentes | Préférence humaine |
| Succès notable | Partage de bonne nouvelle |

---

## Qui escalade vers qui

```
┌─────────────────┐
│    HUMAIN       │  ← Décisions finales, arbitrages critiques
└────────┬────────┘
         │
┌────────▼────────┐
│  MANAGER-DEBAT  │  ← Escalades des agents, synthèses
└────────┬────────┘
         │
┌────────▼────────┐
│     AGENTS      │  ← Exécution, propositions
└─────────────────┘
```

- **Agent → Manager** : Pour demander un arbitrage entre agents
- **Manager → Humain** : Pour demander une décision stratégique ou un déblocage

---

## Comment escalader

### Format d'escalade standard

```markdown
## Escalade : [TITRE COURT]

### Niveau : [INFO / DÉCISION / BLOCAGE]

### Contexte
[2-3 phrases résumant la situation]

### Ce qui a été tenté
- [Action 1 et résultat]
- [Action 2 et résultat]

### Options identifiées
| Option | Avantages | Inconvénients | Recommandation agent |
|--------|-----------|---------------|---------------------|

### Décision demandée
[Question précise à l'humain]

### Urgence
[IMMÉDIATE / JOUR / SEMAINE]

### Impact si pas de réponse
[Ce qui se passe si l'humain ne répond pas]
```

### Niveaux d'escalade

| Niveau | Description | Action attendue |
|--------|-------------|-----------------|
| INFO | Information — pas de décision requise | Accusé de réception |
| DÉCISION | Choix requis parmi les options | Sélection d'une option |
| BLOCAGE | Impossible de continuer | Intervention humaine |

---

## Règles d'escalade

### 1. Escalader tôt plutôt que tard
- Ne pas attendre d'être bloqué pour escalader
- Une escalade INFO permet d'anticiper une future escalade DÉCISION

### 2. Toujours proposer des options
- Ne jamais escalader sans au moins 2 options
- Inclure une recommandation de l'agent

### 3. Documenter ce qui a été tenté
- L'humain doit comprendre pourquoi l'agent n'a pas pu résoudre seul
- Évite les allers-retours inutiles

### 4. Définir l'urgence honnêtement
- IMMÉDIATE : Blocage total, < 2 heures
- JOUR : Impact significatif si non traité dans 24h
- SEMAINE : Peut attendre sans impact majeur

### 5. Prévoir le fallback
- Que fait l'agent si l'humain ne répond pas ?
- Définir un timeout et une action par défaut

---

## Gestion du timeout

| Niveau | Timeout par défaut | Action si timeout |
|--------|-------------------|-------------------|
| INFO | Aucun | Continuer |
| DÉCISION | 24h | Rappel puis option par défaut |
| BLOCAGE | 4h | Rappel puis pause du workflow |

### Rappels
- Premier rappel : à 50% du timeout
- Deuxième rappel : à 90% du timeout
- Format : "[RAPPEL] Escalade en attente : [TITRE]"

---

## Anti-patterns d'escalade

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Sur-escalade | Tout remonter à l'humain | Définir clairement le périmètre d'autonomie |
| Sous-escalade | Ne jamais escalader, même bloqué | Rappeler que l'escalade est normale |
| Escalade vague | "J'ai un problème" sans contexte | Imposer le format standard |
| Escalade sans options | Demander à l'humain de tout résoudre | Toujours proposer 2+ options |
| Fausse urgence | Tout est IMMÉDIAT | Réserver IMMÉDIAT aux vrais blocages |
| Escalade punitive | Escalader pour se décharger | L'escalade n'est pas un échec |

---

## Métriques d'escalade

Pour évaluer la santé du processus d'escalade :

| Métrique | Cible | Alerte si |
|----------|-------|-----------|
| Taux d'escalade | 10-20% des décisions | > 30% ou < 5% |
| Temps de réponse humain | < 24h en moyenne | > 48h |
| Escalades résolues sans intervention | < 10% | > 20% (sur-escalade) |
| Escalades timeout | < 5% | > 10% |
