# Structure des Templates d'Agents

Ce document définit la structure standard pour créer un agent. Tous les templates de ce dossier suivent cette structure.

---

## Structure Standard

```markdown
# Agent : [NOM]

## Rôle
[Description en 1-2 phrases du rôle de l'agent]

## Domaines d'expertise
- [Domaine 1]
- [Domaine 2]
- [Domaine 3]

## Quand cet agent intervient
- [Condition 1]
- [Condition 2]

## Instructions de débat

### Posture générale
[Comment l'agent se comporte dans un débat]

### Ce que l'agent doit toujours faire
1. [Instruction 1]
2. [Instruction 2]
3. [Instruction 3]

### Ce que l'agent ne doit jamais faire
1. [Anti-pattern 1]
2. [Anti-pattern 2]

## Questions types que l'agent pose
- "[Question 1]"
- "[Question 2]"
- "[Question 3]"

## Points de vigilance
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Format de sortie standard

### Proposition
[Structure type d'une proposition]

### Risques identifiés
| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|

### Recommandations
- [Recommandation 1]
- [Recommandation 2]

## Interactions avec les autres agents

| Agent | Type d'interaction | Fréquence |
|-------|-------------------|-----------|
| [Agent X] | [Collaboration/Challenge/Support] | [Toujours/Souvent/Parfois] |

## Métriques de succès
- [Métrique 1]
- [Métrique 2]
```

---

## Comment Créer un Nouvel Agent

### 1. Copier le template
Copier `TPL-TEMPLATE.md` (ce fichier) et renommer en `TPL-[NOM].md`

### 2. Définir le rôle
- Rôle clair et distinct des autres agents
- Pas de chevauchement avec un agent existant
- Si chevauchement, fusionner ou spécialiser

### 3. Définir les domaines d'expertise
- 3-5 domaines maximum
- Domaines concrets, pas abstraits
- Exemples : "CI/CD", "Tests automatisés", pas "Qualité"

### 4. Définir les triggers
- Quand cet agent doit-il être impliqué ?
- Règles claires pour le MANAGER-DEBAT

### 5. Rédiger les instructions
- Instructions actionnables
- Éviter le jargon
- Tester avec un exemple concret

### 6. Définir les questions types
- Questions que l'agent pose naturellement
- Révèlent la perspective unique de l'agent

### 7. Lister les points de vigilance
- Ce que l'agent vérifie systématiquement
- Checklist réutilisable

### 8. Définir le format de sortie
- Structure cohérente avec les autres agents
- Facilite la synthèse par le MANAGER

---

## Bonnes Pratiques

### Spécificité
- Un agent = une perspective unique
- Pas d'agent "généraliste" (sauf MANAGER)
- Mieux vaut 2 agents spécialisés qu'1 agent flou

### Complémentarité
- Les agents doivent se compléter, pas se concurrencer
- Chaque agent apporte quelque chose que les autres n'ont pas
- Vérifier l'absence de redondance

### Testabilité
- Un agent doit pouvoir être "joué" par un humain
- Les instructions doivent être assez claires pour ça
- Tester avec un scénario réel

### Évolutivité
- Le template peut être enrichi au fil du temps
- Documenter les évolutions dans un changelog
- Versionner les changements majeurs

---

## Templates Disponibles

| Template | Rôle | Type |
|----------|------|------|
| [TPL-ARCHITECTE](TPL-ARCHITECTE.md) | Architecture technique | Producteur |
| [TPL-DEVOPS](TPL-DEVOPS.md) | CI/CD, Infrastructure | Producteur |
| [TPL-PRODUCT-OWNER](TPL-PRODUCT-OWNER.md) | Valeur métier, Priorisation | Producteur |
| [TPL-TESTEUR-QA](TPL-TESTEUR-QA.md) | Qualité, Tests | Producteur |
| [TPL-SECOPS](TPL-SECOPS.md) | Sécurité opérationnelle | Producteur |
| [TPL-FINOPS](TPL-FINOPS.md) | Optimisation coûts | Producteur |
| [TPL-CHERCHEUR](TPL-CHERCHEUR.md) | Recherche, État de l'art | Producteur |
| [TPL-DATA-ENGINEER](TPL-DATA-ENGINEER.md) | Données, Pipelines data | Producteur |
| [TPL-CRITIQUE](TPL-CRITIQUE.md) | Challenge, Devil's advocate | Critique |
| [TPL-MANAGER-DEBAT](TPL-MANAGER-DEBAT.md) | Orchestration | Manager |

---

## Matrice des Perspectives

| Sujet | Architecte | DevOps | PO | QA | SecOps | FinOps |
|-------|------------|--------|----|----|--------|--------|
| Performance | X | X | | X | | |
| Coût | | X | | | | X |
| Sécurité | X | | | | X | |
| UX | | | X | X | | |
| Maintenabilité | X | X | | | | |
| Scalabilité | X | X | | | | X |
| Conformité | | | | | X | |
| Time-to-market | | X | X | | | |

Cette matrice aide à sélectionner les agents pertinents pour un sujet donné.
