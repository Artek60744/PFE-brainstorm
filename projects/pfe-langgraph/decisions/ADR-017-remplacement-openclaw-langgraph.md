# ADR-017 : Remplacement OpenClaw par LangGraph

## Statut
**Accepté** — Décision post-audit politique entreprise

## Date
23 avril 2026

## Contexte
La politique d'entreprise Isagri bloque l'utilisation d'OpenClaw et n8n comme frameworks d'agent IA. Le projet PFE doit continuer avec une alternative qui préserve :
- Le pattern RPAE (Read-Plan-Approve-Execute)
- Le heartbeat natif (monitoring continu des pipelines)
- La mémoire persistante (contexte par pipeline)
- L'intégration MCP (Azure DevOps + Digital.ai Release)
- L'approbation via Teams
- Le mode dry-run obligatoire
- Le dashboard FastAPI + HTMX
- La trust boundary (ADR-012 : dashboard sans token ADO)

Un débat a été mené dans le projet `pfe-no-openclaw` avec les agents Architecte, DevOps, Sécurité et Critique.

## Décision
**Remplacer OpenClaw par LangGraph + APScheduler**

Stack technique mise à jour :
| Composant | Avant (OpenClaw) | Nouveau (LangGraph) |
|-----------|------------------|---------------------|
| Agent Framework | OpenClaw | LangGraph |
| Orchestration RPAE | Workflows OpenClaw | LangGraph StateGraph |
| Heartbeat | Natif OpenClaw | APScheduler |
| Mémoire persistante | Mémoire OpenClaw | LangGraph SqliteSaver/PostgresSaver |
| MCP | MCP SDK Python | MCP SDK Python (inchangé) |
| Database | SQLite → PostgreSQL | SQLite → PostgreSQL (inchangé) |
| Dashboard | FastAPI + HTMX | FastAPI + HTMX (inchangé) |
| Communication | Teams | Teams (inchangé) |

## Justification

### Alternatives évaluées

| Alternative | Score | Pourquoi rejetée |
|-------------|-------|------------------|
| **LangGraph seul** | **4.5/5** | **CHOISI** — Parfait pour RPAE séquentiel, persistance native, moins de deps |
| CrewAI + LangGraph | 4/5 | CrewAI overkill pour workflow séquentiel (ADR-013) |
| AutoGen | 3/5 | Trop complexe, mémoire moins structurée |
| FastAPI pur + statemachine | 3/5 | Perd le côté "agent IA", trop de boilerplate |

### Pourquoi LangGraph ?

1. **StateGraph natif** — Le pattern RPAE est un workflow séquentiel (Read → Plan → Approve → Execute), exactement ce que LangGraph modélise
2. **Persistance intégrée** — `SqliteSaver` et `PostgresSaver` remplacent la mémoire OpenClaw sans code custom
3. **Moins de dépendances** — CrewAI ajoute de la complexité inutile pour un workflow séquentiel
4. **MCP indépendant** — Le SDK Python MCP fonctionne quel que soit le framework agent
5. **Python natif** — Pas de runtime externe, s'intègre directement dans le dashboard FastAPI
6. **Open-source** — LangChain/LangGraph = MIT license, pas de risque politique

### Ce qui est préservé (95%)

- ✅ Pattern RPAE (via StateGraph nodes)
- ✅ Mémoire persistante (via checkpointer natif)
- ✅ Intégration MCP (SDK Python inchangé)
- ✅ Approbation Teams (webhooks inchangés)
- ✅ Dry-run (implémentable dans chaque node)
- ✅ Dashboard FastAPI + HTMX (inchangé)
- ✅ Trust boundary ADR-012 (inchangé)
- ✅ Diagnostic séquentiel ADR-013 (cohérent avec LangGraph)

### Ce qui change

- ⚠️ Heartbeat n'est plus natif → APScheduler à configurer (léger, bien documenté)
- ⚠️ Multi-agent conversationnel remplacé par nodes séquentiels (cohérent avec ADR-013)
- ⚠️ Pas de "agent framework" avec personality — acceptable pour un PFE

## Risques acceptés

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| LangGraph moins "agent IA" que OpenClaw | Moyen | Faible | Le PFE évalue le pattern RPAE, pas le framework |
| APScheduler moins robuste que heartbeat natif | Moyen | Faible | APScheduler = mature, utilisé en production depuis 2014 |
| Courbe d'apprentissage LangGraph | Faible | Faible | Documentation LangChain excellente, communauté active |
| Checkpointer SQLite limités en concurrence | Moyen | Faible | MVP = mono-utilisateur, PostgreSQL en V2 |

## Conséquences

- L'architecture est reconstruite autour de LangGraph StateGraph
- Le code OpenClaw spécifique est remplacé par des nodes LangGraph
- Le heartbeat est implémenté via APScheduler dans FastAPI
- La mémoire persistante utilise le checkpointer LangGraph
- Tous les ADRs existants restent valides (sauf ADR-001 qui est superseded)
- Le nom du projet change : `pfe-openclaw` → `pfe-langgraph`

## Alternatives considérées

| Alternative | Raison du rejet |
|-------------|-----------------|
| OpenClaw | Bloqué par politique entreprise |
| n8n | Bloqué par politique entreprise + réactif (pas de heartbeat) |
| CrewAI + LangGraph | Overkill pour workflow séquentiel |
| AutoGen | Trop complexe, mémoire moins structurée |
| FastAPI pur + statemachine | Perd le côté "agent IA", trop de boilerplate |
| LangChain seul (sans Graph) | Moins adapté au workflow séquentiel RPAE |

## Références

- Débat alternatif : `projects/pfe-no-openclaw/` (session brainstorming)
- ADR-001 : Superseded par cette décision
- ADR-013 : Diagnostic séquentiel (cohérent avec LangGraph StateGraph)
- ADR-012 : Trust boundary (inchangé)
- MCP-CONFIGURATION.md : Configuration MCP (inchangée)
