# ADR-015 : Pas de Corrélation ADO↔DAI pour MVP

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
Pipeline ADO peut déclencher release DAI. Release DAI peut dépendre de builds ADO.
Question : corréler automatiquement les incidents cross-platform ?

Exemple :
```
ADO Pipeline "Backend-Build" → trigger → DAI Release "Deploy-Prod"
                                              │
                                              └── Task fails
```

Corrélation = lier incident DAI à build ADO source.

## Décision

**Pas de corrélation automatique ADO↔DAI pour MVP. Flux séparés.**

### Raisons

| Complexité | Effort | Valeur MVP |
|------------|--------|------------|
| Mapping pipeline→template | 2-3 jours | Faible |
| Parsing trigger chains | 3-5 jours | Faible |
| UI corrélation | 2 jours | Faible |
| **Total** | **7-10 jours** | **Faible** |

MVP focus = réduire MTTR. Corrélation = nice-to-have.

### Architecture MVP

```
┌─────────────────────────────────────────────────────────────┐
│                    MVP : FLUX SÉPARÉS                       │
└─────────────────────────────────────────────────────────────┘

  ADO Incidents                    DAI Incidents
       │                                │
       │                                │
       ▼                                ▼
  ┌─────────────┐                 ┌─────────────┐
  │ Table:      │                 │ Table:      │
  │ incidents   │                 │ dai_incidents│
  │ (source=ado)│                 │ (source=dai)│
  └──────┬──────┘                 └──────┬──────┘
         │                               │
         └───────────┬───────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │ Dashboard   │
              │ (2 onglets) │
              └─────────────┘
```

### Dashboard UX

```
┌─────────────────────────────────────────────┐
│  [Pipelines ADO] [Releases DAI]  ← tabs     │
├─────────────────────────────────────────────┤
│  Liste incidents selon onglet actif         │
└─────────────────────────────────────────────┘
```

### V2 : Corrélation future

Si besoin post-MVP :

```python
# V2 : Table de mapping explicite
CREATE TABLE ado_dai_mapping (
    ado_pipeline_id TEXT,
    dai_template_id TEXT,
    relation_type TEXT,  -- 'triggers', 'depends_on'
    PRIMARY KEY (ado_pipeline_id, dai_template_id)
);

# V2 : Query corrélation
SELECT i.*, d.*
FROM incidents i
JOIN ado_dai_mapping m ON i.pipeline_id = m.ado_pipeline_id
JOIN dai_incidents d ON d.template_id = m.dai_template_id
WHERE i.detected_at BETWEEN d.start_date AND d.end_date;
```

## Alternatives rejetées

| Alternative | Raison |
|-------------|--------|
| Corrélation auto par nom | Conventions nommage pas fiables |
| Corrélation par timestamp | Trop de faux positifs |
| Parsing DAI triggers | API complexe, effort disproportionné |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| User perd contexte cross-platform | Moyen | Liens manuels dans diagnostic |
| Diagnostic incomplet | Faible | Humain peut naviguer ADO↔DAI |

## Conséquences

### Positives
- MVP livrable plus tôt (-7 jours)
- Complexité réduite
- Moins de bugs potentiels

### Négatives
- Pas de vue unifiée incident
- Navigation manuelle entre plateformes

## Roadmap

| Version | Fonctionnalité |
|---------|----------------|
| MVP | Flux séparés, 2 onglets dashboard |
| V1.1 | Mapping manuel ADO↔DAI (config YAML) |
| V2 | Corrélation auto par triggers |

## Références
- ADR-014 : Polling DAI
- Débat : 2026-04-21
