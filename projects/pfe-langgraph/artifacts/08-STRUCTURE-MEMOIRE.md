# Structure du Mémoire / PFE — Conforme UniLaSalle

## Informations
- **Titre** : Dans quelle mesure un agent IA avec Read-Plan-Approve-Execute peut-il réduire le MTTR des incidents DevOps ?
- **Établissement** : UniLaSalle-Amiens (Programme RIOC / Apprentissage)
- **Entreprise** : Isagri
- **Durée** : 6 mois

---

## Contraintes Formelles UniLaSalle

| Contrainte | Valeur |
|------------|--------|
| Volume | **60-80 pages hors annexes** |
| Police | **Arial 11 ou 12 pts** |
| Interligne | **Simple** |
| Marges gauche/droite | **2,5 cm** |
| Marges haut/bas (en-têtes/pieds inclus) | **3 cm** |
| Pagination | Commence à l'introduction (page 4). Page de garde, remerciements, table des matières = comptés mais **non numérotés** |
| Remise | **7 jours ouvrés avant la soutenance** au secrétariat apprentissage |
| Pénalité retard | **-1 point par jour de retard** |
| Plagiat | **Strictement interdit** — sanctionné sérieusement |
| Soutenance | **30 min** (démo incluse) + **10 min** Q/R + **10 min** délibération + **5 min** restitution |
| Dates soutenance 2025 | **25/08/2025 au 05/09/2025** à UniLaSalle-Amiens |

### Notation
| Partie | Poids | Évalué par |
|--------|-------|------------|
| Activité en entreprise | 50% | Tuteur entreprise (corrélé avec tuteur école) |
| Rapport | 25% | Tuteur école |
| Soutenance | 25% | Jury présidé par l'entreprise |

### Panneau de Synthèse
- PowerPoint ou équivalent, envoyé **1 semaine avant** la soutenance
- Charte : Arial, pas de fond de couleur, en-tête sur toute la largeur (logo entreprise + titre + logo UniLaSalle + nom/prénom + année + option)
- Présenté **en conclusion** de la soutenance

---

## Structure Conforme UniLaSalle (dans l'ordre)

1. **Page de garde** (modèle Moodle UniLaSalle)
2. **Remerciements**
3. **Table des matières**
4. **Table des figures** *(optionnelle)*
5. **Introduction** (page 4 — première page numérotée)
6. **Corps du rapport**
7. **Conclusion**
8. **Références bibliographiques**
9. **Annexes** *(optionnelles)*
10. **Résumé / Abstract** (4ème de couverture, modèle Moodle)

---

## Plan Détaillé du Mémoire (Conforme UniLaSalle)

### Introduction (5-8 pages) — Page 4
1. **Cadre et environnement** : Alternance chez Isagri, contexte DevOps
2. **Présentation du sujet** : Domaine, objectifs, pourquoi ce projet ?
3. **Contenu du rapport** : Annonce du plan

---

### Corps du Rapport

#### Partie 1 — Présentation de l'Entreprise et Contexte (10-15 pages)
- 1.1 Isagri : secteur, enjeux, organisation
- 1.2 L'équipe DevOps et les pratiques CI/CD en place
- 1.3 La problématique du MTTR chez Isagri
- 1.4 Cahier des charges : objectifs SMART et livrables

#### Partie 2 — Démarche et État de l'Art (15-20 pages)
- 2.1 Démarche adoptée pour atteindre les objectifs
- 2.2 DevOps et gestion des incidents : le MTTR comme métrique SRE
- 2.3 AIOps et diagnostic automatisé : état de l'art
- 2.4 Agents IA : architectures locales/persistants vs cloud/éphémères
- 2.5 Le pattern Read-Plan-Approve-Execute : fondements
- 2.6 Model Context Protocol (MCP) : standard d'interopérabilité
- 2.7 Synthèse et positionnement du projet

#### Partie 3 — Architecture et Conception (15-20 pages)
- 3.1 Analyse des besoins : personas, cas d'usage, requirements
- 3.2 Architecture cible (diagrammes C4)
- 3.3 Le cycle RPAE : Read, Plan, Approve, Execute
- 3.4 Sécurité et gouvernance : permissions, secrets, audit
- 3.5 Moyens mis à disposition : OpenClaw, MCP, VM, accès ADO

