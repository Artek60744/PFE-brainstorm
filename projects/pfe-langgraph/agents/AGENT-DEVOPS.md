# Agent : Expert DevOps / CI-CD 🟢

## Rôle
Définir les cas d'usage CI/CD, les scénarios d'incidents, l'intégration avec Azure DevOps et Digital.ai Release.

**Note** : OpenClaw remplacé par LangGraph + APScheduler (ADR-017, 2026-04-23)

---

## 1. Étapes du Projet

### Phase 0 — Cartographie des Pipelines (Semaines 1-2)
- Inventorier les pipelines Azure DevOps utilisés par Isagri
- **Cartographier les dépendances entre pipelines** (pipeline A déclenche pipeline B)
- Identifier les patterns d'échec les plus fréquents **par pipeline**
- Documenter le flux de release (ADO → Digital.ai Release)
- **Méthode de mesure MTTR manuelle** : impossible d'extraire depuis ADO → chronométrer 10-15 incidents manuellement

### Phase 1 — Détection d'Incidents (Semaines 3-5)
- Configurer le webhook ADO → FastAPI `/webhook/ado` (détection temps réel, ADR-018)
- Configurer APScheduler polling fallback ADO (15min, déduplication build_id, ADR-018)
- Configurer APScheduler polling adaptatif DAI (15s-10min, state SQLite, ADR-019)
- Définir les seuils d'alerte (échec critique vs warning)
- Implémenter la collecte des logs de build via MCP
- Implémenter le cache in-memory FastAPI (TTL 5s) pour le dashboard (ADR-020)
- Implémenter HTMX polling adaptatif + BroadcastChannel multi-tab (ADR-020)

### Phase 2 — Diagnostic Automatisé (Semaines 6-9)
- Classifier les types d'échecs : compilation, tests, déploiement, timeout, ressources
- **Corréler avec l'historique des erreurs du même pipeline** (mémoire par pipeline)
- **Prendre en compte les dépendances entre pipelines** dans le diagnostic
- Identifier les causes racines récurrentes (dépendance cassée, config manquante, etc.)
- Générer un résumé de diagnostic structuré
- **Contraintes système de diagnostic (ADR-009)** :
  - Le bot **NE PEUT PAS** relancer les builds
  - Notification Teams = diagnostic + lien bug pré-rempli
  - Debouncing : 1 notification / 30 min par signature d'erreur

### Phase 3 — Intégration Digital.ai Release (Semaines 10-13)
- Installer et configurer le serveur MCP officiel Digital.ai Release
- Tester les outils MCP disponibles (lecture releases, environnements, approbations)
- Surveiller les blocages de release (environnements indisponibles, approbations en attente)
- Générer des release notes contextuelles

### Phase 4 — Exécution & Correction (Semaines 14-17)
- ~~Relancer un pipeline après correction validée~~ **INTERDIT** : Le bot ne relance pas les builds
- Créer un Work Item ADO avec le diagnostic et le plan d'action (via wit_create_work_item)
- **Mode lien pré-rempli** : Le bot génère l'URL avec query params, l'humain crée le bug
- Ajouter un commentaire d'audit sur le ticket existant (via wit_add_work_item_comment)
- **Configurer webhook Teams** : MessageCard avec liens (Créer Bug, Voir Build)
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
| Notification Teams | Webhook entrant + MessageCard | Simple pour MVP, liens cliquables (pas de boutons interactifs) |
| Création de bug | Lien pré-rempli (pas création auto) | Humain garde le contrôle, valide avant création |
| Debouncing notifications | 1 notif / 30 min par signature | Évite la fatigue d'alertes |
| Assignation bug | Logique hiérarchique (Owner > Blame > Auteur) | Exclut les bots, fallback sur non-assigné |
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
| Webhook Teams | MessageCard avec liens (bug, build) | Semaine 6 |
| Template URL bug | Query params pré-remplis pour ADO | Semaine 6 |
| Module debouncing | 1 notif / 30 min par signature | Semaine 7 |
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
