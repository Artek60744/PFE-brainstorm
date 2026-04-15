# Cahier des Charges PFE — UniLaSalle

## À produire et valider avant le début de la dernière période

**Document à envoyer par mail commun à** :
- Tuteur entreprise
- Tuteur école (S. POMPORTES — stephane.pomportes@unilasalle.fr)
- Secrétariat apprentissage (S. GORGE — sandrine.gorge@unilasalle.fr)

---

## 1. Contexte et Enjeux

### Contexte
- **Étudiant** : [Nom Prénom]
- **Entreprise** : Isagri
- **Établissement** : UniLaSalle-Amiens (Programme RIOC / Apprentissage)
- **Période** : [Date début] — [Date fin]
- **Tuteur entreprise** : [Nom Prénom]
- **Tuteur école** : S. POMPORTES

### Enjeux stratégiques
- Réduire le MTTR (Mean Time To Resolution) des incidents DevOps
- Expérimenter l'usage d'un agent IA autonome avec validation humaine (pattern RPAE)
- Positionner Isagri sur l'innovation AIOps avec MCP comme standard d'intégration

### Positionnement politique et stratégique
- L'IA dans les opérations IT est un sujet émergent avec peu de retours d'expérience concrets
- Le Model Context Protocol (MCP) est un standard naissant qui pourrait devenir la norme d'intégration des agents IA
- Ce PFE produit un POC mesurable et documenté, valorisable pour Isagri et pour la recherche

---

## 2. Périmètre

