# Synthèse des Contraintes Validées

## Réponses Reçues

| Question | Réponse | Impact |
|----------|---------|--------|
| Q1 | ⚠️ Objectif 50% ambitieux, probablement pas atteint mais maintenu comme cible | Maintenir comme objectif SMART, analyse réaliste dans le mémoire |
| Q2 | Se limiter à Azure DevOps pour MVP, Digital.ai en V1 | 🟡 Scope MVP réduit |
| Q3 | Dashboard = requirement MVP, pas reportable en V1 | 🔴 Scope MVP augmenté |
| Q4 | Mémoire d'erreur par pipeline + logique de dépendance à réfléchir | 🟡 Complexité diagnostic augmentée |
| Q5 | **Pas de bac à sable** — Uniquement prod. Rédaction workitems = fin phase 1, extrême prudence. | 🔴 CRITIQUE |
| Q6 | **Lecture seule autorisée** sur projets Isagri réels | 🟢 Validé |
| Q7 | **Tokens MCP Microsoft disponibles** | 🟢 Validé |
| Q9 | **Politique sécurité autorise agent IA en read-only** | 🟢 Validé |
| Q10 | **Approbation par équipe DevOps via canal Teams dédié** | 🟢 Validé |
| Q13 | **Métriques MTTR non extractibles d'ADO** | 🔴 CRITIQUE — Mesure manuelle requise |
| Q15 | ✅ Format imposé UniLaSalle documenté | 🟢 Validé |
| Q17 | ✅ OpenClaw validé par le tuteur | 🟢 Validé |
| Q18 | ✅ MCP Microsoft supporte l'écriture. ⚠️ Champs personnalisés à vérifier | 🟡 Partiel |
| Q20 | ✅ Serveur MCP Digital.ai Release existe | 🟢 Validé |

---

## 🔴 Contrainte Critique #1 : Pas de Bac à Sable (Q5)

### Conséquences
1. **Toute action d'écriture s'exécute en production** — risque réel de création de bruit dans les projets Isagri
2. **La phase Execute ne peut pas commencer avant la fin de la phase 1** — le Read doit être parfaitement validé avant toute écriture
3. **Les tests de rejection et de timeout doivent être simulés** — pas possible de tester sur des vrais workitems en prod avant validation

### Mitigations Obligatoires

| Mesure | Description | Priorité |
|--------|-------------|----------|
| **Dry-run mode** | L'agent doit avoir un mode "simulation" qui logge l'action sans l'exécuter | P0 — Semaine 1 |
| **Double validation humaine** | Avant toute première écriture en prod, validation explicite du tuteur | P0 — Fin phase 1 |
| **Projet prod isolé** | Identifier un projet/projet area dans prod où les workitems de test sont acceptables | P0 — Semaine 2 |
| **Préfixe de test** | Tous les workitems créés par l'agent doivent avoir un préfixe clair : "[OPENCLAW-TEST]" | P0 — Phase 4 |
| **Auto-close** | L'agent doit être capable de fermer automatiquement les workitems de test après validation | P1 — Phase 4 |
| **Rollback plan** | Documenter la procédure de suppression des workitems de test créés par erreur | P0 — Semaine 2 |

---

## 🔴 Contrainte Critique #2 : MTTR Non Extractible d'ADO (Q13)

### Conséquences
1. **Pas de baseline automatique** — impossible de calculer le MTTR historique depuis ADO
2. **Mesure manuelle requise** — le MTTR "avant" doit être estimé ou mesuré manuellement sur un échantillon
3. **Le MTTR "après" doit être mesuré manuellement** — chronométrer chaque incident traité par l'agent

### Méthode Alternative de Mesure

| Méthode | Description | Faisabilité |
|---------|-------------|-------------|
| **Estimation par l'équipe** | Demander aux devs/ops leur estimation du temps moyen de résolution actuel | Moyenne — subjectif mais rapide |
| **Échantillon manuel** | Chronométrer manuellement 10-15 incidents "avant" l'agent (période de 2-3 semaines) | Haute — objectif mais demande du temps |
| **Comparaison A/B** | Pendant la phase de mesure, traiter certains incidents avec l'agent et d'autres sans | Haute — rigoureux mais complexe à orchestrer |
| **Work Items ADO** | Calculer le delta entre date de création et date de résolution des Work Items | Moyenne — inclut le temps d'attente, pas juste l'analyse |

### Recommandation
Combiner **échantillon manuel** (10-15 incidents chronométrés) + **Work Items ADO** (delta création/résolution) pour avoir deux sources de données croisées.

### Impact sur le Planning

| Phase | Impact | Ajustement |
|-------|--------|------------|
| Phase 0 (S1-S3) | Ajouter la méthode de mesure manuelle du MTTR | +2 jours |
| Phase 1 (S4-S6) | Commencer la collecte manuelle du MTTR "avant" | Intégrer au workflow quotidien |
| Phase 5 (S16-S20) | Mesurer le MTTR "après" manuellement + Work Items | +1 semaine de collecte |

