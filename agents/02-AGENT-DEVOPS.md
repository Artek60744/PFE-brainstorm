# Agent : Expert DevOps / CI-CD

## Rôle
Définir les cas d'usage CI/CD, les scénarios d'incidents, l'intégration avec Azure DevOps et Digital.ai Release.

---

## 1. Étapes du Projet

### Phase 0 — Cartographie des Pipelines (Semaines 1-2)
- Inventorier les pipelines Azure DevOps utilisés par Isagri
- **Cartographier les dépendances entre pipelines** (pipeline A déclenche pipeline B)
- Identifier les patterns d'échec les plus fréquents **par pipeline**
- Documenter le flux de release (ADO → Digital.ai Release)
- **Méthode de mesure MTTR manuelle** : impossible d'extraire depuis ADO → chronométrer 10-15 incidents manuellement

### Phase 1 — Détection d'Incidents (Semaines 3-5)
- Configurer le heartbeat OpenClaw pour scraper les statuts de pipelines
- Optionnel : configurer un webhook ADO → OpenClaw pour du temps réel
- Définir les seuils d'alerte (échec critique vs warning)
- Implémenter la collecte des logs de build

### Phase 2 — Diagnostic Automatisé (Semaines 6-9)
- Classifier les types d'échecs : compilation, tests, déploiement, timeout, ressources
- **Corréler avec l'historique des erreurs du même pipeline** (mémoire par pipeline)
- **Prendre en compte les dépendances entre pipelines** dans le diagnostic
- Identifier les causes racines récurrentes (dépendance cassée, config manquante, etc.)
- Générer un résumé de diagnostic structuré

### Phase 3 — Intégration Digital.ai Release (Semaines 10-13)
- Installer et configurer le serveur MCP officiel Digital.ai Release
- Tester les outils MCP disponibles (lecture releases, environnements, approbations)
- Surveiller les blocages de release (environnements indisponibles, approbations en attente)
- Générer des release notes contextuelles

### Phase 4 — Exécution & Correction (Semaines 14-17)
- Relancer un pipeline après correction validée
- Créer un Work Item ADO avec le diagnostic et le plan d'action (via wit_create_work_item)
- Ajouter un commentaire d'audit sur le ticket existant (via wit_add_work_item_comment)
- ⚠️ Pas de bac à sable : mode dry-run obligatoire jusqu'à validation tuteur fin phase 1
- Tester avec préfixe [OPENCLAW-TEST] sur un projet/area isolé en prod

### Phase 5 — Mesure & Optimisation (Semaines 18-22)
- **Mesurer le MTTR manuellement** (chronomètre + Work Items ADO) — pas d'extraction automatique depuis ADO
- Combiner échantillon manuel (10-15 incidents chronométrés) + delta Work Items (création → résolution)
- Identifier les gains par type d'incident **et par pipeline**
- Optimiser le calibrage des alertes
- Documenter les patterns d'échec les mieux traités

---

## 2. Décisions Techniques Clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Détection d'incidents | Heartbeat + Webhook (hybride) | Heartbeat pour la couverture, webhook pour la réactivité |
| Classification des erreurs | LLM + règles heuristiques | LLM pour les cas complexes, règles pour les patterns connus |
| Priorisation des incidents | Basée sur l'impact (prod > staging > dev) | Aligné sur la réduction du MTTR des incidents critiques |
| Environnement de test | Production uniquement avec dry-run | Pas de bac à sable disponible — mode simulation obligatoire |
| Données de production | Lecture seule sur projets Isagri réels | Authentique mais sans risque de modification |

---

## 3. Risques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Pipelines ADO trop hétérogènes pour un diagnostic générique | Haut | Moyen | Commencer par les 3 types d'échecs les plus fréquents |
| Digital.ai Release sans API documentée | Moyen | Moyen | Contacter le support Digital.ai, prévoir un fallback manuel |
| Logs de build trop volumineux pour le contexte LLM | Moyen | Haut | Pré-filtrer les logs (extraire uniquement les erreurs/warnings) |
| MTTR baseline difficile à extraire d'ADO | Moyen | Haut | Utiliser les métriques ADO + estimation manuelle si nécessaire |
| L'agent rate des incidents silencieux (pas d'échec explicite) | Moyen | Moyen | Ajouter des checks de santé post-déploiement |

---

## 4. Livrables

| Livrable | Description | Échéance |
|----------|-------------|----------|
| Cartographie des pipelines | Document des pipelines Isagri + patterns d'échec | Semaine 2 |
| Baseline MTTR | Métriques actuelles extraites d'ADO | Semaine 3 |
| Module de détection | Heartbeat + webhook configurés | Semaine 5 |
| Classifieur d'erreurs | Diagnostic automatisé par type d'incident | Semaine 9 |
| Intégration Digital.ai | Skill ou connecteur MCP fonctionnel | Semaine 13 |
| Module d'exécution | Création de tickets + commentaires d'audit | Semaine 17 |
| Rapport de mesure MTTR | Comparatif avant/après avec graphiques | Semaine 22 |
| Runbook automatisé | Documentation des patterns de correction | Semaine 24 |

---

## 5. Critères de Réussite

- [ ] L'agent détecte 100% des échecs de pipeline sur le périmètre testé
- [ ] Le diagnostic est correct (validé par un humain) dans 80%+ des cas
- [ ] Le MTTR moyen est réduit d'au moins 50% sur les incidents de type "échec de build"
- [ ] L'intégration Digital.ai Release est fonctionnelle (au minimum en lecture)
- [ ] L'agent peut créer un Work Item ADO avec diagnostic complet en < 2 minutes
- [ ] Le runbook automatisé couvre au moins 5 patterns d'échec courants
- [ ] Zéro incident causé par une action non validée de l'agent
