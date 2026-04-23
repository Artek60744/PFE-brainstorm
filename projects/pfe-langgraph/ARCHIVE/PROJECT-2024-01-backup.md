# Projet : Agent IA RPAE pour Réduction du MTTR

## Vue d'ensemble

Ce projet de fin d'études (PFE) vise à évaluer dans quelle mesure un agent IA implémentant le pattern **Read-Plan-Approve-Execute (RPAE)** peut réduire le MTTR (Mean Time To Repair) des incidents DevOps.

---

## Contexte

### Entreprise
**Isagri** — Éditeur de logiciels pour le monde agricole

### Établissement
**UniLaSalle** — Programme RIOC (Responsable en Ingénierie des Logiciels)

### Problématique
Les équipes DevOps passent un temps significatif à diagnostiquer les échecs de pipelines CI/CD. Ce temps pourrait être réduit par un agent IA capable de :
1. **Lire** les logs et le contexte de l'échec
2. **Planifier** une action de correction
3. **Demander l'approbation** humaine
4. **Exécuter** l'action validée

---

## Objectifs

### Objectif Principal
**Réduire de 50% le temps d'analyse primaire des échecs de pipeline**

> Note : Cet objectif est ambitieux et sera analysé honnêtement dans le mémoire.

### Objectifs Secondaires
- Implémenter un cycle RPAE complet et fonctionnel
- Intégrer avec Azure DevOps via MCP
- Créer un dashboard de suivi des pipelines (MVP obligatoire)
- Mesurer et documenter les résultats

---

## Contraintes

### Techniques
| Contrainte | Impact | Mitigation |
|------------|--------|------------|
| Pas de sandbox | Tests en production uniquement | Mode dry-run obligatoire |
| Champs personnalisés Isagri | Compatibilité MCP incertaine | Tests précoces S4 |
| MTTR non extractible d'ADO | Mesure automatique impossible | Chronomètre manuel |

### Organisationnelles
| Contrainte | Impact |
|------------|--------|
| 26 semaines de délai | Planning serré |
| Validation tuteur requise | Dépendance externe |
| Accès équipe DevOps | Coordination nécessaire |

### Sécurité
| Contrainte | Raison |
|------------|--------|
| Zéro action sans approbation | Sécurité production |
| Préfixe [OPENCLAW-TEST] | Identification des tests |
| 3 niveaux d'approbation | Proportionnel au risque |

---

## Stack Technique

```
┌─────────────────────────────────────────────────────────┐
│                      OpenClaw Agent                      │
│            (Mémoire persistante, Heartbeat)              │
└─────────────────────────┬───────────────────────────────┘
                          │ MCP
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │ Azure DevOps│ │ Digital.ai  │ │    Teams    │
   │  (CI/CD)    │ │  Release    │ │ (Approval)  │
   └─────────────┘ └─────────────┘ └─────────────┘
          │
          ▼
   ┌─────────────┐
   │   SQLite    │ → PostgreSQL (V2)
   │  (Mémoire)  │
   └─────────────┘
```

---

## Planning

| Phase | Semaines | Objectif | Livrable clé |
|-------|----------|----------|--------------|
| 0 - Setup | S1-S3 | Environnement prêt | OpenClaw + MCP fonctionnel |
| 1 - Read | S4-S6 | Lecture des données | POC Read complet |
| 2 - Plan | S7-S9 | Diagnostic automatisé | Moteur de diagnostic |
| 3 - Approve | S10-S12 | Flux d'approbation | Intégration Teams |
| 4 - Execute | S13-S15 | Cycle complet | MVP fonctionnel |
| 5 - Mesure | S16-S20 | Industrialisation | Rapport MTTR |
| 6 - Rédaction | S21-S26 | Soutenance | Mémoire + démo |

---

## Équipe

| Rôle | Responsabilité |
|------|----------------|
| Étudiant PFE | Développement, documentation, soutenance |
| Tuteur entreprise | Validation, accès environnements |
| Tuteur académique | Suivi méthodologique, évaluation |
| Équipe DevOps Isagri | Feedback, approbations |

---

## Liens

### Dossiers du projet
- [Agents](agents/) — Agents spécialisés pour ce projet
- [Artifacts](artifacts/) — Livrables du brainstorming
- [Decisions](decisions/) — ADR et décisions prises
- [Sessions](sessions/) — Historique des sessions de débat

### Framework
- [Core](../../core/) — Moteur du framework de brainstorming
- [Workflows](../../core/workflows/) — Workflows disponibles
- [Templates](../../core/templates/) — Templates d'agents

---

## État Actuel

**Phase** : Planification (pré-implémentation)

**Dernière mise à jour** : Janvier 2024

**Prochaines étapes** :
1. Valider l'architecture avec le tuteur
2. Installer OpenClaw
3. Configurer MCP Microsoft
