# ADR-014 : Polling Digital.ai Release (60s)

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
Digital.ai Release = pas de webhook. ADO a webhooks, DAI non.
Besoin : détecter releases FAILED/PAUSED/BLOCKED pour diagnostic.

Options :
1. Polling périodique via MCP
2. Intégration event-driven (inexistante)
3. Webhook custom côté DAI (pas supporté)

## Décision

**Polling MCP 60s avec mode adaptatif**

### Intervalles

| Mode | Intervalle | Condition |
|------|------------|-----------|
| Normal | 60s | Défaut |
| Incident actif | 15s | Release FAILING/FAILED détectée |
| Heures creuses | 5min | 22h-6h + weekends |

### Implémentation

```python
DAI_POLL_INTERVALS = {
    "normal": 60,
    "incident": 15,
    "quiet": 300
}

async def get_poll_interval() -> int:
    """Détermine intervalle polling."""
    # Incident actif = mode rapide
    if await has_active_dai_incident():
        return DAI_POLL_INTERVALS["incident"]
    
    # Heures creuses
    hour = datetime.now().hour
    if hour < 6 or hour >= 22:
        return DAI_POLL_INTERVALS["quiet"]
    
    return DAI_POLL_INTERVALS["normal"]
```

### Outils MCP utilisés

| Tool | Fréquence | Usage |
|------|-----------|-------|
| `list_releases(active=True, failing=True)` | Chaque poll | Détection nouvelles releases problématiques |
| `get_release(id)` | Sur incident | Détails phases/tasks pour diagnostic |
| `get_activity_logs(id)` | Sur incident | Historique actions pour root cause |
| `count_releases` | 5min | Metrics dashboard |

### Circuit breaker

```python
DAI_CIRCUIT_BREAKER = {
    "failure_threshold": 3,      # 3 échecs consécutifs
    "recovery_timeout": 300,     # 5min avant retry
    "half_open_requests": 1      # 1 requête test
}
```

Si DAI indisponible 3x → circuit open → alerte Teams → retry après 5min.

### Charge estimée

| Releases actives | Appels/heure | Acceptable |
|------------------|--------------|------------|
| 5 | 60 + 5×2 = 70 | ✅ |
| 20 | 60 + 20×2 = 100 | ✅ |
| 50 | 60 + 50×2 = 160 | ⚠️ Optimiser |

## Alternatives rejetées

| Alternative | Raison |
|-------------|--------|
| Webhook DAI | Pas supporté |
| Polling 10s | Charge excessive, pas nécessaire pour releases |
| Polling 5min | Latence trop haute pour incidents |

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Rate limit DAI | Haut | Circuit breaker + backoff exponentiel |
| Latence 60s | Faible | Acceptable pour releases (vs builds) |
| DAI API instable | Moyen | Fallback mode dégradé, alerte ops |

## Conséquences

### Positives
- Détection releases problématiques < 2min (worst case)
- Charge maîtrisée
- Mode adaptatif selon contexte

### Négatives
- Pas temps réel (acceptable pour releases)
- Dépendance stabilité API DAI

## Métriques

| Métrique | Cible |
|----------|-------|
| Latence détection | < 90s (p95) |
| Appels DAI/heure | < 200 |
| Disponibilité polling | > 99% |

## Références
- ADR-002 : Protocole MCP
- ADR-015 : Pas de corrélation ADO↔DAI
- Débat : 2026-04-21
