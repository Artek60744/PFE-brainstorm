# WF-DESIGN-ARCHI

## Objectif
Concevoir ou améliorer une architecture technique en confrontant les perspectives de plusieurs experts. Produire :
- Un diagramme d'architecture (C4 ou équivalent)
- Une liste de décisions techniques argumentées (ADR)
- Une matrice des risques techniques
- Un plan d'implémentation priorisé

---

## Agents impliqués
- **MANAGER-DEBAT** (orchestrateur)
- **AGENT-ARCHITECTE** (lead technique)
- **AGENT-DEVOPS** (déployabilité, CI/CD, observabilité)
- **AGENT-SECURITE** (garde-fous, authentification, secrets)
- **AGENT-CRITIQUE** (challenge des hypothèses)

---

## Étapes

### 1. [MANAGER-DEBAT] Cadrage
- Reformule le besoin technique en termes clairs
- Identifie les contraintes : budget, délais, stack existante, compétences équipe
- Précise le niveau de détail attendu (vue contexte, container, component)
- Choisit les agents à impliquer selon le périmètre

### 2. [AGENT-ARCHITECTE] Proposition initiale
- Propose une architecture avec :
  - Diagramme ASCII ou description structurée des composants
  - Stack technique recommandée
  - Interfaces entre composants
  - Patterns utilisés (microservices, event-driven, monolithe modulaire, etc.)
- Explicite ses hypothèses de design
- Liste les alternatives considérées et rejetées

### 3. [AGENT-DEVOPS] Revue opérationnelle
- Valide la déployabilité de l'architecture proposée
- Identifie les besoins CI/CD (pipelines, environnements)
- Évalue l'observabilité (logs, métriques, traces)
- Propose des ajustements pour la scalabilité et la résilience
- Estime la complexité opérationnelle (1-5)

### 4. [AGENT-SECURITE] Revue sécurité
- Analyse les flux de données sensibles
- Vérifie la gestion des secrets et de l'authentification
- Identifie les surfaces d'attaque
- Propose des garde-fous et mitigations
- Attribue un score de risque sécurité (1-5)

### 5. [AGENT-CRITIQUE] Challenge
- Attaque les hypothèses implicites de l'architecture
- Identifie les SPOF (Single Points of Failure)
- Propose des alternatives ou simplifications
- Questionne le rapport coût/bénéfice des choix techniques
- Attribue un score de confiance global (1-5)

### 6. [BOUCLE ACTOR/CRITIC — 2 tours]
- **Tour 1** : AGENT-ARCHITECTE révise sa proposition en intégrant les retours DevOps, Sécurité et Critique
- AGENT-CRITIQUE évalue la révision et identifie les points restants
- **Tour 2** : AGENT-ARCHITECTE finalise avec les derniers ajustements
- AGENT-CRITIQUE donne son évaluation finale

### 7. [MANAGER-DEBAT] Synthèse
- Consolide l'architecture finale
- Rédige les ADR (Architecture Decision Records) pour chaque décision majeure
- Produit la matrice des risques consolidée
- Définit le plan d'implémentation avec jalons

---

## Livrables attendus

| Livrable | Format | Responsable |
|----------|--------|-------------|
| Diagramme d'architecture | ASCII / Mermaid / C4 | ARCHITECTE |
| Liste des composants | Tableau (nom, rôle, techno) | ARCHITECTE |
| ADR (décisions) | Markdown structuré | MANAGER |
| Matrice des risques | Tableau (risque, impact, proba, mitigation) | MANAGER |
| Plan d'implémentation | Liste priorisée avec dépendances | MANAGER |

---

## Conditions d'arrêt
- Maximum 2 tours de débat Actor/Critic
- Si score de confiance CRITIQUE < 3 après 2 tours : escalade vers l'humain avec rapport des divergences
- MANAGER-DEBAT produit toujours une synthèse même en cas de désaccord

---

## Critères de qualité

- [ ] Tous les composants sont justifiés (pas de complexité gratuite)
- [ ] Les interfaces sont clairement définies
- [ ] Les risques majeurs ont une mitigation
- [ ] L'architecture est déployable avec les compétences de l'équipe
- [ ] Le coût opérationnel est acceptable
