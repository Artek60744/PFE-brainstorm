# Agent : Architecte IA/Logiciel 🟢

## Rôle
Définir l'architecture technique, les composants, les interfaces et les patterns du système LangGraph + MCP.

**Note** : OpenClaw remplacé par LangGraph + APScheduler (ADR-017, 2026-04-23)

---

## 1. Étapes du Projet

### Phase 0 — Setup & Découverte (Semaines 1-3)
- Installer et configurer LangGraph dans le projet Python
- Configurer APScheduler pour le heartbeat
- Connecter le serveur MCP Microsoft (Azure DevOps)
- Valider la lecture seule sur un projet Isagri réel
- Documenter l'architecture cible (diagrammes C4)
- Implémenter le StateGraph RPAE (Read → Plan → Approve → Execute)
- Configurer SqliteSaver pour la mémoire persistante

### Phase 1 — Read (Semaines 4-6)
- Implémenter le webhook ADO (`POST /webhook/ado`) avec déduplication build_id (ADR-018)
- Configurer APScheduler polling fallback ADO (15min)
- Configurer APScheduler polling adaptatif DAI (15s-10min, state SQLite) (ADR-019)
- Implémenter le node "Read" du StateGraph : lecture des logs de build via MCP
- Implémenter la lecture des Work Items et PRs via MCP
- Créer la base de données d'archive des erreurs **par pipeline** (SQLite)
- Configurer SqliteSaver pour persister l'état du graph par incident
- Implémenter le cache in-memory FastAPI (TTL 5s) pour le dashboard (ADR-020)
- Implémenter HTMX polling adaptatif + BroadcastChannel multi-tab (ADR-020)
- Cartographier les dépendances entre pipelines

### Phase 2 — Plan (Semaines 7-9)
- Développer le moteur de diagnostic : analyse des logs → identification cause racine
- **Corrélation par pipeline en priorité** : l'historique du même pipeline prime sur l'historique global
- Intégrer la logique de dépendance entre pipelines (pipeline A → pipeline B)
- Générer des plans d'action structurés (format JSON exploitable par l'humain)
- Créer le dashboard de suivi (pipelines en cours + erreurs + contexte) — **MVP obligatoire**
- **Implémenter le système de diagnostic** (voir ADR-009) :
  - Flux 4 phases : Détection → Analyse → Formulation → Notification
  - Debouncing 30 min par signature d'erreur
  - Message Teams avec lien bug pré-rempli (pas de création auto)

### Phase 3 — Approve (Semaines 10-12)
- Intégrer le node "Approve" du StateGraph avec **Teams (canal dédié équipe DevOps)**
- Implémenter les boutons interactifs Approuver/Rejeter
- Restreindre l'approbation aux membres de l'équipe DevOps
- Concevoir le timeout d'approbation (si pas de réponse → escalade ou annulation)
- Implémenter le journal d'audit (qui, quand, quoi)

