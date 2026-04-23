# ADR-012 : Dashboard sans Token ADO (Trust Boundary)

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
Dashboard permet création bug ADO. Deux approches :
1. **Dashboard avec token** : Appelle MCP directement
2. **Dashboard sans token** : Demande à OpenClaw de créer

Enjeu sécurité : Si dashboard compromis, que peut faire l'attaquant ?

## Décision

**Dashboard SANS token ADO. Création bug via OpenClaw uniquement.**

### Architecture Trust Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                    ZONE PRIVILÉGIÉE                         │
│  ┌─────────────┐                                           │
│  │  OpenClaw   │  - Token ADO (read+write)                 │
│  │             │  - Token Digital.ai Release               │
│  │             │  - Accès MCP complet                      │
│  └──────┬──────┘                                           │
│         │ API interne (localhost:8001)                     │
├─────────┼───────────────────────────────────────────────────┤
│         │           ZONE DMZ                               │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │  Dashboard  │  - Read SQLite (incidents)                │
│  │  (FastAPI)  │  - NO token ADO                           │
│  │             │  - Auth utilisateur (bearer/SSO)          │
│  └──────┬──────┘                                           │
│         │ HTTPS (port 443)                                 │
├─────────┼───────────────────────────────────────────────────┤
│         │           ZONE EXTERNE                           │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │   Browser   │  - Utilisateur authentifié                │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Flux création bug

```
User click "Créer Bug"
        │
        ▼
Dashboard POST /incidents/{id}/create-bug
        │
        │  (validate user auth + rate limit)
        ▼
Dashboard → OpenClaw POST localhost:8001/actions/create-bug
        │
        │  (OpenClaw vérifie incident existe, prépare payload)
        ▼
OpenClaw → MCP wit_create_work_item
        │
        ▼
Bug créé, ID retourné
        │
        ▼
Dashboard update UI "Bug #1234 créé"
```

### Endpoints OpenClaw (API interne)

```python
# Exposé sur localhost:8001 uniquement
@app.post("/actions/create-bug")
async def create_bug(incident_id: str, user_id: str):
    """
    Crée bug ADO pour incident donné.
    - Valide incident existe
    - Récupère diagnostic
    - Appelle MCP
    - Log audit
    """
    incident = await get_incident(incident_id)
    if not incident:
        raise HTTPException(404)
    
    bug_id = await mcp_create_work_item(
        title=f"[OPENCLAW] {incident.pipeline_name} - {incident.error_category}",
        description=incident.diagnosis_text,
        # ... autres champs
    )
    
    await log_audit(
        action="create_bug",
        incident_id=incident_id,
        bug_id=bug_id,
        user_id=user_id
    )
    
    return {"bug_id": bug_id}
```

### Contrôles sécurité

| Contrôle | Implémentation |
|----------|----------------|
| Auth dashboard | Bearer token ou SSO Isagri |
| Rate limit création | Max 10 bugs/heure/utilisateur |
| API interne | localhost only (pas exposé) |
| Audit | Chaque création loggée avec user_id |
| Validation | Incident doit exister avant création |

## Alternatives rejetées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Dashboard avec token ADO | Surface d'attaque trop grande |
| Token read-only dashboard | Création bug nécessite write |
| Proxy MCP dans dashboard | Même risque que token direct |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| OpenClaw SPOF | Haut | Healthcheck, restart auto |
| Latence API interne | Faible | localhost = négligeable |

## Conséquences

### Positives
- Dashboard compromis = read-only max
- Audit centralisé dans OpenClaw
- Tokens isolés dans zone privilégiée

### Négatives
- Dépendance OpenClaw pour créer bugs
- Un hop supplémentaire

## Références
- ADR-004 : Canal Teams
- ADR-007 : Dry-run obligatoire
- Session de débat : 2026-04-21
