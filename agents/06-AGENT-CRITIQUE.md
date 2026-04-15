# Agent : Critique / Devil's Advocate

## Rôle
Attaquer les hypothèses faibles, identifier les angles morts, et challenger chaque décision.

---

## 1. Attaques des Hypothèses

### Hypothèse 1 : "OpenClaw est le bon choix"
**Attaque** : OpenClaw est un projet open-source jeune, potentiellement instable, mal documenté, avec une communauté limitée. Si le projet est abandonné ou change de licence, le PFE est bloqué.
**Contre-proposition** : ~~Prévoir un fallback sur LangChain + CrewAI (écosystème mature, documentation riche). Le POC OpenClaw doit être validé en semaine 1 avec un go/no-go clair.~~ **RÉSOLU** : OpenClaw validé par le tuteur. Le risque est assumé.

### Hypothèse 2 : "Le pattern RPAE réduit le MTTR"
**Attaque** : Le temps passé par l'humain à lire le plan, comprendre le diagnostic, et cliquer "Approuver" peut facilement annuler le gain de diagnostic automatisé. Un développeur expérimenté diagnostique un échec de build en 5-10 minutes. Si l'agent met 2 min (détection) + 3 min (diagnostic) + 10 min (humain lit et approuve) + 2 min (exécution) = 17 min, le gain est marginal.
**Contre-proposition** : Cibler les incidents complexes (multi-services, erreurs obscures) où le gain de diagnostic est significatif (> 20 min économisées). Mesurer le MTTR par type d'incident, pas en moyenne globale.

### Hypothèse 3 : "L'approbation humaine est un garde-fou suffisant"
**Attaque** : L'humain suffer de "automation bias" — il clique "Approuver" sans lire, surtout sous pression d'un incident prod. Le pattern RPAE devient alors un "Read-Execute" déguisé.
**Contre-proposition** : Implémenter un "cooling-off period" (délai de réflexion obligatoire de 30 secondes), un résumé en 3 lignes du risque, et un niveau 3 (double approbation) pour toute action en production.

### Hypothèse 4 : "MCP résout tous les problèmes d'intégration"
**Attaque** : Le serveur MCP Microsoft pour Azure DevOps est récent, potentiellement limité en actions d'écriture. Digital.ai Release n'a probablement pas de serveur MCP. Le POC risque de se retrouver bloqué à la phase Execute.
**Contre-proposition** : ~~Prévoir des Skills custom OpenClaw avec API REST native comme fallback.~~ **MIS À JOUR** : Le serveur MCP Digital.ai Release existe officiellement. Le serveur MCP Microsoft supporte l'écriture (wit_*). Reste à vérifier la compatibilité avec les champs personnalisés Isagri.

### Hypothèse 5 : "La base d'archive des erreurs apporte de la valeur"
**Attaque** : Une base d'erreurs historiques n'est utile que si les erreurs sont récurrentes et si le contexte est similaire. Dans un environnement CI/CD dynamique, les erreurs changent avec chaque commit.
**Contre-proposition** : ~~Commencer par une base de patterns d'erreurs (pas d'instances).~~ **MIS À JOUR** : La mémoire doit être **par pipeline** — une erreur sur le pipeline A n'a pas la même signification que sur le pipeline B. La corrélation par pipeline + dépendances entre pipelines est la bonne approche.

### Hypothèse 6 : "Le dashboard maintenu par l'agent est pertinent"
**Attaque** : Un dashboard maintenu par un agent IA est un gadget si l'information n'est pas actionnable. Les équipes DevOps ont déjà des dashboards (Azure DevOps, Grafana, Datadog).
**Contre-proposition** : ~~Le dashboard doit apporter une information unique : la corrélation entre erreurs actuelles et historiques.~~ **RÉSOLU** : Le dashboard est un **requirement du MVP** non reportable. Il doit afficher : pipelines en cours, erreurs par pipeline, contexte historique, dépendances entre pipelines. La valeur unique est la corrélation contextuelle.

---

