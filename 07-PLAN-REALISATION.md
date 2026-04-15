# Plan Détaillé de Réalisation — 6 Mois

## Vue d'Ensemble

| Phase | Semaines | Objectif | Statut |
|-------|----------|----------|--------|
| 0 — Setup & Découverte | S1-S3 | Environnement, baseline, état de l'art | ⬜ |
| 1 — Read (Lecture) | S4-S6 | Détection + collecte de contexte | ⬜ |
| 2 — Plan (Diagnostic) | S7-S9 | Moteur de diagnostic + archive erreurs | ⬜ |
| 3 — Approve (Validation) | S10-S12 | Flux d'approbation Teams (canal dédié DevOps) | ⬜ |
| 4 — Execute (Action) | S13-S15 | Cycle RPAE complet end-to-end + **Dashboard MVP** | ⬜ |
| 5 — Mesure & Itération | S16-S20 | **Mesure MTTR manuelle**, optimisation | ⬜ |
| 6 — Rédaction & Soutenance | S21-S26 | Mémoire, démo, présentation | ⬜ |

---

## Phase 0 — Setup & Découverte (Semaines 1-3)

### Semaine 1 : Environnement & Go/No-Go OpenClaw
- [ ] Installer OpenClaw sur une VM dédiée
- [ ] Connecter le serveur MCP Microsoft (Azure DevOps) — tokens disponibles ✅
- [ ] Tester la lecture seule sur un projet Isagri réel — accès autorisé ✅
- [ ] **Implémenter le mode dry-run** (P0 — pas de bac à sable, uniquement prod)
- [ ] **Go/No-Go OpenClaw** : si instable, basculer sur LangGraph/CrewAI
- [ ] Créer le repository Git du projet
- [ ] Commencer la bibliographie annotée
- [ ] Étudier la doc du serveur MCP Digital.ai Release

