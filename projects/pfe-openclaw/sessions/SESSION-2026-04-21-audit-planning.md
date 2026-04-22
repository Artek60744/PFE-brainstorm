# Sessions OpenClaw Dashboard

Index des sessions de brainstorming et implémentation.

---

## Session 2026-04-21

**Sprint** : Planning Phase - MCP Integration (Next)
**Durée** : 30min planning

### Contexte
- Débat + ADRs terminés (010-015)
- Schemas BD + skeleton dashboard livrés
- MCP stubs placeholders à remplacer
- Clarifications nécessaires avant sprint 1

### Décisions prises
- ✅ Créer ROADMAP.md pour tracking
- ✅ Prioriser Sprint 1 (MCP Integration)
- ✅ Blocker majeur : accès MCP servers (Isagri infra)

### Prochaines étapes
- [ ] **Session 1 (Sprint 1A)** : DAI MCP client
  - Remplacer stub `dai_client.py`
  - Tests sur env staging
  - 2h estimé
  
- [ ] **Session 2 (Sprint 1B)** : ADO webhook + heartbeat
  - Implémenter `ado_webhook.py`
  - Fallback polling `ado_heartbeat.py`
  - Tests intégration
  - 2.5h estimé
  
- [ ] **Session 3 (Sprint 2)** : Diagnostic pipeline
  - Analyse séquentielle incidents
  - Extraction logs + correlation
  - 2h estimé

### Blockers
- 🔴 **MCP servers not accessible yet** - Attendre infra Isagri
- 🔴 **ADO webhook not configured** - Demander DevOps Isagri
- 🟡 **OpenClaw token (test)** - À générer avant Sprint 3

### Notes
- Caveman mode actif (réponses courtes)
- Français pour docs + commentaires
- Tous les fichiers référencent ADRs décisionnels
