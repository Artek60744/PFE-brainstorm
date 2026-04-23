# ADR-020 : Refresh Dashboard — HTMX Polling Adaptatif + BroadcastChannel

**Statut** : Accepté  
**Date** : 2026-04-23  
**Auteur** : Débat WF-DESIGN-ARCHI

## Contexte

Le dashboard doit afficher les incidents et releases en temps quasi-réel. L'ADR-011 spécifiait un polling HTMX toutes les 3s, mais cette approche pose des problèmes :
- **Charge serveur** : 3s × N tabs = requêtes inutiles
- **UX** : Flickering si le DOM change trop souvent
- **Inefficacité** : La plupart des polls ne retournent aucun changement

## Décision

**HTMX polling adaptatif (3 niveaux) + BroadcastChannel API pour coordination multi-tab**

### Fréquences

| État | Intervalle | Déclencheur | Retour normal |
|------|------------|-------------|---------------|
| **Normal** | 10s | Défaut | — |
| **Incident actif** | 3s | ≥1 incident `new` ou `diagnostic_ready` | 2 min sans incident |
| **Idle** | 30s | Aucun changement > 2 min | Nouvel incident ou interaction |

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                      BROWSER                         │
│                                                      │
│  Tab 1 (active)          Tab 2, 3... (background)   │
│  ┌──────────────────┐    ┌──────────────────────┐  │
│  │ HTMX polling     │    │ BroadcastChannel     │  │
│  │ adaptatif        │───→│ .onmessage=updateUI  │  │
│  │ + postMessage    │    │ (pas de polling)     │  │
│  └──────────────────┘    └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓ hx-get
┌─────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                    │
│                                                      │
│  GET /api/incidents                                 │
│  1. Vérifier cache (TTL 5s)                          │
│  2. Si cache miss → query SQLite                     │
│  3. Retourner JSON + X-Poll-Interval header          │
│                                                      │
│  Cache in-memory (dict, TTL 5s)                      │
│  → Évite DB hammer si 50 tabs poll en même temps    │
└─────────────────────────────────────────────────────┘
```

### Implémentation HTMX

```html
<div id="incidents-list"
     hx-get="/api/incidents"
     hx-trigger="every 10s"
     hx-swap="innerHTML">
</div>

<script>
let currentInterval = 10000;
let noChangeCount = 0;

function adjustPollingInterval(data) {
    const hasActiveIncident = data.incidents.some(
        i => ['new', 'diagnostic_ready'].includes(i.status)
    );

    if (hasActiveIncident) {
        setPollingInterval(3000);
        noChangeCount = 0;
    } else if (data.unchanged) {
        noChangeCount++;
        if (noChangeCount >= 12) { // 2 min
            setPollingInterval(30000);
        }
    } else {
        noChangeCount = 0;
        if (currentInterval > 10000) {
            setPollingInterval(10000);
        }
    }
}

function setPollingInterval(ms) {
    if (ms === currentInterval) return;
    currentInterval = ms;
    document.querySelectorAll('[hx-trigger*="every"]').forEach(el => {
        el.setAttribute('hx-trigger', `every ${ms/1000}s`);
        htmx.process(el);
    });
}

// BroadcastChannel : coordination multi-tab
const channel = new BroadcastChannel('dashboard_sync');
const isPrimary = !sessionStorage.getItem('dashboard_secondary');

if (isPrimary) {
    document.body.addEventListener('htmx:afterOnLoad', (evt) => {
        if (evt.detail.pathInfo?.path === '/api/incidents') {
            channel.postMessage(JSON.parse(evt.detail.xhr.responseText));
        }
    });
} else {
    document.querySelectorAll('[hx-trigger*="every"]').forEach(el => {
        el.removeAttribute('hx-trigger');
    });
    channel.onmessage = (event) => updateUI(event.data);
}

sessionStorage.setItem('dashboard_primary', 'true');
</script>
```

### Backend FastAPI

```python
_cache: dict = {}
_CACHE_TTL = 5

@app.get("/api/incidents")
async def get_incidents():
    now = time.time()

    if "incidents" in _cache:
        data, timestamp = _cache["incidents"]
        if now - timestamp < _CACHE_TTL:
            has_active = any(
                i["status"] in ("new", "diagnostic_ready")
                for i in data["incidents"]
            )
            interval = 3 if has_active else 10
            return JSONResponse(
                content=data,
                headers={"X-Poll-Interval": str(interval)}
            )

    incidents = db.fetchall("SELECT * FROM incidents ORDER BY created_at DESC LIMIT 50")
    data = {"incidents": incidents, "unchanged": False}
    _cache["incidents"] = (data, now)
    return data
```

## Conséquences

- ADR-011 (polling 3s fixe) est **superseded**
- Backend nécessite cache in-memory (TTL 5s)
- Frontend nécessite JS custom pour polling adaptatif + BroadcastChannel
- Tabs secondaires ne pollent pas (économie ressources)

## Alternatives

| Option | Avantages | Inconvénients | Décision |
|--------|-----------|---------------|----------|
| Polling fixe 3s (ADR-011) | Simple | Charge inutile, flickering | Rejeté |
| **HTMX adaptatif + BroadcastChannel** | Optimisé, natif | JS custom nécessaire | **CHOISI** |
| SSE | Temps réel sub-second | Custom JS, overkill MVP | Rejeté |
| WebSocket | Bidirectionnel | Complexité ×3, inutile read-only | Rejeté |

## Références

- ADR-011 : Polling HTMX 3s (superseded)
- ADR-010 : FastAPI + HTMX
- ADR-018 : Collecte ADO
- ADR-019 : Collecte DAI
