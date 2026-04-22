# ADR-016 : Timing d'Implémentation du Dashboard (S12 vs S7-S9 vs S13)

## Statut
**Accepté** — Timeline clarifiée

## Date
22 avril 2026

## Contexte

La timeline du dashboard était ambiguë dans la planification du projet :

- **PLAN-REALISATION.md** dit : Dashboard MVP implémenté en **S12** (Phase 3)
- **BACKLOG.md** dit : Dashboard MVP part du scope MVP se terminant **S15**
- **BLOCKERS.md** listait initialement cela comme incohérence prioritaire

**Question** : Quand devrait-on démarrer le développement du dashboard ? S7-S9 ou S12 ou S13 ?

## Décision

Le dashboard doit être **construit en S12** (pas avant, pas après), avec validation en S13-S15.

## Justification

```
Phase 0 (S1-S3):   Discovery + Architecture ← Dashboard sketched but not built
Phase 1 (S4-S6):   Read implementation ← Dashboard NOT required yet
Phase 2 (S7-S11):  Plan + Approve implementation ← Dashboard design finalized
Phase 3 (S10-S12): Execute + Dashboard MVP ← Dashboard BUILD starts in S12
                                             ← Dashboard COMPLETE by S12 (end of Phase 3)

MVP Validation (S13-S15): Testing + measurement ← Dashboard already live, used for testing

V1 (S16-S20): Post-MVP improvements ← Dashboard enhanced with metrics, custom fields
```

### Arguments en faveur de S12

1. **Le dashboard n'est pas bloquant pour le MVP**
   - Le MVP peut terminer le cycle diagnostic/approbation sans interface visuelle
   - Les cartes Teams fournissent l'interface d'approbation

2. **Le dashboard améliore la validation du MVP**
   - Implémenter le dashboard en S12 permet à S13-S15 de tester avec une UI fonctionnelle
   - Meilleur contexte visible dans le dashboard accélère les diagnostics

3. **"MVP" se réfère au scope, pas à la timeline**
   - Scope MVP inclut le dashboard (feature must-have)
   - Deadline scope MVP = S15
   - Implémentation dashboard peut être S12 car non dépendance-bloquante

4. **Exécution parallèle possible**
   - Phase Execute (E0-E4) peut tourner sans dashboard
   - Dashboard construit en parallèle (S12) après stabilisation phase Approve (S10-S11)

## Conséquences

### Timeline du Dashboard (DÉCISION FINALE)

```
Phase 0 (S1-S3):   Discovery + Architecture ← Dashboard esquisé, pas construit
Phase 1 (S4-S6):   Implémentation Read ← Dashboard NON requis
Phase 2 (S7-S11):  Implémentation Plan + Approve ← Design finalisé
Phase 3 (S10-S12): Execute + Dashboard MVP ← BUILD démarre en S12
                                             ← COMPLET à fin S12

Validation MVP (S13-S15): Test + mesure ← Dashboard live, utilisé pour tests

V1 (S16-S20): Améliorations post-MVP ← Dashboard enrichi avec métriques, champs custom
```

### Pourquoi PAS plus tôt ? (Pourquoi pas S7-S9)

Le dashboard n'est pas requis tant que phase Approve n'est pas mature :

- S4-S9 : Focus sur logique Read, Plan, Approve
- Dashboard oisif sans données de diagnostic fonctionnelles
- Prioriser cycle RPAE core d'abord, UI second
- S7-S9 doit focus sur complexité Plan + Approve

### Pourquoi PAS plus tard ? (Pourquoi pas S13)

Le dashboard est nécessaire pour validation MVP :

- S13-S15 doit tester avec données incidents live
- Dashboard accélère review diagnostics vs outils ligne de commande
- Démontre "full cycle" aux stakeholders
- Meilleure UX pour mesure MTTR
