# ADR-018 : Collecte Azure DevOps — Webhook + Polling Fallback

**Statut** : Accepté  
**Date** : 2026-04-23  
**Auteur** : Débat WF-DESIGN-ARCHI

## Contexte

Azure DevOps supporte les webhooks pour notifier les changements de statut des builds. Cependant, les webhooks peuvent échouer (réseau, configuration, timeout). Un mécanisme de fallback est nécessaire pour garantir qu'aucun incident n'est manqué.

## Décision

**Webhook ADO en primaire + Polling APScheduler en fallback (15 min)**

### Architecture

```
Azure DevOps
    │
    ├─ Webhook ──────────────────→ FastAPI /webhook/ado
    │                                ↓
    │                           Insert incident DB
    │                                ↓
    │                           Trigger LangGraph Read node
    │
    └─ APScheduler (fallback) ──→ MCP list_builds(failed, last 15min)
                                   ↓
                              Dedup vs webhook incidents
                                   ↓
                              Create missing incidents
```

### Déduplication

- Clé unique : `build_id` (ADO)
- `INSERT OR IGNORE INTO incidents (build_id, source) VALUES (?, 'webhook')`
- Le polling fallback utilise `source = 'polling'`

### Webhook Handler

```python
@app.post("/webhook/ado")
async def handle_ado_webhook(payload: dict):
    build_id = payload["resource"]["id"]
    status = payload["resource"]["result"]

    if status == "failed":
        existing = db.fetch("SELECT id FROM incidents WHERE build_id = ?", build_id)
        if not existing:
            db.execute(
                "INSERT INTO incidents (build_id, source, status) VALUES (?, 'webhook', 'new')",
                build_id
            )
            await trigger_rpae_read(build_id)

    return {"status": "ok"}
```

### Polling Fallback

```python
scheduler.add_job(
    poll_ado_builds,
    'interval',
    minutes=15,
    id='ado_build_polling',
    max_instances=1,
    misfire_grace_time=300
)
```

## Conséquences

- Webhook ADO doit être configuré dans l'organisation Isagri
- Table incidents avec contrainte UNIQUE sur build_id
- Polling fallback = 15min (compromis latence/charge API)
- Champ `source` pour tracer webhook vs polling

## Alternatives

| Option | Avantages | Inconvénients | Décision |
|--------|-----------|---------------|----------|
| Webhook seul | Instantané | Peut échouer silencieusement | Rejeté |
| Polling seul | Fiable | Latence 15min | Rejeté |
| **Webhook + Polling** | Best of both | Plus complexe | **CHOISI** |
| Polling 1min | Réactif | Trop d'appels API | Rejeté |

## Références

- ADR-002 : MCP comme protocole
- ADR-009 : Système diagnostic read-only
