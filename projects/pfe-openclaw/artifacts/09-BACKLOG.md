# Backlog MVP / V1 / V2

## Vue d'Ensemble

| Version | Scope | Échéance | Objectif |
|---------|-------|----------|----------|
| **MVP** | Cycle RPAE sur échecs de pipeline ADO + **Dashboard** | S15 | Prouver la faisabilité du pattern RPAE |
| **V1** | MVP + Digital.ai + Mesure MTTR manuelle | S20 | Système utilisable et mesuré |
| **V2** | V1 + capacités avancées + industrialisation | Post-PFE | Système industrialisable |

---

## MVP (Semaines 1-15) — POC

### Épique 1 : Read — Détection et Collecte
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| R1 | En tant que système, je détecte un échec de pipeline ADO via heartbeat | P0 | Détection en < 2 min après l'échec |
| R2 | En tant que système, je collecte les logs du pipeline échoué via MCP | P0 | Logs complets extraits et stockés |
| R3 | En tant que système, je collecte les Work Items liés au pipeline | P1 | Work Items associés identifiés |
| R4 | En tant que système, je collecte les PRs liées au pipeline | P1 | PRs associées identifiées |
| R5 | En tant que système, je stocke l'erreur dans la base d'archive SQLite **par pipeline** | P1 | Erreur queryable par pipeline_id, type et date |

### Épique 2 : Plan — Diagnostic
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| P1 | En tant que système, je classe l'erreur par type (compilation, tests, déploiement, timeout, ressources) | P0 | Classification correcte à 80%+ |
| P2 | En tant que système, j'identifie la cause racine probable | P0 | Cause racine identifiée et expliquée |
| P3 | En tant que système, je corrèle avec les erreurs historiques **du même pipeline** | P0 | Corrélation par pipeline affichée en priorité |
| P3b | En tant que système, je prends en compte les **dépendances entre pipelines** | P1 | Dépendances modélisées et utilisées dans le diagnostic |
| P4 | En tant que système, je génère un plan d'action structuré (Cause → Impact → Action → Risque) | P0 | Plan lisible et exploitable par un humain |
| P5 | En tant que système, je propose un correctif si le pattern d'erreur est connu | P2 | Correctif proposé pour les 3 patterns les plus fréquents

### Épique 3 : Approve — Validation Humaine
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| A1 | En tant que membre de l'équipe DevOps, je reçois une notification **Teams (canal dédié)** avec le diagnostic et le plan | P0 | Message reçu dans le canal Teams dédié en < 5 min après détection |
| A2 | En tant que membre de l'équipe DevOps, je peux approuver ou rejeter le plan via des boutons interactifs | P0 | Boutons fonctionnels, action déclenchée, accès restreint à l'équipe DevOps |
| A3 | En tant que système, j'applique un cooling-off period de 30 secondes avant de permettre l'approbation | P1 | Bouton désactivé pendant 30s |
| A4 | En tant que système, j'applique un timeout de 30 minutes si pas de réponse | P1 | Action annulée ou escaladée après 30 min |
| A5 | En tant que système, j'applique les 3 niveaux d'approbation selon le risque | P2 | Niveau 1 auto, Niveau 2 simple, Niveau 3 double |

### Épique 4 : Execute — Action
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| E0 | En tant que système, j'ai un mode dry-run qui logge l'action sans l'exécuter | P0 | Action loggée mais non exécutée en prod |
| E1 | En tant que système, je crée un Work Item ADO avec le diagnostic et le plan si approuvé | P0 | Work Item créé avec préfixe [OPENCLAW-TEST] — uniquement après validation tuteur |
| E2 | En tant que système, j'ajoute un commentaire d'audit sur le Work Item | P0 | Commentaire avec : action, validateur, timestamp |
| E3 | En tant que système, je stocke l'action dans le journal d'audit local SQLite | P1 | Action queryable dans le journal |
| E4 | En tant que système, je relance le pipeline si l'action approuvée est un retry | P2 | Pipeline relancé via MCP |

### Critères de Validation du MVP
- [ ] Cycle RPAE complet fonctionnel en dry-run (prod contrôlée après validation tuteur)
- [ ] Détection → Diagnostic → Approbation → Exécution (dry-run) en < 15 minutes
- [ ] Diagnostic correct à 80%+ sur les 3 types d'échecs les plus fréquents
- [ ] Corrélation par pipeline fonctionnelle (erreurs archivées et corrélées par pipeline_id)
- [ ] Zéro action exécutée sans approbation humaine (sauf niveau 1)
- [ ] Journal d'audit complet pour chaque action
- [ ] Mode dry-run fonctionnel et testé — aucune écriture en prod avant validation tuteur
- [ ] **Dashboard MVP fonctionnel** : pipelines en cours + erreurs par pipeline + contexte + dépendances
- [ ] Canal Teams dédié configuré et fonctionnel pour l'approbation
- [ ] **Dashboard MVP fonctionnel** : pipelines en cours + erreurs par pipeline + contexte + dépendances
- [ ] Canal Teams dédié configuré et fonctionnel pour l'approbation

---

## V1 (Semaines 16-20) — Prototype Utilisable