---

## 🟡 Contrainte Partielle : Champs Personnalisés Isagri (Q18)

### Question
Les outils MCP Microsoft (`wit_create_work_item`, etc.) supportent-ils les champs personnalisés utilisés par Isagri dans Azure DevOps ?

### Actions Requises
| Action | Échéance | Responsable |
|--------|----------|-------------|
| Inventorier les champs personnalisés des Work Items Isagri | Semaine 2 | DevOps |
| Tester `wit_create_work_item` avec un champ personnalisé (en dry-run) | Semaine 4 | Architecte |
| Si incompatible : prévoir fallback API REST ADO directe | Semaine 5 | Architecte |
| Documenter la compatibilité dans le mémoire | Chapitre 3 | Recherche |

---

## 🟡 Contrainte : Mémoire d'Erreur par Pipeline (Q4)

### Contexte
Les échecs dépendent du contexte de chaque pipeline. Une erreur sur le pipeline A n'a pas la même signification que la même erreur sur le pipeline B.

### Implications Techniques
- La base d'archive des erreurs doit stocker : **pipeline_id + erreur + contexte + résolution**
- Le moteur de diagnostic doit corréler avec l'historique **du même pipeline** en priorité
- La logique de dépendance entre pipelines doit être modélisée (pipeline A déclenche pipeline B)

### Actions Requises
| Action | Échéance | Responsable |
|--------|----------|-------------|
| Cartographier les pipelines et leurs dépendances | Semaine 2 | DevOps |
| Concevoir le schéma de la BDD d'erreurs (par pipeline) | Semaine 4 | Architecte |
| Implémenter la corrélation par pipeline dans le diagnostic | Semaine 7 | Architecte |
| Implémenter la logique de dépendance entre pipelines | Semaine 8 | Architecte |

---

## 🟢 Validations Positives

### OpenClaw Validé (Q17)
- Choix technique confirmé par le tuteur
- Pas de fallback requis
- Risque assumé — documenter dans le mémoire

### Format UniLaSalle Documenté (Q15)
- **60-80 pages hors annexes**
- **Arial 11 ou 12 pts, interligne simple**
- **Marges : 2,5 cm (gauche/droite), 3 cm (haut/bas)**
- **Pagination** : commence à l'introduction (page 4)
- **Remise** : 7 jours ouvrés avant soutenance
- **Soutenance** : 30 min + 10 min Q/R, dates 25/08/2025 – 05/09/2025
- **Structure** : 6 parties conformes (voir `08-STRUCTURE-MEMOIRE.md`)
- **Références** : format spécifique UniLaSalle (livre, article, rapport)
- **Panneau de synthèse** : PowerPoint, envoyé 1 semaine avant
- **Cahier des charges** : à produire et valider avant début dernière période
- **Revue de projet intermédiaire** : minimum une, semaine 13 cible
- **Contacts** : S. POMPORTES (responsable), S. GORGE (secrétariat)
- **Grille NAME** : positionner les compétences développées

### Politique Sécurité Validée (Q9)
- Agent IA autorisé en **read-only** sur les pipelines
- Écriture uniquement via pattern RPAE avec approbation humaine

### Canal d'Approbation : Teams Dédié (Q10)
- Canal Teams dédié à l'équipe DevOps
- Boutons interactifs Approuver/Rejeter dans ce canal
- Seuls les membres de l'équipe DevOps peuvent approuver

### Serveur MCP Digital.ai Release (Q20)
- **Documentation officielle disponible**
- Pas besoin de créer une Skill custom
- À intégrer en V1 (pas dans le MVP — voir Q2)

### Accès Lecture Seule Isagri (Q6)
- POC Read sur données réelles possible dès Semaine 4
- Authentique et valorisant pour la soutenance

### Tokens MCP Microsoft Disponibles (Q7)
- Authentification configurée dès Semaine 1
- Pas de délai d'attente côté infrastructure

### Objectif 50% MTTR Maintenu (Q1)
- Ambitieux, probablement pas atteint
- Maintenir comme cible SMART
- Analyser honnêtement les résultats dans le mémoire

---

## Questions Restantes (Non Répondues)

| Question | Priorité | Échéance de réponse |
|----------|----------|---------------------|
| Q8 — Équipe disposée pour tests qualitatifs ? | Moyenne | Semaine 4 |
| Q11 — Azure Key Vault disponible ? | Moyenne | Semaine 3 |
| Q12 — Journal d'audit centralisé ou SQLite suffit ? | Moyenne | Semaine 4 |
| Q14 — Taille échantillon incidents ? | Moyenne | Semaine 6 |
| Q16 — Groupe témoin ou avant/après ? | Moyenne | Semaine 6 |
| Q19 — Slack ou Teams pour l'équipe ? | ✅ Résolu (Teams) | — |
