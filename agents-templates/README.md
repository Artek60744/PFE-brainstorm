# Templates d'Agents

Ce dossier contient des templates d'agents génériques réutilisables pour orchestrer des débats multi-perspectives.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                     MANAGER-DEBAT                            │
│                   (Orchestration)                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
     ▼                     ▼                     ▼
┌─────────┐         ┌─────────────┐        ┌─────────┐
│ ACTORS  │         │   ACTORS    │        │ CRITIC  │
│(Experts)│         │ (Support)   │        │(Quality)│
└─────────┘         └─────────────┘        └─────────┘
```

---

## Templates Disponibles

### Agents Producteurs (Actors)

| Template | Rôle | Expertise principale |
|----------|------|---------------------|
| [TPL-ARCHITECTE](TPL-ARCHITECTE.md) | Conception technique | Architecture, patterns, composants |
| [TPL-DEVOPS](TPL-DEVOPS.md) | Opérations | CI/CD, infra, observabilité |
| [TPL-PRODUCT-OWNER](TPL-PRODUCT-OWNER.md) | Valeur métier | Priorisation, UX, KPIs |
| [TPL-TESTEUR-QA](TPL-TESTEUR-QA.md) | Qualité | Tests, cas limites, défauts |
| [TPL-SECOPS](TPL-SECOPS.md) | Sécurité | Menaces, contrôles, conformité |
| [TPL-FINOPS](TPL-FINOPS.md) | Coûts | Optimisation cloud, TCO, budget |
| [TPL-CHERCHEUR](TPL-CHERCHEUR.md) | Recherche | État de l'art, sources, tendances |
| [TPL-DATA-ENGINEER](TPL-DATA-ENGINEER.md) | Données | Pipelines, qualité, gouvernance |

### Agents Transverses

| Template | Rôle | Fonction |
|----------|------|----------|
| [TPL-CRITIQUE](TPL-CRITIQUE.md) | Challenge | Devil's advocate, risques |
| [TPL-MANAGER-DEBAT](TPL-MANAGER-DEBAT.md) | Orchestration | Cadrage, synthèse, arbitrage |

### Méta-documentation

| Fichier | Contenu |
|---------|---------|
| [00-STRUCTURE-TEMPLATE](00-STRUCTURE-TEMPLATE.md) | Structure standard d'un template |

---

## Matrice de Sélection des Agents

### Par type de sujet

| Sujet | Agents recommandés |
|-------|-------------------|
| Architecture technique | Architecte + DevOps + SecOps + Critique |
| Choix technologique | Architecte + Chercheur + DevOps + Critique |
| Sécurité | SecOps + Architecte + DevOps + Critique |
| Coûts | FinOps + DevOps + Architecte + Critique |
| Qualité | QA + DevOps + Architecte + Critique |
| Priorisation | PO + Architecte + DevOps + Critique |
| Données | Data Engineer + Architecte + SecOps + Critique |

### Par type de décision

| Décision | Agents à impliquer |
|----------|-------------------|
| Nouvelle fonctionnalité | PO + Architecte + DevOps |
| Nouvelle infrastructure | DevOps + Architecte + FinOps + SecOps |
| Migration | Architecte + DevOps + Data Engineer |
| Optimisation | FinOps + DevOps + Architecte |
| Audit | SecOps + QA + Architecte |

---

## Comment Utiliser ces Templates

### 1. Sélectionner les agents pertinents
Utiliser la matrice ci-dessus ou les règles de routing (`workflows/rules/03-RULES-MANAGER-ROUTING.md`)

### 2. Adapter le template au contexte
- Les templates sont génériques et doivent être contextualisés
- Ajouter les contraintes spécifiques au projet
- Personnaliser les questions types si nécessaire

### 3. Intégrer dans un workflow
Chaque workflow (`workflows/XX-WF-*.md`) définit :
- Quels agents participent
- Dans quel ordre
- Avec quel format de sortie

### 4. Instancier pour un projet spécifique
Pour un projet concret, créer des agents spécialisés dans le dossier `agents/` en s'inspirant des templates.

---

## Créer un Nouvel Agent

1. **Copier** `00-STRUCTURE-TEMPLATE.md`
2. **Renommer** en `TPL-[NOM].md`
3. **Remplir** chaque section
4. **Tester** avec un scénario réel
5. **Ajouter** à ce README

Voir `00-STRUCTURE-TEMPLATE.md` pour le guide complet.

---

## Bonnes Pratiques

### Spécialisation
- Un agent = une perspective unique
- Pas de chevauchement entre agents
- Mieux vaut 2 agents spécialisés qu'1 agent généraliste

### Complémentarité
- Les agents doivent se compléter
- Chaque agent apporte ce que les autres n'ont pas
- Le CRITIQUE est toujours présent

### Équilibre
- Minimum 2 agents producteurs + 1 critique
- Maximum 5-6 agents par débat (au-delà, trop de bruit)
- Toujours un MANAGER pour orchestrer

---

## Évolutions Futures

- [ ] Ajouter TPL-UX-DESIGNER
- [ ] Ajouter TPL-LEGAL
- [ ] Ajouter TPL-SUPPORT-CLIENT
- [ ] Créer des variantes par industrie
- [ ] Ajouter des exemples de débats par template
