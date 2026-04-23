# ADR-001 : ~~OpenClaw~~ LangGraph comme Framework Agent

## Statut
**Superseded** — Remplacé par [ADR-017](ADR-017-remplacement-openclaw-langgraph.md) (23 avril 2026)

**Raison** : Politique entreprise bloque OpenClaw et n8n. LangGraph + APScheduler choisis comme alternative.

## Date
Janvier 2024

## Contexte
Le projet nécessite un framework d'agent IA capable de :
- Surveiller des systèmes en continu (heartbeat)
- Maintenir une mémoire persistante des incidents
- S'intégrer avec des outils externes via des protocoles standards
- Être open-source pour la reproductibilité académique

## Décision
Utiliser **OpenClaw** comme framework principal pour l'agent IA.

## Justification

### Avantages
| Critère | OpenClaw | Alternatives (LangChain, n8n) |
|---------|----------|-------------------------------|
| Mémoire persistante | Native | À implémenter |
| Heartbeat | Natif | Non disponible |
| Open-source | Oui | Oui (partiel pour n8n) |
| Pattern RPAE | Compatible | À adapter |

### Pourquoi pas n8n ?
n8n est un outil d'orchestration **réactive** (déclenché par événements), alors qu'OpenClaw est un agent **proactif** avec heartbeat. Pour surveiller des pipelines en continu, OpenClaw est plus adapté.

### Pourquoi pas LangChain/LangGraph ?
LangChain offre plus de contrôle mais nécessite plus de développement custom. OpenClaw apporte une valeur différenciante pour le PFE avec ses fonctionnalités natives.

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Projet jeune, potentiellement instable | POC validé en semaine 1 |
| Documentation limitée | Contribution à la documentation |
| Communauté restreinte | Fallback LangChain si nécessaire |

## Conséquences
- ~~L'architecture est construite autour d'OpenClaw~~ → **Voir ADR-017**
- ~~L'équipe doit monter en compétence sur OpenClaw~~ → **LangGraph à la place**
- ~~La documentation du projet contribuera à l'écosystème OpenClaw~~ → **Écosystème LangChain/LangGraph**

## Alternatives considérées
| Alternative | Raison du rejet |
|-------------|-----------------|
| n8n | Réactif, pas de heartbeat natif |
| LangChain + CrewAI | Plus de travail custom, moins de valeur différenciante |
| Agent custom | Temps de développement trop long |

## Références
- Discussion : AGENT-ARCHITECTE, AGENT-CRITIQUE
- Validation : Tuteur entreprise
