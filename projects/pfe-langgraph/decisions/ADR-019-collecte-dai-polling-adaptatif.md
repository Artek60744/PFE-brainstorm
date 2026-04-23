# ADR-019 : Collecte Digital.ai Release — Polling Adaptatif

**Statut** : Accepté  
**Date** : 2026-04-23  
**Auteur** : Débat WF-DESIGN-ARCHI

## Contexte

Digital.ai Release ne supporte pas les webhooks. Le polling est la seule option. Un intervalle fixe (60s dans ADR-014) est inefficace : 99% des polls ne trouvent rien en période calme, mais 60s est trop lent pendant un incident.

## Décision

**Polling adaptatif avec intervalles dynamiques stockés dans SQLite**

### Intervalles

| État | Intervalle | Déclencheur | Retour normal |
|------|------------|-------------|---------------|
| **Normal** | 5 min | Défaut | — |
| **Incident ADO détecté** | 15s | Incident créé il y a < 10 min | 10 min sans incident |
| **Release DAI en cours** | 30s | `list_releases()` retourne IN_PROGRESS | Release terminée |
| **Off-peak (20h-7h)** | 10 min | Heure | Retour à 7h |
| **Circuit breaker ouvert** | 5 min | 3 erreurs MCP consécutives | 5 polls réussis |

### State Table

```sql
CREATE TABLE dai_polling_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    current_interval_seconds INTEGER DEFAULT 300,
    last_incident_at DATETIME,
    consecutive_errors INTEGER DEFAULT 0,
    last_poll_at DATETIME,
    last_release_snapshot TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Logique d'adaptation

```python
async def adjust_dai_polling_interval():
    state = db.fetch("SELECT * FROM dai_polling_state WHERE id = 1")
    hour = datetime.now().hour

    if hour >= 20 or hour < 7:
        return 600  # 10 min off-peak

    if state["last_incident_at"]:
        minutes_since = (datetime.now() - state["last_incident_at"]).total_seconds() / 60
        if minutes_since < 10:
            return 15  # 15s pendant 10 min

    releases = await mcp_dai.list_releases(status="IN_PROGRESS")
    if releases:
        return 30  # 30s si release active

    if state["consecutive_errors"] >= 3:
        return 300  # 5 min en cas d'erreurs

    return 300  # 5 min normal
```

### Déduplication

```sql
CREATE TABLE dai_releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    release_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255),
    status VARCHAR(30),
    last_polled_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT OR REPLACE INTO dai_releases (release_id, title, status)
VALUES (?, ?, ?);
```

## Conséquences

- Table `dai_polling_state` créée au startup (singleton)
- Job APScheduler reschedulé dynamiquement
- Déduplication par `release_id`
- Circuit breaker : reset après 5 polls réussis

## Alternatives

| Option | Avantages | Inconvénients | Décision |
|--------|-----------|---------------|----------|
| Polling fixe 60s (ADR-014) | Simple | 99% polls inutiles | Rejeté |
| Polling fixe 5min | Économe | Trop lent en incident | Rejeté |
| **Polling adaptatif** | Efficace + réactif | Plus complexe | **CHOISI** |
| Redis pour state | Persistant | Dépendance externe | Rejeté |

## Références

- ADR-014 : Polling DAI (superseded)
- ADR-002 : MCP comme protocole
