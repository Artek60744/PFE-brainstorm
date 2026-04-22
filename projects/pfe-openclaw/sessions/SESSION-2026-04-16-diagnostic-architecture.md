# Session : Architecture du Système de Diagnostic

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-04-16 |
| **Workflow** | WF-DESIGN-ARCHI |
| **Durée** | ~45 min |
| **Participants** | ARCHITECTE, DEVOPS, RECHERCHE, CRITIQUE |
| **Statut** | Validé |

## Sujet

Conception du système de diagnostic des erreurs de pipeline avec les contraintes suivantes :
- Le bot **n'a PAS le droit de relancer les builds**
- Action : notification Teams avec diagnostic complet
- Proposition de création de bug ADO avec formulation IA optimisée

## Questions traitées

1. **Process** : Quel workflow de diagnostic ?
2. **Logique** : Comment classifier et analyser les erreurs ?
3. **Mémoire** : Comment stocker et exploiter l'historique ?
4. **Apprentissage** : Comment affiner l'analyse au fil du temps ?

## Déroulement

### Phase 1 : Proposition initiale (ARCHITECTE)
- Architecture en 4 phases : Détection → Analyse → Formulation → Notification
- Schéma DB avec 4 tables (error_patterns, pipeline_errors, diagnostic_feedback, pipeline_dependencies)
- Message Teams avec boutons interactifs
- Score de confiance affiché

### Phase 2 : Revue opérationnelle (DEVOPS)
- Validation faisabilité MCP (reads OK, Teams webhook nécessaire)
- Catégories d'erreurs CI/CD : compilation, test, package, deployment, timeout, resource
- Options Teams : webhook simple vs Bot Framework vs Power Automate
- Complexité opérationnelle : 3/5

### Phase 3 : Apport recherche (RECHERCHE)
- Patterns d'apprentissage : RAG-like, Pattern Mining, Feedback Loop
- Métriques de qualité : précision > 80%, utilité > 70%
- Recommandation : feedback binaire pour MVP, embeddings en V2

### Phase 4 : Challenge (CRITIQUE)
**Score initial : 3/5**

Critiques soulevées :
1. Schéma DB trop complexe pour POC
2. Bouton "Créer Bug" ambigu (auto vs draft ?)
3. Score confiance arbitraire
4. Intégration Teams sous-estimée
5. Risque de notification fatigue
6. Assignation "dernier auteur" simpliste

### Phase 5 : Révision (ARCHITECTE)
Ajustements :
- Schéma simplifié à 1 table (`diagnostic_log`)
- Bouton = lien pré-rempli (pas création auto)
- Score masqué à l'utilisateur
- Webhook simple + liens pour MVP
- Debouncing 30 min ajouté
- Logique d'assignation hiérarchique

### Phase 6 : Évaluation finale (CRITIQUE)
**Score final : 4/5** ✅

## Décisions prises

| # | Décision | Détail |
|---|----------|--------|
| 1 | Schéma DB MVP | 1 table `diagnostic_log`, normalisation V2 |
| 2 | Flux bug | Lien pré-rempli, humain crée le bug |
| 3 | Score confiance | Usage interne uniquement |
| 4 | Teams MVP | Webhook + MessageCard + liens |
| 5 | Debouncing | 1 notif / 30 min par signature |
| 6 | Assignation | Owner > Blame > Auteur > Non assigné |

## Livrables produits

| Livrable | Chemin |
|----------|--------|
| ADR-009 | `decisions/ADR-009-systeme-diagnostic.md` |
| Session | `sessions/2026-04-16-diagnostic-architecture.md` |

## Actions suivantes

| Action | Responsable | Échéance |
|--------|-------------|----------|
| Créer schéma SQLite `diagnostic_log` | ARCHITECTE | Semaine 4 |
| Implémenter Collector (MCP reads) | DEVOPS | Semaine 5 |
| Développer Analyzer (prompt LLM) | ARCHITECTE | Semaine 6 |
| Configurer webhook Teams | DEVOPS | Semaine 6 |
| Créer template URL bug pré-rempli | DEVOPS | Semaine 6 |
| Tester debouncing sur données réelles | DEVOPS | Semaine 7 |

## Points ouverts (V2)

- [ ] Migration vers Adaptive Cards (boutons interactifs Teams)
- [ ] Embeddings vectoriels pour recherche sémantique
- [ ] Normalisation schéma DB (patterns, dépendances)
- [ ] Calibration du debouncing sur données réelles

## Diagramme final

```
   Heartbeat (2 min)
         │
         ▼
┌─────────────────┐
│ Pipeline échoué │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Collecter logs  │────▶│ Debouncing      │──── Si récent ───▶ Incrémenter compteur
│ + contexte      │     │ (30 min window) │
└─────────────────┘     └────────┬────────┘
                                 │ Si nouveau
                                 ▼
                        ┌─────────────────┐
                        │ Analyser erreur │
                        │ (LLM + histo)   │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Générer message │
                        │ Teams + lien    │
                        │ bug pré-rempli  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Webhook Teams   │
                        │ (MessageCard)   │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Enregistrer     │
                        │ diagnostic_log  │
                        └─────────────────┘
```

## Références

- Workflow utilisé : `core/workflows/WF-DESIGN-ARCHI.md`
- ADR produit : `decisions/ADR-009-systeme-diagnostic.md`
- ADR connexes : ADR-004 (Teams), ADR-006 (Mémoire pipeline)