### Épique 5 : Digital.ai Release
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| D1 | En tant que système, je lis les statuts de release Digital.ai via le serveur MCP officiel | P0 | Statuts de release queryables |
| D2 | En tant que système, je détecte un blocage de release | P1 | Blocage détecté et notifié |
| D3 | En tant que système, je génère des release notes contextuelles | P1 | Release notes générées avec contexte |
| D4 | En tant que système, je propose un plan d'action pour un blocage de release | P2 | Plan d'action structuré et validable |

### Épique 6 : Dashboard — Améliorations Post-MVP
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| DS4 | En tant qu'utilisateur, je vois les métriques MTTR avant/après | P1 | Graphiques comparatifs |
| DS5 | En tant que système, le dashboard est maintenu automatiquement par l'agent | P1 | Données mises à jour sans intervention humaine |
| DS6 | En tant qu'utilisateur, je vois les dépendances entre pipelines sur le dashboard | P2 | Visualisation des dépendances |

### Épique 7 : Mesure et Optimisation
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| M1 | En tant que researcher, je mesure le MTTR **manuellement** (chronomètre + Work Items) sur 20+ incidents | P0 | Données collectées et analysées |
| M2 | En tant que researcher, je mesure le taux de justesse du diagnostic | P0 | Taux calculé et documenté |
| M3 | En tant que researcher, je collecte les retours qualitatifs des utilisateurs | P1 | Survey complétée par 5+ utilisateurs |
| M4 | En tant que système, je calibre les alertes pour limiter les faux positifs à < 3/jour | P1 | Faux positifs mesurés et réduits |
| M5 | En tant que système, j'optimise le moteur de diagnostic sur la base des retours | P2 | Justesse améliorée de 10%+ |

### Critères de Validation de V1
- [ ] Digital.ai Release intégré (au minimum en lecture via MCP officiel)
- [ ] Dashboard MVP amélioré avec métriques MTTR
- [ ] MTTR mesuré manuellement sur 20+ incidents
- [ ] Réduction du MTTR mesurée (objectif ambitieux 50%, analyse réaliste)
- [ ] Confiance de l'équipe > 3/5 (survey)

---

## V2 (Post-PFE) — Système Industrialisable

### Épique 8 : Capacités Avancées
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| V2-1 | En tant que système, je peux proposer un rollback automatique (avec approbation niveau 3) | P1 | Rollback proposé et exécutable |
| V2-2 | En tant que système, je peux scaler automatiquement une ressource (avec approbation) | P2 | Scaling proposé et exécutable |
| V2-3 | En tant que système, j'apprends des corrections validées pour améliorer mes futurs diagnostics | P1 | Base de patterns enrichie automatiquement |
| V2-4 | En tant que système, je peux corriger automatiquement les erreurs de dépendance connues | P2 | Correction appliquée après approbation |
| V2-5 | En tant que système, je génère des runbooks automatisés à partir des patterns appris | P2 | Runbooks consultables et exécutables |

### Épique 9 : Industrialisation
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| I1 | En tant qu'ops, je peux déployer l'agent via Infrastructure as Code | P1 | Deployment automatisé (Terraform/Ansible) |
| I2 | En tant qu'ops, je peux monitorer la santé de l'agent | P1 | Health checks, alerting, logs centralisés |
| I3 | En tant qu'admin, je peux configurer les permissions de l'agent via une politique | P1 | Politique RBAC configurée |
| I4 | En tant qu'admin, je peux auditer toutes les actions de l'agent via un SIEM | P2 | Logs exportés vers SIEM |
| I5 | En tant qu'ops, je peux configurer des connecteurs MCP pour d'autres outils CI/CD | P2 | Connecteurs GitLab CI, Jenkins, etc. |

### Épique 10 : Multi-Tenant & Gouvernance
| ID | User Story | Priorité | Critères d'Acceptation |
|----|-----------|----------|----------------------|
| G1 | En tant qu'admin, je peux gérer plusieurs agents pour plusieurs équipes | P1 | Isolation des contextes et permissions |
| G2 | En tant qu'admin, je peux définir des politiques d'approbation par équipe | P1 | Politiques configurables par équipe |
| G3 | En tant qu'admin, je peux générer des rapports de conformité | P2 | Rapports automatisés |
| G4 | En tant qu'admin, je peux désactiver l'agent globalement ou par équipe | P2 | Kill switch fonctionnel |

### Critères de Validation de V2
- [ ] Déploiement automatisé via IaC
- [ ] Monitoring et alerting de la santé de l'agent
- [ ] Multi-tenant avec isolation des contextes
- [ ] Connecteurs pour au moins 2 outils CI/CD supplémentaires
- [ ] Apprentissage continu des patterns d'erreurs
- [ ] Conformité SIEM et gouvernance entreprise

---

## Matrice de Priorisation (MoSCoW)

| Catégorie | MVP | V1 | V2 |
|-----------|-----|----|----|
| **Must Have** | R1, R2, R5, P1, P2, P3, P4, A1, A2, E0, E1, E2, **DS1, DS2, DS3** | M1, M2, D1 | I1, I2, I3 |
| **Should Have** | R3, R4, P3b, A3, A4, E3 | D2, D3, DS4, DS5, M3, M4 | V2-1, V2-3, G1, G2 |
| **Could Have** | P5, A5, E4 | DS6, M5 | V2-2, V2-4, V2-5, I4, I5, G3, G4 |
| **Won't Have** | — | — | — |
