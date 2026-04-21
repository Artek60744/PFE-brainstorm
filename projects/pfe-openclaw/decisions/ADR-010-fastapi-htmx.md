# ADR-010 : FastAPI + HTMX plutôt que Streamlit

## Statut
**Accepté**

## Date
Avril 2026

## Contexte
Dashboard MVP = requirement non négociable. Deux options techniques :
- **Streamlit** : Framework Python data-centric, rapide à prototyper
- **FastAPI + HTMX** : API REST + templating HTML avec interactivité côté serveur

Besoins dashboard :
- Afficher liste incidents en temps quasi-réel
- Afficher diagnostic OpenClaw (Markdown)
- Permettre création bug ADO via bouton
- Rafraîchissement automatique sans reload page

## Décision

**FastAPI + HTMX + Jinja2**

### Raisons

| Critère | Streamlit | FastAPI + HTMX |
|---------|-----------|----------------|
| Temps réel | Polling constant (resource heavy) | Polling ciblé via `hx-trigger` |
| Contrôle UI | Limité (widgets prédéfinis) | Total (HTML/CSS custom) |
| Auth custom | Complexe (session hacky) | Native (middleware, OAuth) |
| API endpoints | Pas prévu | Natif |
| Deploy | Streamlit Cloud ou custom | Standard ASGI (uvicorn) |
| Intégration OpenClaw | Appel direct (couplage) | API interne (découplé) |

### Stack finale

```
┌─────────────────────────────────────┐
│           Dashboard MVP             │
├─────────────────────────────────────┤
│  FastAPI      - Routing, API        │
│  Jinja2       - Templates HTML      │
│  HTMX         - Interactivité       │
│  TailwindCSS  - Styling (optionnel) │
│  SQLite       - Read incidents      │
└─────────────────────────────────────┘
```

### Dépendances Python

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
jinja2>=3.1.0
python-multipart  # forms
aiosqlite         # async SQLite
```

## Alternatives rejetées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Streamlit | Polling constant, auth complexe, UI limitée |
| Flask + HTMX | Flask moins performant async, FastAPI meilleur pour API |
| React/Vue SPA | Over-engineering pour MVP, maintenance JS |
| Django | Trop lourd pour dashboard simple |

## Risques acceptés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| HTMX courbe apprentissage | Faible | Doc excellente, patterns simples |
| Pas de composants prêts | Moyen | TailwindUI ou DaisyUI si besoin |

## Conséquences

### Positives
- Contrôle total sur UX
- API endpoints réutilisables
- Déploiement standard
- Découplage propre avec OpenClaw

### Négatives
- Plus de code que Streamlit pour MVP initial
- Pas de widgets graphiques out-of-box (charts)

## Métriques de succès

| Métrique | Cible |
|----------|-------|
| Temps chargement page | < 500ms |
| Refresh incidents | < 100ms (partial) |
| Lignes de code dashboard | < 500 |

## Références
- ADR-005 : Dashboard MVP obligatoire
- ADR-011 : Polling HTMX vs SSE
- Session de débat : 2026-04-21
