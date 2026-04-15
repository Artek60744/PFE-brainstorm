# WF-REVUE-SECURITE

## Objectif
Auditer un composant, une décision ou une architecture du point de vue sécurité. Produire :
- Une analyse des menaces (STRIDE ou équivalent)
- Une matrice des risques sécurité priorisée
- Un plan de mitigation actionnable
- Une liste de recommandations classées par urgence

---

## Agents impliqués
- **MANAGER-DEBAT** (orchestrateur)
- **AGENT-SECURITE** (lead de l'audit)
- **AGENT-ARCHITECTE** (contexte technique)
- **AGENT-DEVOPS** (aspects opérationnels)
- **AGENT-CRITIQUE** (challenge des mitigations)

---

## Étapes

### 1. [MANAGER-DEBAT] Cadrage du périmètre
- Définit le scope de l'audit : composant, flux, infrastructure, ou système complet
- Identifie les actifs critiques à protéger
- Précise le niveau de sensibilité des données
- Rappelle les contraintes réglementaires (RGPD, etc.)

### 2. [AGENT-ARCHITECTE] Présentation du contexte
- Décrit l'architecture du périmètre audité
- Liste les flux de données (entrées, sorties, stockage)
- Identifie les dépendances externes (API, services tiers)
- Documente les mécanismes d'authentification/autorisation existants

### 3. [AGENT-SECURITE] Analyse des menaces (STRIDE)
Pour chaque composant/flux, analyse :
- **S**poofing : Usurpation d'identité possible ?
- **T**ampering : Modification non autorisée des données ?
- **R**epudiation : Actions non traçables ?
- **I**nformation Disclosure : Fuite de données sensibles ?
- **D**enial of Service : Vulnérabilité aux attaques DoS ?
- **E**levation of Privilege : Escalade de privilèges possible ?

Produit une matrice des risques :
| Menace | Composant | Probabilité | Impact | Score | Mitigation proposée |

### 4. [AGENT-DEVOPS] Revue opérationnelle sécurité
- Vérifie la gestion des secrets (rotation, stockage)
- Analyse les logs et la traçabilité
- Évalue la sécurité du pipeline CI/CD
- Identifie les vulnérabilités infrastructure (ports ouverts, configs par défaut)
- Vérifie les mises à jour et le patching

### 5. [AGENT-CRITIQUE] Challenge des mitigations
- Questionne l'efficacité des mitigations proposées
- Identifie les scénarios d'attaque non couverts
- Propose des alternatives ou renforcements
- Évalue le rapport effort/réduction de risque
- Attribue un score de confiance aux mitigations (1-5)

### 6. [BOUCLE ACTOR/CRITIC — 2 tours]
- **Tour 1** : AGENT-SECURITE révise son analyse en intégrant les retours Critique et DevOps
- AGENT-CRITIQUE évalue la révision
- **Tour 2** : AGENT-SECURITE finalise les recommandations
- AGENT-CRITIQUE donne son évaluation finale

### 7. [MANAGER-DEBAT] Synthèse et rapport
- Consolide la matrice des risques finale
- Classe les recommandations par urgence :
  - **P0** : Critique — à traiter immédiatement
  - **P1** : Haute — à traiter avant mise en production
  - **P2** : Moyenne — à planifier dans le sprint suivant
  - **P3** : Basse — backlog
- Produit le plan de mitigation avec responsables et échéances
- Documente les risques acceptés (avec justification)

---

## Livrables attendus

| Livrable | Format | Responsable |
|----------|--------|-------------|
| Cartographie des flux | Diagramme + description | ARCHITECTE |
| Analyse STRIDE | Tableau par composant | SECURITE |
| Matrice des risques | Tableau priorisé | SECURITE |
| Revue infra/pipeline | Checklist | DEVOPS |
| Plan de mitigation | Liste actions + responsables + échéances | MANAGER |
| Risques acceptés | Liste justifiée | MANAGER |

---

## Conditions d'arrêt
- Maximum 2 tours de débat Actor/Critic
- Si un risque P0 est identifié sans mitigation viable : escalade immédiate vers l'humain
- Tout risque accepté doit être documenté et signé par l'humain responsable

---

## Checklist de revue sécurité

### Authentification & Autorisation
- [ ] Authentification forte implémentée
- [ ] Principe du moindre privilège respecté
- [ ] Tokens/sessions avec expiration
- [ ] Révocation d'accès fonctionnelle

### Gestion des secrets
- [ ] Aucun secret en dur dans le code
- [ ] Secrets stockés dans un vault sécurisé
- [ ] Rotation des secrets automatisée ou planifiée
- [ ] Accès aux secrets audité

### Données
- [ ] Données sensibles chiffrées au repos
- [ ] Données sensibles chiffrées en transit (TLS)
- [ ] Logs ne contiennent pas de données sensibles
- [ ] Conformité RGPD vérifiée

### Infrastructure
- [ ] Ports non nécessaires fermés
- [ ] Configurations par défaut modifiées
- [ ] Mises à jour de sécurité appliquées
- [ ] Segmentation réseau appropriée

### Audit & Monitoring
- [ ] Actions critiques loguées
- [ ] Alertes sur comportements suspects
- [ ] Rétention des logs conforme
- [ ] Plan de réponse aux incidents documenté
