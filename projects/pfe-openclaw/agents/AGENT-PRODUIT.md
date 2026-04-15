# Agent : Analyste Produit / Valeur Métier

## Rôle
Définir les personas, les cas d'usage métier, les critères de succès chiffrés, et la roadmap produit.

---

## 1. Étapes du Projet

### Phase 0 — Discovery Produit (Semaines 1-3)
- Identifier les personas : SRE, développeurs, ops, release managers
- Cartographier le workflow actuel de résolution d'incidents
- **Établir la baseline MTTR manuellement** (impossible d'extraire depuis ADO) : chronométrer 10-15 incidents
- Définir les KPIs de succès (SMART) — objectif 50% maintenu comme cible ambitieuse

### Phase 1 — Definition du MVP (Semaines 4-6)
- Prioriser les cas d'usage par impact MTTR
- Définir le scope du MVP : détection + diagnostic d'échec de pipeline + **dashboard obligatoire**
- Rédiger les user stories du MVP
- Valider le scope avec le tuteur

### Phase 2 — Conception UX d'Approbation (Semaines 7-9)
- Concevoir le flux **Teams (canal dédié équipe DevOps)** (mockups des messages interactifs)
- Définir le format du plan d'action présenté à l'humain
- Tester la lisibilité du diagnostic avec des utilisateurs cibles
- Itérer sur le format (trop technique vs pas assez)

### Phase 3 — Dashboard Produit (Semaines 10-13) — **MVP OBLIGATOIRE**
- Concevoir le dashboard : pipelines en cours, erreurs par pipeline, contexte historique, dépendances
- Fonctionnalités MVP : tableau + filtres + contexte erreurs par pipeline + dépendances
- Implémenter le dashboard avec maintenance par l'agent
- Tester l'UX avec les personas cibles

### Phase 4 — Mesure de Valeur (Semaines 14-18)
- **Mesurer le MTTR manuellement** (chronomètre + Work Items ADO) — pas d'extraction automatique
- Collecter les retours qualitatifs des utilisateurs (confiance, satisfaction)
- Calculer le ROI temps gagné vs temps passé à configurer/maintenir l'agent
- Ajuster le produit en fonction des retours

### Phase 5 — Roadmap V1/V2 (Semaines 19-22)
- Définir le backlog V1 (améliorations post-MVP)
- Définir le backlog V2 (fonctionnalités avancées)
- Documenter les leçons apprises produit
- Préparer la démo de soutenance

---

## 2. Décisions Techniques Clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Persona prioritaire | Développeur + SRE | Ce sont les premiers impactés par les échecs de pipeline |
| KPI principal | Réduction de 50% du temps d'analyse primaire (objectif ambitieux) | SMART, mesurable manuellement, aligné avec l'objectif PFE |
| KPI secondaire | Confiance de l'équipe (survey qualitative) | Mesure l'adoption réelle, pas juste la performance technique |
| Format du plan d'action | Structuré (Cause → Impact → Action proposée → Risque) | Lisible par un humain, exploitable pour l'approbation |
| Dashboard | **Requirement MVP** — minimaliste mais obligatoire | Tableau + filtres + contexte erreurs par pipeline + dépendances |
| Canal d'approbation | Teams (canal dédié équipe DevOps) | Restreint aux membres de l'équipe DevOps |
| Mesure MTTR | Manuelle (chronomètre + Work Items ADO) | Pas d'extraction automatique depuis ADO |

---

## 3. Risques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| L'équipe n'adopte pas l'agent (méfiance envers l'IA) | Haut | Moyen | Impliquer l'équipe dès le début, transparence totale sur le fonctionnement |
| Le MTTR baseline est impossible à mesurer précisément | Moyen | Certain | Mesure manuelle : chronométrer 10-15 incidents + delta Work Items ADO |
| Le diagnostic est trop technique pour les non-experts | Moyen | Moyen | Tester le format avec différents personas, itérer |
| Le dashboard devient un projet dans le projet | Haut | Moyen | **Obligatoire MVP** — scope strict : tableau + filtres + contexte par pipeline + dépendances |
| Le ROI temps est négatif (plus de temps à configurer qu'à gagner) | Haut | Faible | Mesurer en continu, pivoter si nécessaire |

---

## 4. Livrables

| Livrable | Description | Échéance |
|----------|-------------|----------|
| Cartographie des personas | Document des utilisateurs cibles + workflows | Semaine 3 |
| Baseline MTTR | **Mesure manuelle** : chronométrer 10-15 incidents + méthode de calcul | Semaine 3 |
| User stories MVP | Backlog priorisé avec critères d'acceptation | Semaine 6 |
| Mockups UX d'approbation | Maquettes des messages **Teams (canal dédié DevOps)** | Semaine 9 |
| Dashboard MVP | Fonctionnel avec maintenance par l'agent — **obligatoire MVP** | Semaine 13 |
| Rapport de mesure de valeur | MTTR avant/après (mesure manuelle) + retours qualitatifs | Semaine 18 |
| Roadmap V1/V2 | Backlog structuré par version | Semaine 22 |
| Démo de soutenance | Scénario de démonstration complet | Semaine 25 |

---

## 5. Critères de Réussite

- [ ] Le MVP couvre au moins 80% des cas d'échec de pipeline courants
- [ ] Le MTTR moyen est réduit (objectif ambitieux 50%, analyse réaliste des résultats)
- [ ] 80%+ des utilisateurs testés trouvent le diagnostic compréhensible
- [ ] Le dashboard est fonctionnel et utilisé au moins 3 fois/semaine par l'équipe
- [ ] Le ROI temps est positif (temps gagné > temps de configuration)
- [ ] L'équipe exprime une confiance > 3/5 dans l'agent (survey qualitative)
- [ ] La démo de soutenance est reproductible et impressionnante