### Semaine 2 : Cartographie & Politique de Sécurité
- [ ] Inventorier les pipelines ADO utilisés par Isagri
- [ ] **Cartographier les dépendances entre pipelines** (pipeline A déclenche pipeline B)
- [ ] Identifier les 3 patterns d'échec les plus fréquents
- [ ] Définir la matrice des permissions de l'agent (Read-Only par défaut)
- [ ] Configurer l'authentification MCP sécurisée — tokens disponibles ✅
- [ ] **Établir la baseline MTTR manuellement** (impossible d'extraire depuis ADO) : chronométrer 10-15 incidents
- [ ] **Identifier un projet/area isolé en prod pour les tests d'écriture**
- [ ] **Documenter le rollback plan pour les workitems de test**

### Semaine 3 : État de l'Art & Discovery Produit
- [ ] Finaliser la bibliographie annotée (15+ références)
- [ ] Identifier les personas (SRE, devs, ops, release managers)
- [ ] Cartographier le workflow actuel de résolution d'incidents
- [ ] Rédiger les user stories du MVP (incluant **dashboard obligatoire**)
- [ ] Valider le scope et la méthodologie avec le tuteur

**Jalon Phase 0** : Environnement fonctionnel, baseline MTTR établie (manuelle), scope MVP validé (dashboard inclus)

---

## Phase 1 — Read (Lecture) (Semaines 4-6)

### Semaine 4 : Architecture & Détection
- [ ] Documenter l'architecture cible (diagrammes C4)
- [ ] Configurer le heartbeat OpenClaw pour interroger les pipelines ADO
- [ ] Optionnel : configurer un webhook ADO → OpenClaw
- [ ] Implémenter la lecture des logs de build via MCP

### Semaine 5 : Collecte de Contexte
- [ ] Implémenter la lecture des Work Items via MCP
- [ ] Implémenter la lecture des Pull Requests via MCP
- [ ] Définir les seuils d'alerte (échec critique vs warning)
- [ ] Tester la détection sur des échecs de pipeline réels

### Semaine 6 : Base d'Archive des Erreurs
- [ ] Créer la base de données SQLite pour l'archive des erreurs **par pipeline** (pipeline_id + erreur + contexte + résolution)
- [ ] Implémenter l'ingestion des erreurs détectées
- [ ] Tester la corrélation avec les erreurs historiques **du même pipeline**
- [ ] **POC Read validé** : l'agent détecte et collecte le contexte d'un échec

**Jalon Phase 1** : POC Read fonctionnel — l'agent détecte un échec de pipeline et collecte logs, Work Items, PRs, archive par pipeline

---

## Phase 2 — Plan (Diagnostic) (Semaines 7-9)

### Semaine 7 : Moteur de Diagnostic
- [ ] Classifier les types d'échecs : compilation, tests, déploiement, timeout, ressources
- [ ] Implémenter l'analyse des logs par le LLM (extraction erreurs/warnings)
- [ ] **Corréler avec l'historique du même pipeline en priorité**
- [ ] Générer un résumé de diagnostic structuré
- [ ] Tester sur 5+ échecs de pipeline réels

### Semaine 8 : Corrélation Historique + UX d'Approbation
- [ ] Intégrer la mémoire persistante d'OpenClaw pour corréler avec l'historique **par pipeline**
- [ ] **Implémenter la logique de dépendance entre pipelines** (pipeline A → pipeline B)
- [ ] Concevoir le format du plan d'action (Cause → Impact → Action → Risque)
- [ ] Créer les mockups des messages **Teams (canal dédié DevOps)** interactifs
- [ ] Tester la lisibilité du diagnostic avec des utilisateurs cibles

### Semaine 9 : Génération de Plans d'Action
- [ ] Implémenter la génération de plans d'action structurés (format JSON)
- [ ] Intégrer les patterns d'erreurs connus (base de patterns **par pipeline**)
- [ ] Valider la qualité du diagnostic avec le tuteur (80%+ de justesse)
- [ ] **POC Plan validé** : l'agent génère un diagnostic correct et un plan d'action

**Jalon Phase 2** : Moteur de diagnostic fonctionnel — l'agent identifie la cause racine et propose un plan

---

## Phase 3 — Approve (Validation) (Semaines 10-12)

### Semaine 10 : Intégration Teams (Canal Dédié DevOps)
- [ ] Connecter OpenClaw au **canal Teams dédié de l'équipe DevOps**
- [ ] Implémenter l'envoi de messages avec le plan d'action
- [ ] Implémenter les boutons interactifs Approuver/Rejeter
- [ ] Restreindre l'approbation aux membres de l'équipe DevOps
- [ ] Tester le flux end-to-end (détection → message → bouton)

### Semaine 11 : Niveaux d'Approbation & Timeout
- [ ] Implémenter les 3 niveaux d'approbation :
  - Niveau 1 (automatique) : lecture, création de ticket informatif
  - Niveau 2 (simple) : relance de pipeline, commentaire
  - Niveau 3 (double) : rollback, modification de config prod
- [ ] Implémenter le timeout d'approbation (30 min)
- [ ] Implémenter le cooling-off period (30 secondes minimum)

### Semaine 12 : Journal d'Audit + **Dashboard MVP**
- [ ] Implémenter le commentaire d'audit dans les Work Items ADO
- [ ] Implémenter le journal d'audit local (SQLite)
- [ ] **Implémenter le dashboard MVP** : pipelines en cours + erreurs par pipeline + contexte + dépendances
- [ ] Tester les scénarios de rejection et de timeout
- [ ] **POC Approve validé** : le flux d'approbation fonctionne avec audit

**Jalon Phase 3** : Flux d'approbation Teams fonctionnel + Dashboard MVP — l'humain reçoit, valide ou rejette le plan, tout est audité

---

## Phase 4 — Execute (Action) (Semaines 13-15)

### Semaine 13 : Exécution via MCP + **Dashboard MVP Finalisation**
- [ ] **Go/No-Go écriture prod** — validation explicite du tuteur requise
- [ ] Implémenter l'exécution des actions validées via MCP
- [ ] Créer un Work Item ADO avec le diagnostic et le plan d'action (wit_create_work_item)
- [ ] ⚠️ Préfixe [OPENCLAW-TEST] obligatoire sur tous les workitems
- [ ] Tester en mode dry-run d'abord, puis en prod contrôlée après validation
- [ ] **Finaliser le dashboard MVP**

### Semaine 14 : Intégration Digital.ai Release (V1)
- [ ] Installer et configurer le serveur MCP officiel Digital.ai Release (doc officielle disponible ✅)
- [ ] Tester les outils MCP disponibles (lecture releases, environnements, approbations)
- [ ] Surveiller les blocages de release
- [ ] Tester la lecture des statuts de release

### Semaine 15 : Cycle RPAE Complet
- [ ] Tester le cycle complet RPAE end-to-end (dry-run puis prod contrôlée après validation tuteur)
- [ ] Mesurer le temps de chaque étape (Read, Plan, Approve, Execute)
- [ ] Corriger les bugs et optimiser les performances
- [ ] **Prototype V1 validé** : cycle RPAE complet fonctionnel + Dashboard MVP

**Jalon Phase 4** : Prototype V1 — cycle RPAE complet end-to-end en prod contrôlée + Dashboard MVP fonctionnel

---

## Phase 5 — Mesure & Itération (Semaines 16-20)

### Semaine 16 : Déploiement Périmètre Réel
- [ ] Déployer sur un périmètre réel (lecture seule + actions validées)
- [ ] **Commencer la collecte manuelle du MTTR** (chronomètre + Work Items ADO)
- [ ] Monitorer les faux positifs (objectif : < 3/jour)
- [ ] Commencer la rédaction du chapitre 4 (Mise en œuvre)

### Semaine 17 : Dashboard MVP — Déjà livré en Phase 4
- [ ] **Dashboard MVP déjà fonctionnel** — itérations sur les retours utilisateurs
- [ ] Intégrer les données : pipelines en cours, erreurs **par pipeline**, contexte historique, dépendances
- [ ] Tester l'UX avec les personas cibles
- [ ] Commencer la rédaction du chapitre 5 (Résultats)

### Semaine 18 : Mesure MTTR Manuelle & Retours Qualitatifs
- [ ] **Mesurer le MTTR manuellement** (chronomètre + delta Work Items ADO) — pas d'extraction automatique
- [ ] Collecter les retours qualitatifs des utilisateurs (survey)
- [ ] Calculer le ROI temps gagné
- [ ] Ajuster le calibrage des alertes

### Semaine 19 : Optimisation & Chapitre 6
- [ ] Optimiser le moteur de diagnostic (améliorer la justesse)
- [ ] Rédiger le chapitre 6 (Discussion et limites)
- [ ] Documenter les patterns d'échec les mieux traités
- [ ] Préparer le runbook automatisé

### Semaine 20 : Finalisation Technique
- [ ] Finaliser le rapport de mesure MTTR
- [ ] Finaliser le dossier de conformité sécurité
- [ ] Documenter les leçons apprises
- [ ] **Prototype V2 validé** : système mesuré et optimisé

**Jalon Phase 5** : Prototype V2 — système déployé, mesuré, optimisé, résultats documentés

---

## Phase 6 — Rédaction & Soutenance (Semaines 21-26)

### Semaine 21 : Rédaction — Introduction & Conclusion
- [ ] Rédiger l'introduction du mémoire
- [ ] Rédiger la conclusion
- [ ] Compiler la bibliographie finale
- [ ] Faire relire l'ensemble par le tuteur

### Semaine 22 : Rédaction — Révisions
- [ ] Intégrer les retours du tuteur
- [ ] Vérifier la conformité avec les normes UniLaSalle
- [ ] Préparer les annexes (code, configurations, captures)
- [ ] Finaliser le rapport de mesure MTTR

### Semaine 23 : Mémoire Final
- [ ] Version finale du mémoire prête pour dépôt
- [ ] Vérification anti-plagiat
- [ ] Dépôt du mémoire

### Semaine 24 : Préparation Soutenance
- [ ] Créer le support de présentation
- [ ] Préparer la démo live (scénario complet)
- [ ] Anticiper les questions du jury
- [ ] Répéter la présentation

### Semaine 25 : Répétition Générale
- [ ] Répétition avec le tuteur
- [ ] Ajuster la démo et la présentation
- [ ] Préparer les backups (vidéo de la démo)

### Semaine 26 : Soutenance
- [ ] Soutenance finale
- [ ] Archivage du code et de la documentation

**Jalon Phase 6** : Soutenance réussie, mémoire déposé, code archivé

---

## Résumé des Jalons

| Jalon | Semaine | Critère de Validation |
|-------|---------|----------------------|
| Go/No-Go OpenClaw | S1 | OpenClaw stable sur VM, MCP connecté |
| Baseline MTTR (manuelle) | S2 | 10-15 incidents chronométrés + méthode de calcul |
| Scope MVP validé (dashboard inclus) | S3 | Validé par le tuteur |
| POC Read | S6 | Détection + collecte + archive par pipeline fonctionnelles |
| POC Plan | S9 | Diagnostic correct à 80%+ avec corrélation par pipeline |
| POC Approve + Dashboard MVP | S12 | Flux Teams + audit + dashboard fonctionnels |
| Prototype V1 | S15 | Cycle RPAE complet + Dashboard MVP en prod contrôlée |
| Prototype V2 | S20 | MTTR mesuré (manuel), système optimisé |
| Mémoire final | S23 | Déposé, conforme |
| Soutenance | S26 | Présentation + démo réussies |
