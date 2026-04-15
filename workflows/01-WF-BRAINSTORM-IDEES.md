# WF-BRAINSTORM-IDEES

## Objectif
Explorer une idée de projet et produire :
- 3 variantes d’idée
- un premier découpage fonctionnel
- une liste de risques et contraintes majeurs

## Agents impliqués
- MANAGER-DEBAT (virtuel, décrit dans rules)
- AGENT-PRODUIT
- AGENT-RECHERCHE
- AGENT-ARCHITECTE
- AGENT-CRITIQUE

## Étapes

1. [MANAGER-DEBAT]
   - Reformule la question de l’utilisateur.
   - Choisit les 2 ou 3 agents les plus pertinents en fonction du type de question.
   - Demande une première proposition à chacun.

2. [BOUCLE DEBAT ACTOR/CRITIC - 2 tours]
   - Chaque agent producteur (PRODUIT, ARCHITECTE, RECHERCHE) génère sa proposition.
   - AGENT-CRITIQUE lit chaque proposition et rédige une critique détaillée.
   - L’agent initial révise sa proposition en intégrant les critiques.

3. [SYNTHESE]
   - MANAGER-DEBAT agrège les meilleures parties de chaque proposition.
   - Produit un document final structuré (sections recommandées, TODO, questions ouvertes).

## Conditions d’arrêt
- Maximum 2 tours de débat.
- MANAGER-DEBAT doit toujours produire une synthèse finale même si les agents ne sont pas d’accord.
