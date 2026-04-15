# Agent : Analyste Recherche / Mémoire

## Rôle
Structurer l'état de l'art, la méthodologie de recherche, le plan du mémoire, et les références académiques.

---

## 1. Étapes du Projet

### Phase 0 — État de l'Art (Semaines 1-4)
- Rechercher les papers sur les agents IA en opérations IT (AIOps, SRE automatisé)
- Analyser l'émergence du Model Context Protocol (MCP) comme standard d'interopérabilité
- Comparer les architectures d'agents : locaux/persistants (OpenClaw) vs cloud/éphémères
- Documenter le passage de n8n (orchestration réactive) à OpenClaw (agent proactif)
- Compiler une bibliographie annotée (15-20 références minimum)

### Phase 1 — Méthodologie de Recherche (Semaines 5-7)
- Définir la méthodologie : étude de cas unique avec mesure quantitative + qualitative
- Concevoir le protocole d'expérimentation (groupe témoin vs groupe avec agent)
- Définir les instruments de mesure (métriques ADO, surveys, interviews)
- Valider la méthodologie avec le tuteur et l'établissement

### Phase 2 — Rédaction — Parties Théoriques (Semaines 8-14)
- Rédiger le chapitre 1 : Contexte et problématique
- Rédiger le chapitre 2 : État de l'art (AIOps, agents IA, MCP, RPAE)
- Rédiger le chapitre 3 : Architecture et conception du système
- Faire relire par le tuteur après chaque chapitre

### Phase 3 — Rédaction — Expérimentation (Semaines 15-20)
- Rédiger le chapitre 4 : Mise en œuvre et expérimentation
- Rédiger le chapitre 5 : Résultats et analyse (MTTR avant/après)
- Rédiger le chapitre 6 : Discussion et limites
- Intégrer les graphiques et tableaux de résultats

### Phase 4 — Finalisation (Semaines 21-24)
- Rédiger l'introduction et la conclusion
- Compiler la bibliographie finale
- Vérifier la conformité avec les normes UniLaSalle
- Préparer les annexes (code, configurations, captures d'écran)

### Phase 5 — Préparation Soutenance (Semaines 25-26)
- Créer le support de présentation
- Préparer la démo live
- Anticiper les questions du jury

---

## 2. Décisions Techniques Clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Type de recherche | Étude de cas unique avec mesure | Réaliste pour un PFE, permet une analyse approfondie |
| Références clés | AIOps, SRE automatisé, agents IA locaux, MCP | Piliers du sujet, littérature émergente mais existante |
| Justification OpenClaw vs n8n | Chapitre dédié dans le mémoire | Monture la maturité de l'analyse technique |
| Méthode d'évaluation | Mixte : quantitative (MTTR) + qualitative (confiance) | Couvre les deux dimensions de la recherche |
| Structure du mémoire | Conforme UniLaSalle : 6 parties (Présentation entreprise → Démarche/État de l'art → Architecture → Travail réalisé → Résultats → Discussion) | 60-80 pages hors annexes, Arial 11-12, interligne simple, marges 2,5/3 cm |

---

## 3. Risques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Littérature insuffisante sur MCP (trop récent) | Moyen | Haut | Élargir aux protocoles d'intégration IA similaires, citer la doc officielle |
| Littérature insuffisante sur OpenClaw | Moyen | Moyen | Traiter comme étude de cas "agent local persistant", généraliser les concepts |
| Résultats d'expérimentation non concluants | Haut | Moyen | Documenter les limites honnêtement, c'est aussi un résultat de recherche |
| Non-conformité avec le format UniLaSalle | Haut | Faible | Format documenté dans `contexte_PFE_unilasalle.md`, vérification continue |
| Retard de rédaction | Haut | Moyen | Rédiger en continu (pas en batch à la fin), relire au fil de l'eau |

---

## 4. Livrables

| Livrable | Description | Échéance |
|----------|-------------|----------|
| Bibliographie annotée | 15-20 références avec résumé et pertinence | Semaine 4 |
| Protocole d'expérimentation | Méthodologie validée par le tuteur | Semaine 7 |
| Chapitre 1-2 | Contexte + État de l'art | Semaine 10 |
| Chapitre 3-4 | Architecture + Mise en œuvre | Semaine 16 |
| Chapitre 5-6 | Résultats + Discussion | Semaine 20 |
| Mémoire complet | Version finale prête pour relecture | Semaine 23 |
| Support de soutenance | Présentation + démo | Semaine 25 |
| Annexes | Code, configs, captures, données brutes | Semaine 24 |

---

## 5. Critères de Réussite

- [ ] La bibliographie contient 15+ références académiques pertinentes
- [ ] Le protocole d'expérimentation est validé par le tuteur
- [ ] Chaque chapitre est relu et approuvé avant de passer au suivant
- [ ] Le mémoire respecte le format et le nombre de pages imposés par UniLaSalle
- [ ] Les résultats sont présentés avec des graphiques et une analyse statistique
- [ ] Les limites de l'étude sont discutées honnêtement
- [ ] La soutenance est claire, la démo fonctionne, les questions sont anticipées
