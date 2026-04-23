# ADR-011 : Polling HTMX plutôt que SSE/WebSocket

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
Dashboard doit afficher incidents en temps quasi-réel. Options :
- **WebSocket** : Bidirectionnel, connexion persistante
- **SSE** (Server-Sent Events) : Unidirectionnel serveur→client
- **Polling** : Requêtes périodiques client→serveur

## Décision

**Polling HTMX avec `hx-trigger="every 3s"`**

### Raisons

| Critère | WebSocket | SSE | Polling 3s |
|---------|-----------|-----|------------|
| Complexité serveur | Haute | Moyenne | Basse |
| Reconnexion auto | Manuel | Natif | N/A |
| Firewall/proxy | Problèmes possibles | OK | OK |
| Load balancer | Sticky sessions | Sticky sessions | Stateless |
| Code HTMX | Custom JS | Custom JS | Natif |
| Latence max | ~0s | ~0s | 3s |

### Implémentation

```html
<!-- Auto-refresh liste incidents -->
<div hx-get="/api/incidents" 
     hx-trigger="every 3s"
     hx-swap="innerHTML">
  <!-- Content remplacé automatiquement -->
</div>

<!-- Refresh conditionnel (stop quand status=ready) -->
<div hx-get="/api/incidents/{{ id }}/status"
     hx-trigger="every 3s[status != 'ready']">
</div>
```

### Optimisations

1. **ETag/304** : Serveur renvoie `304 Not Modified` si rien changé
2. **Partial HTML** : Retourner uniquement le fragment, pas la page
3. **Backoff** : Si erreur, HTMX retry avec backoff automatique

```python
@app.get("/api/incidents")
async def list_incidents(request: Request):
    incidents = await get_incidents()
    etag = compute_etag(incidents)
    
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)
    
    return templates.TemplateResponse(
        "partials/incident_list.html",
        {"incidents": incidents},
        headers={"ETag": etag}
    )
```

### Calcul charge

| Clients | Requêtes/min | Requêtes/sec |
|---------|--------------|--------------|
| 5 | 100 | 1.7 |
| 20 | 400 | 6.7 |
| 50 | 1000 | 16.7 |

→ Acceptable pour MVP. Si > 50 clients, migrer vers SSE.

## Alternatives rejetées

| Alternative | Raison du rejet |
|-------------|-----------------|
| WebSocket | Over-engineering, gestion connexions complexe |
| SSE | Nécessite code custom JS, reconnexion à gérer |
| Long polling | Plus complexe que polling simple |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Latence 3s | Faible | Acceptable pour monitoring |
| Charge si beaucoup clients | Moyen | ETag + 304, migration SSE si besoin |

## Conséquences

### Positives
- Zéro JS custom
- Stateless (facile à scale)
- Debug facile (requêtes HTTP standard)
- HTMX gère retry/erreurs

### Négatives
- Latence max 3s (pas instant)
- Charge linéaire avec nombre clients

## Références
- ADR-010 : FastAPI + HTMX
- Session de débat : 2026-04-21
