# Agent : Expert Sécurité / Gouvernance 🟢

## Rôle
Définir les garde-fous, la gestion des accès, l'audit, et la conformité du système RPAE.

---

## 1. Étapes du Projet

### Phase 0 — Politique de Sécurité (Semaines 1-2)
- Définir la matrice des permissions de l'agent (Read-Only par défaut)
- Identifier les secrets nécessaires (tokens ADO, credentials Digital.ai)
- Concevoir le modèle d'approbation humaine (qui peut approuver quoi)
- Documenter les risques de sécurité spécifiques aux agents IA

### Phase 1 — Gestion des Secrets (Semaines 3-4)
- Configurer l'authentification via le serveur MCP Microsoft
- Stocker les tokens dans Azure Key Vault ou variables sécurisées ADO
- Implémenter le rotation automatique des tokens
- Tester l'accès Read-Only sur un projet Isagri

### Phase 2 — Contrôles d'Approbation (Semaines 5-8)
- Implémenter le flux **Teams (canal dédié équipe DevOps)** avec boutons Approuver/Rejeter
- Restreindre l'approbation aux membres de l'équipe DevOps
- Définir les niveaux d'approbation :
  - Niveau 1 (automatique) : lecture de logs, création de ticket informatif
  - Niveau 2 (simple approval) : relance de pipeline, commentaire
  - Niveau 3 (double approval) : rollback, modification de config prod
- Implémenter le timeout d'approbation (30 min par défaut)

### Phase 3 — Audit & Traçabilité (Semaines 9-12)
- Implémenter le journal d'audit dans chaque Work Item ADO
- Format du commentaire d'audit : "Action X effectuée par OpenClaw, validée par [Nom] via [Canal] à [Timestamp]"
- Stocker un journal d'audit local (SQLite) pour analyse post-mortem
- Générer un rapport hebdomadaire des actions de l'agent

### Phase 4 — Hardening & Tests de Sécurité (Semaines 13-16)
- Tester les scénarios de rejection (agent propose une action dangereuse) en dry-run
- Tester le timeout d'approbation en dry-run
- ⚠️ Pas de bac à sable : tous les tests d'écriture doivent passer par le mode dry-run
- Vérifier qu'aucun secret n'est exposé dans les logs ou le dashboard
- Audit de code et de configuration
- Préparer le rollback plan pour les workitems de test créés en prod
- Préparer le rollback plan pour les workitems de test créés en prod
- Préparer le rollback plan pour les workitems de test créés en prod

### Phase 5 — Conformité & Documentation (Semaines 17-20)
- Documenter la politique de sécurité complète
- Préparer un dossier de conformité pour la soutenance
- Valider avec le tuteur que les garde-fous sont suffisants
- Rédiger la section sécurité du mémoire

---

## 2. Décisions Techniques Clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Permission par défaut | Read-Only | Principe du moindre privilège, écriture uniquement après approbation |
| Gestion des secrets | Serveur MCP Microsoft + Azure Key Vault | Délégation au standard MCP, pas de credentials en dur |
| Niveaux d'approbation | 3 niveaux (auto, simple, double) | Proportionnel au risque de l'action |
| Timeout d'approbation | 30 minutes | Suffisant pour une réponse humaine, pas trop long pour le MTTR |
| Journal d'audit | Double stockage (Work Item ADO + SQLite local) | Redondance pour la traçabilité et l'analyse post-mortem |

---

## 3. Risques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| L'agent exécute une action sans approbation | Critique | Faible | Pattern RPAE strict, tests de rejection, dry-run obligatoire |
| Token MCP compromis | Critique | Faible | Rotation automatique, scope minimal, monitoring d'usage |
| Approbation "trop rapide" (humain clique sans lire) | Haut | Moyen | Résumé obligatoire du plan, confirmation explicite, niveau 3 pour les actions critiques |
| Secrets exposés dans les logs du dashboard | Moyen | Moyen | Filtrage des logs, masking des tokens, revue de code |
| L'agent spamme les API (boucle incontrôlée) | Moyen | Moyen | Rate limiting, quota d'actions par heure, alerte si seuil dépassé |
| Non-conformité avec les politiques Isagri | Haut | Moyen | Validation précoce avec le tuteur et l'équipe sécurité |
| Écriture accidentelle en prod (pas de bac à sable) | Critique | Moyen | Mode dry-run par défaut, préfixe [OPENCLAW-TEST], validation tuteur obligatoire avant première écriture réelle |

---

## 4. Livrables

| Livrable | Description | Échéance |
|----------|-------------|----------|
| Politique de sécurité | Document des permissions, secrets, approbations | Semaine 2 |
| Configuration MCP sécurisée | Authentification fonctionnelle, Read-Only validé | Semaine 4 |
| Flux d'approbation 3 niveaux | Slack/Teams avec boutons et timeout | Semaine 8 |
| Journal d'audit | Implémentation double stockage (ADO + SQLite) | Semaine 12 |
| Rapport de tests de sécurité | Scénarios de rejection, timeout, exposition de secrets | Semaine 16 |
| Dossier de conformité | Document complet pour la soutenance | Semaine 20 |
| Section sécurité du mémoire | Rédaction complète | Semaine 24 |

---

## 5. Critères de Réussite

- [ ] Zéro action exécutée sans approbation humaine (sauf niveau 1 informatif)
- [ ] Aucun secret exposé dans les logs, le dashboard ou le code
- [ ] Le journal d'audit est complet et consultable pour chaque action
- [ ] Les 3 niveaux d'approbation sont fonctionnels et testés
- [ ] Le rate limiting empêche tout spam d'API
- [ ] Le dossier de conformité est validé par le tuteur
- [ ] La politique de sécurité est documentée et reproductible