### Personnes impactées
- Équipes DevOps Isagri (utilisateurs finaux de l'agent)
- Développeurs (bénéficiaires du diagnostic automatisé)
- Release managers (bénéficiaires de la surveillance des releases)
- SRE / Ops (premiers répondants aux incidents)

### Ressources impactées
- Azure DevOps (pipelines, work items, logs)
- Digital.ai Release (releases, environnements)
- **Teams (canal dédié équipe DevOps)** pour l'approbation
- VM dédiée pour OpenClaw

### Limites du périmètre
- **MVP** : Échecs de pipeline Azure DevOps uniquement + **Dashboard obligatoire**
- **V1** : Extension à Digital.ai Release + mesure MTTR manuelle
- **V2** : Capacités avancées (rollback, scaling, apprentissage continu)
- **Hors périmètre** : Monitoring applicatif, alerting infrastructure, correction automatique sans approbation

---

## 3. Problématique

**Dans quelle mesure un agent IA avec Read-Plan-Approve-Execute peut-il réduire le MTTR des incidents DevOps ?**

### Sous-questions
1. Le diagnostic automatisé par IA réduit-il le temps d'analyse primaire d'un incident ?
2. Le pattern RPAE (avec validation humaine) est-il un garde-fou suffisant pour un agent autonome ?
3. L'intégration via MCP est-elle un standard viable pour l'interopérabilité des agents IA DevOps ?

---

## 4. Objectifs SMART et Livrables

### Objectif Principal
**Réduire de 50% le temps humain passé sur l'analyse primaire d'un échec de pipeline** lors du prochain PI Planning.
> ⚠️ Objectif ambitieux, probablement pas atteint mais maintenu comme cible SMART. Analyse réaliste des résultats dans le mémoire.
> ⚠️ Objectif ambitieux, probablement pas atteint mais maintenu comme cible SMART. Analyse réaliste des résultats dans le mémoire.

### Objectifs Secondaires
| Objectif | Mesurable | Réaliste | Temporel |
|----------|-----------|----------|----------|
| Détecter un échec de pipeline en < 2 minutes | Oui, mesurable via logs | Oui, heartbeat OpenClaw | MVP (S15) |
| Générer un diagnostic correct à 80%+ | Oui, validé par humain | Oui, LLM + patterns connus | MVP (S15) |
| Cycle RPAE complet en < 15 minutes | Oui, mesurable | Oui, avec validation humaine | MVP (S15) |
| Limiter les faux positifs à < 3/jour | Oui, mesurable | Oui, calibrage des alertes | V1 (S20) |
| Mesurer le MTTR sur 20+ incidents | Oui, comptable | Oui, avec accès ADO | V1 (S20) |

### Livrables
| Livrable | Description | Date |
|----------|-------------|------|
| POC OpenClaw + MCP Read | Agent capable de lire logs, PRs, Work Items | S6 |
| Moteur de diagnostic | Analyse logs → cause racine + historique | S9 |
| Cycle RPAE complet | End-to-end sur Azure DevOps (dry-run puis prod) | S15 |
| Intégration Digital.ai Release | Serveur MCP officiel configuré | S15 |
| Dashboard MVP | Suivi pipelines + erreurs + contexte | S18 |
| Rapport de mesure MTTR | Avant/après sur échantillon | S22 |
| Mémoire PFE | 60-80 pages conforme UniLaSalle | J-7 ouvrés |
| Panneau de synthèse | PowerPoint conforme charte UniLaSalle | J-7 |
| Code source | Repository documenté | S24 |

---

## 5. Planning Prévisionnel

### Jalons
| Jalon | Semaine | Date Cible | Chemin Critique |
|-------|---------|------------|-----------------|
| Go/No-Go OpenClaw | S1 | | OUI |
| Baseline MTTR extraite | S2 | | OUI |
| Cahier des charges validé | S4 | | OUI |
| POC Read fonctionnel | S6 | | OUI |
| Diagnostic correct à 80%+ | S9 | | OUI |
| Approbation Slack/Teams fonctionnelle | S12 | | OUI |
| **Revue de projet intermédiaire** | S13 | | OUI (obligatoire UniLaSalle) |
| Cycle RPAE complet (Prototype V1) | S15 | | OUI |
| Dashboard fonctionnel | S18 | | NON |
| MTTR mesuré sur 20+ incidents (Prototype V2) | S20 | | OUI |
| Mémoire complet (version relecture) | S23 | | OUI |
| Remise au secrétariat | J-7 ouvrés | ~15/08/2025 | OUI |
| Soutenance | — | 25/08 – 05/09/2025 | OUI |

### Chemin Critique
```
S1: Go/No-Go OpenClaw
  → S2: Baseline MTTR
    → S4: Cahier des charges validé
      → S6: POC Read
        → S9: Diagnostic
          → S12: Approbation
            → S13: Revue intermédiaire
              → S15: Cycle RPAE complet
                → S20: Mesure MTTR
                  → S23: Mémoire complet
                    → J-7: Remise
                      → Soutenance
```

---

## 6. Méthodes

### Méthodologie de Développement
- **Pattern RPAE** (Read → Plan → Approve → Execute) avec validation humaine obligatoire
- **Mode dry-run** pour tous les tests d'écriture (pas de bac à sable disponible)
- **Itérations courtes** (1 semaine) avec démonstration au tuteur

### Méthodologie de Recherche
- **Étude de cas unique** avec mesure quantitative (MTTR) et qualitative (confiance)
- **Comparaison avant/après** sur un échantillon de 20+ incidents
- **Mesure MTTR manuelle** : chronométrage + delta Work Items ADO (pas d'extraction automatique depuis ADO)
- **Survey de confiance** auprès des utilisateurs (échelle 1-5)

### Outils
| Outil | Usage |
|-------|-------|
| OpenClaw | Agent IA persistant avec mémoire et heartbeat |
| MCP Microsoft | Intégration Azure DevOps |
| MCP Digital.ai Release | Intégration Digital.ai Release |
| Slack/Teams | Canal d'approbation humaine |
| SQLite | Base d'archive des erreurs + journal d'audit |
| Git | Versionnement du code |

---

## 7. Moyens

### Matériels
- VM dédiée pour OpenClaw (specs à définir)
- Accès réseau aux APIs Azure DevOps et Digital.ai Release

### Techniques
- Tokens/credentials MCP Microsoft (disponibles ✅)
- Accès lecture seule aux projets Isagri réels (autorisé ✅)
- Serveur MCP Digital.ai Release (documentation officielle disponible ✅)
- OpenClaw validé par le tuteur (✅)

### Humains
- Tuteur entreprise : [Nom Prénom] — [Email] — [Tél]
- Tuteur école : S. POMPORTES — stephane.pomportes@unilasalle.fr — 03 22 66 20 54
- **Équipe DevOps Isagri** : membres autorisés à approuver les actions via canal Teams dédié

### Financiers
- Coût VM : [à définir]
- Coût licences : OpenClaw (open-source), MCP (open-source)
- Coût LLM : [à définir selon le modèle utilisé]

---

## 8. Contrôles

### Critères de Contrôle Périodique
| Point de Contrôle | Critère | Fréquence | Responsable |
|-------------------|---------|-----------|-------------|
| Avancement vs planning | Jalons respectés à ±1 semaine | Hebdomadaire | Étudiant + Tuteur entreprise |
| Qualité du diagnostic | Justesse ≥ 80% | À chaque itération | Étudiant |
| Sécurité | Zéro action sans approbation | Continu | Étudiant |
| MTTR | Réduction mesurable | Phase 5 (S16-S20) | Étudiant + Tuteur entreprise |
| Conformité mémoire | Format UniLaSalle respecté | Continu | Étudiant + Tuteur école |

### Points de Contrôle Formels
| Point | Date | Participants | Livrable |
|-------|------|-------------|----------|
| Validation cahier des charges | S4 | Tuteur entreprise + Tuteur école | Ce document signé |
| Revue de projet intermédiaire | S13 | Tuteur entreprise + Tuteur école + Parties prenantes | Démo POC + avancement |
| Validation mémoire (tuteur entreprise) | S24 | Tuteur entreprise | Mémoire complet |
| Validation mémoire (tuteur école) | S25 | Tuteur école | Mémoire complet |
| Remise au secrétariat | J-7 ouvrés | Secrétariat | Mémoire final |
| Soutenance | 25/08 – 05/09 | Jury | Présentation + démo |

---

## Compétences Développées (Grille NAME)

| Compétence | Niveau Visé | Justification |
|------------|-------------|---------------|
| Architecture d'agents IA | **M → E** | Conception d'un système RPAE complet avec MCP |
| DevOps / CI-CD | **A → M** | Intégration Azure DevOps + Digital.ai Release |
| Sécurité / Gouvernance | **N → A** | Pattern d'approbation, audit, gestion des secrets |
| Recherche / Méthodologie | **N → A** | Étude de cas, mesure quantitative/qualitative |
| Communication | **A → M** | Rédaction mémoire, soutenance, démo |

---

## Validation

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Étudiant | [Nom Prénom] | | |
| Tuteur entreprise | [Nom Prénom] | | |
| Tuteur école | S. POMPORTES | | |
