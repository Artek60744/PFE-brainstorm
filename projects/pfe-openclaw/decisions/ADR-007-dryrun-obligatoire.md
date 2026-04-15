# ADR-007 : Dry-Run Obligatoire (Pas de Sandbox)

## Statut
**Accepté** — Contrainte critique

## Date
Janvier 2024

## Contexte
Le projet n'a **pas accès à un environnement sandbox**. Tous les tests d'écriture de l'agent doivent être effectués sur l'environnement de production Azure DevOps d'Isagri.

C'est une contrainte majeure qui nécessite des garde-fous stricts.

## Décision
Implémenter un **mode dry-run obligatoire** pour toutes les opérations d'écriture, avec les garde-fous suivants :
1. Dry-run par défaut jusqu'à validation tuteur
2. Préfixe `[OPENCLAW-TEST]` sur toutes les ressources de test
3. Validation humaine pour chaque écriture réelle

## Justification

### Contrainte
| Situation | Impact |
|-----------|--------|
| Pas de sandbox | Tests en production uniquement |
| Work items réels | Impact sur le backlog Isagri |
| Commentaires réels | Visible par toute l'équipe |

### Garde-fous implémentés

#### 1. Mode Dry-Run
```python
def execute_action(action, dry_run=True):
    if dry_run:
        log(f"[DRY-RUN] Would execute: {action}")
        return SimulatedResult(action)
    else:
        if not is_approved(action):
            raise NotApprovedError()
        return real_execute(action)
```

#### 2. Préfixe de test
| Type de ressource | Format |
|-------------------|--------|
| Work Item | `[OPENCLAW-TEST] Titre...` |
| Commentaire | `[OPENCLAW-TEST] Contenu...` |
| Branch | `openclaw-test/...` |

#### 3. Validation tuteur
| Phase | Écriture autorisée |
|-------|-------------------|
| Phase 0-1 | Dry-run uniquement |
| Après validation tuteur | Écriture avec préfixe test |
| Production | Écriture normale après approbation |

### Procédure de rollback
En cas de création accidentelle :
1. Identifier les ressources avec préfixe `[OPENCLAW-TEST]`
2. Supprimer ou archiver manuellement
3. Documenter l'incident

## Risques acceptés
| Risque | Mitigation |
|--------|------------|
| Création accidentelle | Dry-run par défaut, préfixe obligatoire |
| Commentaire inapproprié | Revue avant envoi, niveau d'approbation |
| Impact sur le vrai backlog | Area Path dédié si possible |

## Conséquences
- Développement plus lent (pas de tests libres)
- Documentation détaillée de chaque test
- Validation tuteur obligatoire avant première écriture

## Recommandations du débat

### AGENT-CRITIQUE
> "Pas de bac à sable — est-ce acceptable ?"

### Réponse
C'est une contrainte, pas un choix. Les mitigations (dry-run, préfixe, validation) réduisent le risque à un niveau acceptable pour un POC.

## Checklist avant écriture réelle

- [ ] Mode dry-run testé avec succès
- [ ] Validation tuteur obtenue
- [ ] Préfixe `[OPENCLAW-TEST]` configuré
- [ ] Area Path de test identifié
- [ ] Procédure de rollback documentée
- [ ] Équipe DevOps informée

## Références
- Discussion : AGENT-SECURITE, AGENT-CRITIQUE
- Contrainte : Environnement Isagri