## 2. Risques Non Couverts par les Autres Agents

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Le PFE devient un projet d'intégration technique sans valeur recherche | Haut | Moyen | Ancrer chaque décision dans la littérature, mesurer scientifiquement |
| Le jury considère le sujet "trop outil" et "pas assez ingénierie" | Haut | Moyen | Insister sur l'architecture, le pattern RPAE, la méthodologie d'évaluation |
| L'équipe Isagri change de priorité pendant le PFE | Moyen | Moyen | Sécuriser l'accès aux environnements de test dès le début |
| Le modèle LLM sous-jacent change de comportement (mise à jour) | Moyen | Moyen | Versionner le modèle utilisé, documenter les différences de comportement |
| Le sujet est "trop à la mode" et le jury est sceptique sur la profondeur | Moyen | Moyen | Ancrer dans des concepts fondamentaux (SRE, AIOps, automatisation), pas juste "IA cool" |

---

## 3. Questions Irrésolues à Challenger

1. **Pourquoi OpenClaw et pas un agent custom construit sur LangGraph ?** LangGraph offre un contrôle total sur le graphe RPAE, une communauté active, et une documentation solide. OpenClaw apporte-t-il vraiment une valeur différentiante suffisante pour justifier le risque ?

2. **Le heartbeat est-il vraiment nécessaire ?** Les webhooks ADO existent et sont plus efficaces pour la détection en temps réel. Le heartbeat ajoute de la complexité et du bruit potentiel.

3. **La réduction de 50% du MTTR est-elle réaliste ?** Sur des incidents simples, le gain est faible. Sur des incidents complexes, le gain est potentiellement élevé mais les cas sont rares. L'objectif devrait-il être différencié par type d'incident ? **MIS À JOUR** : Le tuteur confirme que 50% est ambitieux et probablement pas atteint, mais maintenu comme cible. Mesurer par type d'incident et analyser honnêtement.

4. ~~**Le dashboard n'est-il pas un scope creep ?**~~ **RÉSOLU** : Le dashboard est un requirement du MVP non reportable. Le risque est que sa complexité dépasse le temps disponible. Mitigation : scope strict (tableau + filtres + contexte par pipeline + dépendances).

5. **L'audit dans les Work Items ADO est-il suffisant ?** Que se passe-t-il si le Work Item est supprimé ou modifié ? Le journal local SQLite est-il une vraie solution ou un bricolage ?

6. **🔴 Pas de bac à sable — est-ce acceptable ?** Travailler en production dès le départ pour les tests d'écriture est un risque majeur. Un workitem mal créé, un commentaire inapproprié, ou une action non désirée aura un impact réel. Le dry-run mode est-il suffisant comme garde-fou ?

---

## 4. Recommandations du Critique

1. ~~**Go/No-Go OpenClaw en semaine 1**~~ **RÉSOLU** : OpenClaw validé par le tuteur.
2. **Mesurer par type d'incident** : Ne pas se fier à un MTTR moyen. Mesurer séparément : échecs de build simples, échecs de build complexes, blocages de release. Mesure manuelle requise (pas d'extraction ADO).
3. ~~**Supprimer le dashboard du MVP**~~ **RÉSOLU** : Dashboard obligatoire MVP. Scope strict : tableau + filtres + contexte par pipeline + dépendances.
4. **Implémenter le cooling-off period** : 30 secondes minimum avant approbation, avec résumé du risque.
5. **Documenter les échecs de l'agent** : Un agent qui rate un diagnostic ou propose une action incorrecte est une donnée de recherche précieuse. Ne pas les cacher.
6. **Mémoire par pipeline** : Corréler les erreurs par pipeline en priorité, puis globalement. Modéliser les dépendances entre pipelines.
7. **MTTR mesuré manuellement** : Combiner chronométrage manuel (10-15 incidents) + delta Work Items ADO pour deux sources croisées.
6. **Mémoire par pipeline** : Corréler les erreurs par pipeline en priorité, puis globalement. Modéliser les dépendances entre pipelines.
7. **MTTR mesuré manuellement** : Combiner chronométrage manuel (10-15 incidents) + delta Work Items ADO pour deux sources croisées.
