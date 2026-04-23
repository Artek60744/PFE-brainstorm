# Questions Ouvertes à Valider avec le Tuteur

## Catégorie 1 : Scope et Objectifs

| # | Question | Contexte | Impact si non résolu |
|---|----------|----------|---------------------|
| Q1 | L'objectif de réduction de 50% du MTTR est-il réaliste pour le périmètre Isagri ? | Le critique souligne que le gain varie fortement par type d'incident | Risque de résultats non concluants |
| Q2 | Le périmètre MVP doit-il inclure Digital.ai Release ou se limiter à Azure DevOps ? | Digital.ai nécessite une Skill custom (pas de MCP officiel) | Impact sur la charge de travail du MVP |
| Q3 | Le dashboard est-il un requirement du MVP ou peut-il être reporté en V1 ? | Le critique le considère comme un scope creep | Risque de dérive du scope |
| Q4 | Quels sont les 3 types d'échecs de pipeline prioritaires pour Isagri ? | Nécessaire pour focaliser le moteur de diagnostic | Risque de diagnostic trop générique |

## Catégorie 2 : Environnement et Accès

| # | Question | Contexte | Impact si non résolu |
|---|----------|----------|---------------------|
| Q5 | Un environnement Azure DevOps "bac à sable" est-il disponible pour les tests d'écriture ? | Nécessaire pour tester le cycle RPAE complet | Bloquant pour les phases 4-5 |
| Q6 | L'accès en lecture seule à des projets Isagri réels est-il autorisé ? | Nécessaire pour affiner le diagnostic sur des données authentiques | Impact sur la qualité du POC |
| Q7 | Les tokens/credentials pour le serveur MCP Microsoft sont-ils disponibles ? | Nécessaire pour l'authentification ADO | Bloquant pour la phase 1 |
| Q8 | L'équipe Isagri est-elle disposée à participer aux tests qualitatifs (survey, retours) ? | Nécessaire pour la mesure qualitative | Impact sur la validité des résultats |

## Catégorie 3 : Sécurité et Gouvernance

| # | Question | Contexte | Impact si non résolu |
|---|----------|----------|---------------------|
| Q9 | La politique de sécurité Isagri autorise-t-elle un agent IA à interagir avec les pipelines ? | Risque de non-conformité | Bloquant pour le déploiement |
| Q10 | Qui sont les personnes autorisées à approuver les actions de l'agent ? | Nécessaire pour configurer les niveaux d'approbation | Impact sur le design du flux |
| Q11 | Azure Key Vault est-il disponible pour la gestion des secrets ? | Alternative aux variables sécurisées ADO | Impact sur l'architecture sécurité |
| Q12 | Faut-il un journal d'audit centralisé (SIEM) ou le journal ADO + SQLite suffit-il ? | Le critique souligne les limites du SQLite | Impact sur la traçabilité |

## Catégorie 4 : Méthodologie et Évaluation

| # | Question | Contexte | Impact si non résolu |
|---|----------|----------|---------------------|
| Q13 | Les métriques MTTR actuelles sont-elles extractibles d'Azure DevOps ? | Nécessaire pour la baseline | Risque de ne pas pouvoir mesurer le gain |
| Q14 | Quelle est la taille de l'échantillon d'incidents suffisante pour une mesure valide ? | Impact sur la durée de la phase de mesure | Risque de résultats non statistiquement significatifs |
| Q15 | Le format du mémoire est-il imposé par UniLaSalle (nombre de pages, plan, normes de citation) ? | Nécessaire pour la conformité | Risque de non-conformité |
| Q16 | L'évaluation doit-elle inclure un groupe témoin (sans agent) ou une comparaison avant/après suffit-elle ? | Impact sur la rigueur méthodologique | Risque de critique du jury sur la méthode |

## Catégorie 5 : Technique

| # | Question | Contexte | Impact si non résolu |
|---|----------|----------|---------------------|
| Q17 | OpenClaw est-il un choix validé par le tuteur ou faut-il prévoir un fallback ? | Le critique souligne les risques d'instabilité | Risque de blocage technique |
| Q18 | Le serveur MCP Microsoft pour Azure DevOps supporte-t-il les actions d'écriture ? | Nécessaire pour la phase Execute | Risque de devoir créer une Skill custom |
| Q19 | Slack ou Teams — quel canal est utilisé par l'équipe Isagri ? | Impact sur l'intégration d'approbation | Bloquant pour la phase 3 |
| Q20 | Existe-t-il une API documentée pour Digital.ai Release ? | Nécessaire pour la Skill custom | Impact sur l'intégration Digital.ai |

---

## Priorisation des Questions

### Urgent (à valider en Semaine 1)
- Q5, Q6, Q7 : Accès et environnement
- Q9 : Politique de sécurité
- Q17 : Validation du choix OpenClaw
- Q13 : Extractibilité des métriques MTTR

### Important (à valider en Semaine 2-3)
- Q1, Q2, Q3, Q4 : Scope et objectifs
- Q10, Q11, Q12 : Sécurité et gouvernance
- Q15, Q16 : Méthodologie
- Q18, Q19, Q20 : Technique

### Secondaire (à valider en Semaine 4-6)
- Q8 : Participation de l'équipe aux tests
- Q14 : Taille de l'échantillon

---

## Template de Suivi des Réponses

| Question | Réponse du Tuteur | Date | Décision Prise |
|----------|-------------------|------|----------------|
| Q1 | ⚠️ Objectif 50% ambitieux, probablement pas atteint mais maintenu comme cible | | Maintenir 50% comme objectif SMART, mais prévoir une analyse réaliste des résultats dans le mémoire |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | ❌ Pas de bac à sable disponible. Uniquement prod. Rédaction workitems = fin phase 1, extrême prudence. | | **IMPACT MAJEUR** — Voir 11-SYNTHESIS-CONTRAINTES.md |
| Q6 | ✅ Accès lecture seule autorisé sur projets Isagri réels | | Validé — POC Read sur données réelles |
| Q7 | ✅ Tokens/credentials MCP Microsoft disponibles | | Validé — Auth configurée |
| Q8 | | | |
| Q9 | ✅ Politique sécurité autorise agent IA en read-only sur les pipelines | | Validé — Écriture uniquement via RPAE avec approbation |
| Q10 | ✅ Membres de l'équipe DevOps via canal Teams dédié | | Canal Teams dédié à configurer pour l'approbation |
| Q11 | | | |
| Q12 | | | |
| Q13 | ❌ Métriques MTTR non extractibles d'Azure DevOps | | **IMPACT MAJEUR** — Voir alternative ci-dessous |
| Q14 | | | |
| Q15 | ✅ Format imposé UniLaSalle documenté dans `05-AGENT-RECHERCHE/contexte_PFE_unilasalle.md` | | Voir synthèse ci-dessous |
| Q16 | | | |
| Q17 | ✅ OpenClaw validé par le tuteur | | Choix technique confirmé — pas de fallback requis |
| Q18 | ✅ MCP Microsoft supporte l'écriture: wit_create_work_item, wit_update_work_item, wit_add_work_item_comment, wit_work_items_link. ⚠️ À vérifier: compatibilité avec champs personnalisés Isagri | | Validé partiellement — Test champs personnalisés requis |
| Q19 | | | |
| Q20 | ✅ Serveur MCP Digital.ai Release existe. Docs: https://docs.digital.ai/release/docs/how-to/release-mcp-server-installation | | Validé — Pas de Skill custom nécessaire |
