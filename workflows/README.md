# Guide des Workflows de Débat

Ce dossier contient les workflows et règles pour orchestrer des débats structurés entre agents IA. L'objectif est de produire des documents et décisions de haute qualité en confrontant plusieurs perspectives.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        HUMAIN                                    │
│                    (Validation finale)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Escalade si nécessaire
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MANAGER-DEBAT                                │
│              (Orchestration, synthèse, arbitrage)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Coordination
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  ACTOR 1  │   │  ACTOR 2  │   │  ACTOR N  │
    │(Producteur│   │(Producteur│   │(Producteur│
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                   ┌───────────┐
                   │  CRITIC   │
                   │ (Challenge)│
                   └───────────┘
```

---

## Workflows Disponibles

### Workflows de création

| # | Workflow | Quand l'utiliser | Durée | Agents principaux |
|---|----------|------------------|-------|-------------------|
| 01 | [Brainstorm Idées](01-WF-BRAINSTORM-IDEES.md) | Explorer une nouvelle idée | 30 min | PRODUIT, RECHERCHE, CRITIQUE |
| 02 | [Design Architecture](02-WF-DESIGN-ARCHI.md) | Concevoir une architecture technique | 45 min | ARCHITECTE, DEVOPS, SECURITE |
| 04 | [Planification Projet](04-WF-PLANIFICATION-PROJET.md) | Définir roadmap et backlog | 45 min | PRODUIT, ARCHITECTE, DEVOPS |

### Workflows de revue

| # | Workflow | Quand l'utiliser | Durée | Agents principaux |
|---|----------|------------------|-------|-------------------|
| 03 | [Revue Sécurité](03-WF-REVUE-SECURITE.md) | Auditer un composant/système | 30 min | SECURITE, ARCHITECTE, DEVOPS |
| 07 | [Validation Livrable](07-WF-VALIDATION-LIVRABLE.md) | Revue finale avant soumission | 20 min | Expert domaine, CRITIQUE |

### Workflows de gouvernance

| # | Workflow | Quand l'utiliser | Durée | Agents principaux |
|---|----------|------------------|-------|-------------------|
| 05 | [Rétrospective](05-WF-RETROSPECTIVE.md) | Analyser une phase passée | 30 min | Tous les agents concernés |
| 06 | [Résolution Conflit](06-WF-RESOLUTION-CONFLIT.md) | Arbitrer un désaccord | 20 min | MANAGER, agents en conflit |

---

## Règles Disponibles

| # | Règle | Description |
|---|-------|-------------|
| 01 | [Débat Général](rules/01-RULES-DEBAT-GENERAL.md) | Principes de base des débats |
| 02 | [Actor-Critic](rules/02-RULES-ACTOR-CRITIC.md) | Pattern de proposition/critique |
| 03 | [Manager Routing](rules/03-RULES-MANAGER-ROUTING.md) | Sélection des agents par sujet |
| 04 | [Escalade](rules/04-RULES-ESCALADE.md) | Quand et comment escalader |
| 05 | [Format Sortie](rules/05-RULES-FORMAT-SORTIE.md) | Standards de formatage |
| 06 | [Timeboxing](rules/06-RULES-TIMEBOXING.md) | Gestion du temps |

---

## Comment Choisir le Bon Workflow

### Arbre de décision

```
Question initiale
       │
       ▼
┌──────────────────┐
│ Type de besoin ? │
└────────┬─────────┘
         │
    ┌────┴────┬────────────┬───────────┐
    ▼         ▼            ▼           ▼
 Création   Revue      Analyse     Conflit
    │         │            │           │
    ▼         ▼            ▼           ▼
┌───────┐ ┌───────┐   ┌────────┐  ┌────────┐
│Idée?  │ │Sécu?  │   │Passé?  │  │WF-06   │
└───┬───┘ └───┬───┘   └────┬───┘  └────────┘
    │         │            │
   Oui       Oui          Oui
    │         │            │
    ▼         ▼            ▼
 WF-01     WF-03        WF-05
    │
   Non
    │
    ▼
┌───────┐
│Archi? │
└───┬───┘
    │
   Oui
    │
    ▼
 WF-02
    │
   Non
    │
    ▼
┌───────┐
│Plan?  │
└───┬───┘
    │
   Oui
    │
    ▼
 WF-04
```

### Guide rapide

| Je veux... | Workflow |
|------------|----------|
| Explorer une idée de projet | WF-01 Brainstorm |
| Concevoir l'architecture d'un système | WF-02 Design Archi |
| Vérifier la sécurité d'un composant | WF-03 Revue Sécurité |
| Planifier les prochaines semaines | WF-04 Planification |
| Analyser ce qui a bien/mal fonctionné | WF-05 Rétrospective |
| Résoudre un désaccord entre agents | WF-06 Résolution Conflit |
| Valider un document avant livraison | WF-07 Validation |

---

## Déroulement Type d'un Débat

### Phase 1 : Cadrage (5 min)
1. MANAGER reformule la question/le besoin
2. MANAGER sélectionne les agents pertinents
3. MANAGER rappelle les contraintes et le temps disponible

### Phase 2 : Production (10-15 min)
1. Chaque agent producteur (ACTOR) propose sa contribution
2. Les propositions sont structurées selon le format standard
3. Chaque agent explicite ses hypothèses

### Phase 3 : Critique (5-10 min)
1. AGENT-CRITIQUE analyse chaque proposition
2. Il attribue un score de confiance
3. Il propose des améliorations concrètes

### Phase 4 : Révision (5-10 min)
1. Les agents producteurs intègrent les critiques
2. Ils justifient les points maintenus
3. Maximum 2 tours de révision

### Phase 5 : Synthèse (10 min)
1. MANAGER consolide les meilleures contributions
2. Il produit le livrable final
3. Il documente les décisions et les points ouverts

---

## Exemple de Session Complète

### Contexte
Question : "Quelle base de données utiliser pour le POC ?"

### Session

```
[MANAGER-DEBAT] 
Workflow : WF-02 Design Architecture
Question : Choix de la base de données pour le POC
Agents : ARCHITECTE, DEVOPS, CRITIQUE
Durée : 30 min

---

[AGENT-ARCHITECTE] Proposition
Base de données : SQLite
Justification : Simple, embarqué, pas de serveur à maintenir
Hypothèses : Volume < 10 Go, un seul processus écrit
Risques : Concurrence d'écriture limitée

---

[AGENT-DEVOPS] Complément
SQLite OK pour POC. Points d'attention :
- Backup : script cron simple
- Migration V2 : prévoir interface abstraite
- Monitoring : logs applicatifs suffisants

---

[AGENT-CRITIQUE] 
Score : 3/5
Points forts : Simplicité, time-to-market
Points faibles : 
- Hypothèse "un seul processus" à vérifier (heartbeat + actions)
- Migration V2 risquée si schéma évolue
Suggestion : Interface Repository pour découpler

---

[AGENT-ARCHITECTE] Révision
SQLite avec :
- Mode WAL pour meilleure concurrence
- Interface Repository abstraite
- Mutex applicatif si nécessaire

---

[AGENT-CRITIQUE]
Score révisé : 4/5
Acceptable avec les mitigations proposées.

---

[MANAGER-DEBAT] Synthèse

## Décision : SQLite pour le POC

### ADR-001 : Choix de SQLite
- **Statut** : Accepté
- **Contexte** : POC avec contraintes de temps
- **Décision** : SQLite avec mode WAL et interface Repository
- **Conséquences** : Migration V2 facilitée, légère complexité ajoutée

### Actions
| Action | Responsable | Échéance |
|--------|-------------|----------|
| Implémenter interface Repository | DEVOPS | S4 |
| Configurer mode WAL | DEVOPS | S4 |
```

---

## Bonnes Pratiques

### Pour le MANAGER
- Toujours commencer par reformuler la question
- Cadrer le temps strictement
- Ne jamais laisser un débat sans conclusion
- Documenter les désaccords, pas les ignorer

### Pour les ACTORS
- Structurer chaque proposition (pas de prose libre)
- Expliciter les hypothèses
- Reconnaître les limites de sa proposition
- Intégrer visiblement les critiques

### Pour le CRITIC
- Critiquer la proposition, pas l'agent
- Toujours proposer une amélioration
- Reconnaître les points forts
- Donner un score honnête

### Pour tous
- Respecter le timeboxing
- Utiliser les formats standards
- Escalader plutôt que bloquer
- Privilégier le consensus pragmatique

---

## Fichiers et Structure

```
workflows/
├── README.md                          # Ce fichier
├── 01-WF-BRAINSTORM-IDEES.md
├── 02-WF-DESIGN-ARCHI.md
├── 03-WF-REVUE-SECURITE.md
├── 04-WF-PLANIFICATION-PROJET.md
├── 05-WF-RETROSPECTIVE.md
├── 06-WF-RESOLUTION-CONFLIT.md
├── 07-WF-VALIDATION-LIVRABLE.md
└── rules/
    ├── 01-RULES-DEBAT-GENERAL.md
    ├── 02-RULES-ACTOR-CRITIC.md
    ├── 03-RULES-MANAGER-ROUTING.md
    ├── 04-RULES-ESCALADE.md
    ├── 05-RULES-FORMAT-SORTIE.md
    └── 06-RULES-TIMEBOXING.md
```

---

## Évolutions Futures

- [ ] Ajouter des exemples de sessions complètes par workflow
- [ ] Créer des templates de livrables pré-remplis
- [ ] Définir des métriques de qualité des débats
- [ ] Automatiser le timeboxing avec des rappels
