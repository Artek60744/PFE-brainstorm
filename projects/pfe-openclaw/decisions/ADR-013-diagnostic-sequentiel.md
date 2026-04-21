# ADR-013 : Diagnostic Séquentiel plutôt que Sub-Agents Parallèles

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
OpenClaw doit diagnostiquer échecs pipeline. Deux approches :
1. **Sub-agents parallèles** : Plusieurs agents travaillent simultanément
2. **Diagnostic séquentiel** : Un seul agent, étapes ordonnées

Contrainte : API LLM (OpenAI/Claude) = ressource partagée, rate limits.

## Décision

**Diagnostic séquentiel avec pipeline d'étapes pour MVP.**

### Raisons

| Critère | Sub-agents parallèles | Séquentiel |
|---------|----------------------|------------|
| Contention API LLM | Haute | Nulle |
| Débogage | Complexe (race conditions) | Simple (linéaire) |
| Coût tokens | Contexte dupliqué | Contexte partagé |
| Implémentation | Orchestration complexe | Simple async/await |
| Temps total | Plus rapide (théorique) | Prévisible |

### Pipeline de diagnostic

```
┌─────────────────────────────────────────────────────────────┐
│              PIPELINE DIAGNOSTIC SÉQUENTIEL                 │
└─────────────────────────────────────────────────────────────┘

  Étape 1: COLLECT (< 30s)
      │
      │  - Fetch logs via MCP
      │  - Fetch commit info
      │  - Fetch pipeline config
      │
      ▼
  Étape 2: EXTRACT (< 10s)
      │
      │  - Regex: lignes ERROR/FAIL/EXCEPTION
      │  - Générer fingerprint erreur
      │  - Identifier catégorie (compilation/test/deploy)
      │
      ▼
  Étape 3: CORRELATE (< 20s)
      │
      │  - Query historique même pipeline
      │  - Query historique même auteur
      │  - Identifier patterns récurrents
      │
      ▼
  Étape 4: ANALYZE (< 60s) ← LLM call
      │
      │  - Prompt avec contexte consolidé
      │  - Cause probable
      │  - Impact estimé
      │  - Recommandations
      │
      ▼
  Étape 5: FORMAT (< 10s)
      │
      │  - Générer Markdown diagnostic
      │  - Pré-remplir bug proposal
      │  - Préparer message Teams
      │
      ▼
  DONE (total < 2 min 30s)
```

### Implémentation

```python
class DiagnosticPipeline:
    async def run(self, incident_id: str) -> Diagnostic:
        # Étape 1
        await self.update_status(incident_id, "collecting")
        context = await self.collect(incident_id)
        
        # Étape 2
        await self.update_status(incident_id, "extracting")
        extracted = await self.extract(context)
        
        # Étape 3
        await self.update_status(incident_id, "correlating")
        correlated = await self.correlate(extracted)
        
        # Étape 4
        await self.update_status(incident_id, "analyzing")
        analysis = await self.analyze(correlated)  # LLM call
        
        # Étape 5
        await self.update_status(incident_id, "formatting")
        diagnostic = await self.format(analysis)
        
        await self.update_status(incident_id, "ready")
        return diagnostic
```

### Status exposés au dashboard

| Status | Description | UI |
|--------|-------------|-----|
| `detecting` | Échec détecté, pas encore traité | Spinner |
| `collecting` | Récupération logs/contexte | "Collecte..." |
| `extracting` | Extraction erreurs | "Analyse logs..." |
| `correlating` | Recherche historique | "Corrélation..." |
| `analyzing` | Appel LLM en cours | "Diagnostic IA..." |
| `formatting` | Génération output | "Finalisation..." |
| `ready` | Diagnostic disponible | Afficher résultat |
| `failed` | Erreur dans pipeline | Message erreur |

### V2 : Sub-agents conditionnels

Réservé pour V2 si besoin :
- Sub-agent "blame" : analyse git blame (long)
- Sub-agent "similar" : recherche incidents similaires autres pipelines
- Sub-agent "docs" : recherche dans wiki/docs

Condition : seulement si MVP prouve que latence est problématique.

## Alternatives rejetées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Sub-agents parallèles | Contention LLM, complexité orchestration |
| Queue de jobs (Celery) | Over-engineering pour MVP |
| Threads Python | GIL, pas de gain réel pour I/O |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Latence > 3 min | Moyen | Optimiser prompts, cacher historique |
| LLM timeout | Moyen | Retry avec backoff, timeout 60s |

## Conséquences

### Positives
- Débogage simple (logs linéaires)
- Coût tokens optimisé
- Statuts clairs pour UX
- Pas de race conditions

### Négatives
- Latence non compressible
- Pas de parallélisme (V2)

## Métriques de succès

| Métrique | Cible |
|----------|-------|
| Temps total diagnostic | < 2 min 30s |
| Temps étape LLM | < 60s |
| Taux échec pipeline | < 5% |

## Références
- ADR-009 : Système de diagnostic
- ADR-006 : Mémoire par pipeline
- Session de débat : 2026-04-21
