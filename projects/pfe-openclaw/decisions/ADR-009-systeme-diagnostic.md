# ADR-009 : Système de Diagnostic des Erreurs Pipeline

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
L'agent OpenClaw doit diagnostiquer les erreurs de pipeline et notifier l'équipe DevOps. Contraintes majeures :
- **Le bot n'a PAS le droit de relancer les builds**
- L'action principale est une notification Teams avec diagnostic complet
- L'agent propose la création d'un bug ADO avec formulation IA optimisée

Questions à résoudre :
1. Quel flux de diagnostic (détection → analyse → notification) ?
2. Comment classifier et analyser les erreurs ?
3. Comment stocker et exploiter l'historique ?
4. Comment affiner l'analyse au fil du temps ?

## Décision

### Architecture en 4 phases

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  DÉTECTION   │────▶│   ANALYSE    │────▶│  FORMULATION │────▶│ NOTIFICATION │
│  (Heartbeat) │     │  (LLM+Histo) │     │   (Output)   │     │   (Teams)    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
     < 30s               < 2 min              < 30s               < 10s
```

### Phase 1 : Collecte (< 30 secondes)
- Heartbeat détecte échec pipeline via MCP
- Récupérer logs de build (dernières 500 lignes ou section erreur)
- Récupérer contexte : commit, auteur, branche, changeset
- Vérifier dépendances : pipeline upstream récemment modifié ?

### Phase 2 : Analyse (< 2 minutes)
- Pré-traitement : extraction lignes ERROR/FAIL/EXCEPTION
- Génération fingerprint/signature de l'erreur
- Recherche patterns connus dans l'historique
- Corrélation par pipeline (même pipeline × 3, même auteur × 2)
- Analyse LLM : cause probable, impact, recommandations

### Phase 3 : Formulation (< 30 secondes)
- Générer message Teams structuré
- Pré-remplir URL bug ADO avec query params
- Calculer assignation suggérée (logique hiérarchique)

### Phase 4 : Notification (< 10 secondes)
- Poster sur Teams (webhook + MessageCard)
- Liens cliquables : "Créer Bug", "Voir Build"
- Mettre à jour dashboard

### Debouncing
- Même pipeline + même signature = 1 notification / 30 min max
- Compteur d'occurrences affiché si > 1

### Schéma de données (MVP simplifié)

```sql
CREATE TABLE diagnostic_log (
    id INTEGER PRIMARY KEY,
    -- Contexte pipeline
    pipeline_id TEXT NOT NULL,
    pipeline_name TEXT,
    build_id TEXT NOT NULL,
    build_url TEXT,
    -- Erreur
    error_category TEXT,        -- 'compilation', 'test', 'package', 'deployment', 'timeout', 'resource'
    error_signature TEXT,       -- Fingerprint pour déduplication
    error_excerpt TEXT,         -- Extrait de log (500 chars max)
    -- Diagnostic
    diagnosis_text TEXT,
    confidence_score REAL DEFAULT 0.5,  -- Usage interne uniquement
    -- Contexte
    commit_id TEXT,
    commit_author TEXT,
    branch_name TEXT,
    files_changed TEXT,         -- JSON array
    -- Actions
    teams_notified BOOLEAN DEFAULT FALSE,
    bug_created BOOLEAN DEFAULT FALSE,
    bug_id TEXT,
    -- Feedback
    feedback TEXT,              -- 'useful', 'not_useful', 'partial', NULL
    feedback_comment TEXT,
    -- Timestamps
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    diagnosed_at TIMESTAMP,
    notified_at TIMESTAMP,
    feedback_at TIMESTAMP,
    -- Debouncing
    notification_group_id TEXT,
    occurrence_count INTEGER DEFAULT 1
);

CREATE INDEX idx_debounce ON diagnostic_log(pipeline_id, error_signature, detected_at);
CREATE INDEX idx_pipeline ON diagnostic_log(pipeline_id, detected_at DESC);
```

### Catégories d'erreurs supportées

| Catégorie | Signatures | Sévérité |
|-----------|------------|----------|
| `compilation` | `error CS`, `error TS`, `MSB`, `Build FAILED` | Haute |
| `test` | `Test Run Failed`, `FAIL:`, `Assert.` | Moyenne |
| `package` | `NuGet`, `npm ERR`, `Unable to resolve` | Moyenne |
| `deployment` | `Deployment failed`, `503 Service` | Haute |
| `timeout` | `timeout`, `Job timed out` | Moyenne |
| `resource` | `Connection refused`, `ECONNREFUSED` | Haute |

### Intégration Teams

**MVP** : Webhook entrant + MessageCard
```json
{
  "@type": "MessageCard",
  "themeColor": "FF0000",
  "summary": "Échec Pipeline",
  "potentialAction": [
    {
      "@type": "OpenUri",
      "name": "Créer Bug",
      "targets": [{ "os": "default", "uri": "https://dev.azure.com/...?[System.Title]=..." }]
    }
  ]
}
```

**V2** : Adaptive Cards via Power Automate (boutons interactifs)

### Logique d'assignation du bug

1. Owner explicite du pipeline (si configuré)
2. Auteur du fichier en erreur (via git blame)
3. Auteur du dernier commit (si humain, exclure bots)
4. Non assigné (si doute)

### Flux "Créer Bug"

Le bot ne crée PAS le bug. Il fournit un lien pré-rempli :
```
Clic "Créer Bug" → Ouvre ADO avec formulaire pré-rempli → Humain valide/modifie → Bug créé par l'humain
```

## Alternatives rejetées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Création automatique de bug | Trop risqué, perte de contrôle humain |
| Schéma DB normalisé (4 tables) | Over-engineering pour MVP |
| Score confiance affiché | UX confuse, utilité non prouvée |
| Relance automatique des builds | Interdit par contrainte projet |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Qualité diagnostic LLM variable | Moyen | Affiner prompt en pilote, feedback loop |
| Debouncing 30min mal calibré | Faible | Paramètre configurable |
| Adoption utilisateurs | Moyen | Mesurer taux de clic, itérer sur UX |

## Conséquences

### Positives
- Humain garde le contrôle total
- Apprentissage via feedback explicite
- Diagnostic enrichi par historique pipeline

### Négatives
- Intégration Teams hors MCP (webhook manuel)
- Nécessite calibration en pilote
- Bug non créé automatiquement (friction volontaire)

## Métriques de succès

| Métrique | Cible |
|----------|-------|
| Précision diagnostic | > 80% |
| Taux feedback positif | > 70% |
| Taux création bug | 40-60% |
| Temps diagnostic total | < 3 min |

## Historique du débat

### Session
Date : 2026-04-16
Participants : ARCHITECTE, DEVOPS, RECHERCHE, CRITIQUE
Workflow : WF-DESIGN-ARCHI

### Score Critique
- Initial : 3/5
- Final : 4/5 (après intégration des révisions)

### Points clés du débat
1. **Schéma DB** : Simplifié de 4 tables à 1 table pour MVP
2. **Bouton bug** : Clarifié comme lien pré-rempli (pas création auto)
3. **Score confiance** : Masqué à l'utilisateur (usage interne)
4. **Debouncing** : Ajouté pour éviter notification fatigue
5. **Assignation** : Logique hiérarchique intelligente

## Références
- ADR-006 : Mémoire par Pipeline
- ADR-004 : Canal Teams
- Session de débat : 2026-04-16