### Phase 4 — Execute (Semaines 13-15)
- Implémenter le mode dry-run (log sans exécution) — P0 absolu
- Implémenter l'exécution via MCP (création de tickets, commentaires d'audit)
- Ajouter la capacité de création de release notes automatisées
- ⚠️ Pas de bac à sable : exécution en prod uniquement après validation tuteur fin phase 1
- Préfixe [OPENCLAW-TEST] obligatoire sur tous les workitems de test
- Valider le cycle complet RPAE end-to-end (dry-run d'abord, puis prod contrôlée)

### Phase 5 — Industrialisation & Mesure (Semaines 16-20)
- Déployer sur un périmètre réel (lecture seule + actions validées)
- Mesurer le MTTR avant/après sur un échantillon d'incidents
- Itérer sur le calibrage des alertes (éviter l'alert fatigue)
- Documenter les leçons apprises

### Phase 6 — Rédaction & Soutenance (Semaines 21-26)
- Rédiger le mémoire
- Préparer la démo
- Finaliser les artefacts de soutenance

---

## 2. Décisions Techniques Clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Framework agent | LangGraph + APScheduler | StateGraph natif pour RPAE, persistance intégrée, MIT license, pas de risque politique |
| Heartbeat | APScheduler | Cron-like, léger, mature (2014+), remplace heartbeat natif OpenClaw |
| Mémoire persistante | LangGraph SqliteSaver → PostgresSaver | Persistance native de l'état du graph par incident |
| Protocole d'intégration | MCP (Model Context Protocol) | Standard émergent, serveur Microsoft officiel pour ADO, interopérabilité future |
| Base de données d'erreurs | SQLite (POC) → PostgreSQL (V2) — **mémoire par pipeline** | Erreurs stockées avec pipeline_id, contexte, dépendances. Corrélation par pipeline en priorité |
| Schéma diagnostic MVP | Table unique `diagnostic_log` | Simplifié pour MVP, normalisation V2. Voir ADR-009 |
| Notification Teams | Webhook + MessageCard + liens | Pas de Bot Framework pour MVP. Lien bug pré-rempli, pas création auto |
| Debouncing | 1 notification / 30 min par signature | Évite la notification fatigue |
| Canal d'approbation | Teams (canal dédié équipe DevOps) | Outil déjà utilisé, boutons interactifs natifs, accès restreint à l'équipe DevOps |
| Dashboard | Web app légère (FastAPI + HTMX) — **MVP obligatoire** | Maintenance par l'agent lui-même, requirement du MVP non reportable |
| Environnement de test | Production uniquement avec dry-run | Pas de bac à sable disponible — mode simulation obligatoire |
| Abandon d'OpenClaw | Justifié dans le mémoire (ADR-017) | Politique entreprise bloque OpenClaw/n8n ; LangGraph = alternative équivalente |

---

## 3. Risques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| LangGraph instable ou mal documenté | Haut | Faible | POC rapide en semaine 1, documentation LangChain excellente |
| Écriture en prod sans bac à sable | Critique | Certain | Mode dry-run obligatoire, préfixe [OPENCLAW-TEST], validation tuteur avant première écriture |
| Champs personnalisés Isagri incompatibles avec MCP | Moyen | Moyen | Tester wit_create_work_item avec champs custom en semaine 4, fallback API REST si nécessaire |
| Complexité du dashboard > temps disponible | Haut | Moyen | Dashboard MVP minimal (tableau + filtres + contexte erreurs par pipeline) — non reportable |
| Hallucination de l'agent sur le diagnostic | Haut | Moyen | Pattern RPAE strict + validation humaine obligatoire |
| Mémoire par pipeline trop complexe à implémenter | Moyen | Moyen | Commencer par corrélation simple (pipeline_id + erreur), ajouter dépendances progressivement |
| Qualité diagnostic LLM variable | Moyen | Moyen | Feedback loop (boutons utile/pas utile), affiner prompt en pilote |
| Notification fatigue | Moyen | Moyen | Debouncing 30 min, compteur d'occurrences |

---

## 4. Livrables

| Livrable | Description | Échéance |
|----------|-------------|----------|
| Architecture C4 | Diagrammes Context, Container, Component | Semaine 4 |
| POC LangGraph + MCP Read | StateGraph RPAE capable de lire logs, PRs, Work Items | Semaine 6 |
| Moteur de diagnostic | Analyse logs → cause racine + historique | Semaine 9 |
| Intégration Approve | Teams (canal dédié DevOps) avec boutons interactifs | Semaine 12 |
| Cycle RPAE complet | End-to-end en prod contrôlée (dry-run d'abord) | Semaine 15 |
| Dashboard MVP | Suivi pipelines + erreurs par pipeline + contexte — **obligatoire MVP** | Semaine 13 |
| Rapport de mesure MTTR | Avant/après sur échantillon | Semaine 22 |
| Code source | Repository documenté | Semaine 24 |

---

## 5. Critères de Réussite

- [ ] LangGraph détecte un échec de pipeline en < 2 minutes (APScheduler heartbeat)
- [ ] Le diagnostic est généré en < 5 minutes après détection
- [ ] Le plan d'action est compréhensible par un développeur non expert IA
- [ ] Le StateGraph RPAE complet s'exécute en < 15 minutes (détection → exécution validée)
- [ ] L'agent ne génère pas plus de 3 faux positifs par jour (alert fatigue)
- [ ] Le dashboard est fonctionnel et maintenu par l'agent
- [ ] L'architecture est documentée et reproductible