#### Partie 4 — Travail Réalisé et Expérimentation (15-20 pages)
- 4.1 Configuration d'OpenClaw et connexion MCP
- 4.2 Implémentation du module Read (heartbeat, webhooks, logs)
- 4.3 Implémentation du module Plan (diagnostic LLM, archive erreurs)
- 4.4 Implémentation du module Approve (Slack/Teams, boutons interactifs)
- 4.5 Implémentation du module Execute (dry-run → prod contrôlée)
- 4.6 Intégration Digital.ai Release via serveur MCP officiel
- 4.7 Protocole d'expérimentation et mesure du MTTR
- 4.8 Incidents rencontrés et résolutions

#### Partie 5 — Résultats et Analyse (10-15 pages)
- 5.1 Résultats quantitatifs : MTTR avant/après, justesse du diagnostic
- 5.2 Résultats qualitatifs : retours utilisateurs, confiance, adoption
- 5.3 Analyse et interprétation : validation/infirmation des hypothèses
- 5.4 Comparaison avec le cahier des charges

#### Partie 6 — Discussion, Limites et Perspectives (5-10 pages)
- 6.1 Discussion : implications pour la pratique DevOps et la recherche
- 6.2 Limites : méthodologiques, techniques, contextuelles
- 6.3 Perspectives : V1, V2, recherches futures
- 6.4 Leçons apprises (positionnement grille NAME)

---

### Conclusion (3-5 pages)
1. **Aspects techniques** : synthèse des conclusions intermédiaires
2. **Comparaison avec le cahier des charges** : résultats vs objectifs SMART
3. **Perspectives** : ouvertures et recherches futures

---

### Références Bibliographiques
Format UniLaSalle :
- Livre : `[n°] Nom(s), « Titre », Edition, Année`
- Article : `[n°] Nom(s), « Titre », Revue, Volume/N°/Année, pages`
- Rapport : `[n°] Nom, « Titre », Type (DEA/Thèse/Projet…), École/Université, Année`
- Les numéros doivent apparaître dans le texte. Les URLs sont acceptées.
- **15-20 références minimum**

---

### Annexes *(optionnelles — non comptées dans les 60-80 pages)*
- A : Code source (extraits significatifs)
- B : Configurations (OpenClaw, MCP, Slack/Teams)
- C : Captures d'écran du système
- D : Données brutes de l'expérimentation
- E : Survey de confiance (questionnaire complet)
- F : Diagrammes C4 complets
- G : Justification détaillée OpenClaw vs n8n vs LangGraph
- H : Cahier des charges validé

---

### Résumé / Abstract (4ème de couverture)
- Modèle Moodle UniLaSalle à utiliser

---

## Échéancier de Rédaction (Conforme UniLaSalle)

| Élément | Rédaction | Relecture Tuteur | Finalisation |
|---------|-----------|------------------|--------------|
| Cahier des charges | S2 | S3 | S4 |
| Partie 1 | S6-S8 | S9 | S10 |
| Partie 2 | S8-S12 | S13 | S14 |
| Partie 3 | S12-S16 | S17 | S18 |
| Partie 4 | S16-S20 | S21 | S22 |
| Partie 5 | S20-S22 | S23 | S24 |
| Partie 6 | S22-S23 | S24 | S25 |
| Introduction + Conclusion | S23-S24 | S25 | S26 |
| Bibliographie + Annexes | S24-S25 | S26 | S26 |
| **Remise au secrétariat** | — | — | **J-7 ouvrés avant soutenance** |
| Panneau de synthèse | S24-S25 | S26 | S26 |

### Dates Clés
| Jalon | Date Cible |
|-------|------------|
| Soutenance | 25/08/2025 – 05/09/2025 |
| Remise mémoire (7 jours ouvrés avant) | ~15/08/2025 (à confirmer) |
| Panneau de synthèse (1 semaine avant) | ~18/08/2025 (à confirmer) |
| Cahier des charges validé | Semaine 4 |
| Revue de projet intermédiaire | Semaine 13 (minimum requis par UniLaSalle) |
