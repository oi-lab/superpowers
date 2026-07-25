# Gabarit de prompt pour la re-revue ciblée

Utilise ce gabarit pour dispatcher une re-revue après une salve de corrections. Le
re-reviewer vérifie que les constats ont été traités et contrôle le diff de correction pour
détecter de nouvelles casses. Ce n'est pas une revue à neuf — la revue complète a déjà eu lieu.

**But :** vérifier que chaque constat de la revue précédente a été traité, et
que la correction elle-même n'a rien cassé.

```
Subagent (general-purpose):
  description: "Re-review Task N fix round R"
  model: [MODEL — REQUIS : choisis selon la section Model Selection du SKILL.md ;
         un modèle omis hérite silencieusement du plus coûteux de la session]
  prompt: |
    Tu re-revois une salve de corrections d'une tâche. Une revue précédente a produit
    des constats ; un implémenteur a tenté de les corriger. Ton rôle est de rendre un
    verdict sur chaque constat et d'inspecter le diff de correction — rien d'autre.

    ## La tâche

    Lis le briefing de tâche : [BRIEF_FILE]

    ## Les constats à vérifier

    [FINDINGS]

    ## La correction

    Lis le rapport de l'implémenteur (les rapports de correction sont ajoutés à la fin) :
    [REPORT_FILE]

    **Fix base:** [FIX_BASE_SHA] (le head que la revue précédente a vu)
    **Head:** [HEAD_SHA]
    **Diff file:** [DIFF_FILE]

    Lis le fichier de diff une fois — il contient les commits de correction, un résumé
    statistique et le diff de correction avec son contexte. Ne relance pas de commandes git.
    Si le fichier de diff est absent, récupère le diff toi-même :
    `git diff --stat [FIX_BASE_SHA]..[HEAD_SHA]` et
    `git diff [FIX_BASE_SHA]..[HEAD_SHA]`.

    Ta revue est en lecture seule sur ce checkout. Ne modifie ni l'arbre de travail,
    ni l'index, ni HEAD, ni l'état de branche, d'aucune façon.

    ## Périmètre

    Ton périmètre, c'est la liste des constats et le diff de correction. Rends un verdict sur chaque constat.
    Inspecte le diff de correction pour les nouveaux problèmes que la correction elle-même a introduits. NE
    re-revois PAS du code que la correction n'a pas touché : si tu remarques un problème entièrement
    hors du diff de correction, signale-le sous Out-of-Scope Observations — il
    ne bloque pas cette tâche et n'étend pas la boucle. Une revue large de toute
    la branche a lieu une fois toutes les tâches terminées.

    ## Tests

    L'implémenteur a relancé les tests couvrant le code amendé et a ajouté
    les résultats au fichier de rapport. Traite le rapport comme des affirmations non vérifiées :
    confirme que le rapport de correction nomme les tests couvrants et montre leur sortie,
    et vérifie les affirmations contre le diff. Ne relance pas la suite pour
    confirmer son rapport. Ne lance un test que lorsque la lecture du code soulève un
    doute spécifique qu'aucun run existant ne répond — et alors un test ciblé,
    jamais une suite à l'échelle du paquet.

    ## Format de sortie

    Ton message final EST le rapport lui-même : commence directement par le verdict du
    premier constat. Chaque ligne est un verdict, un constat avec file:line,
    ou une vérification que tu as faite — pas de préambule, pas de narration de processus.

    ### Finding Verdicts

    Pour chaque constat de « Les constats à vérifier », dans l'ordre :
    - **[constat en une ligne]** — ADDRESSED | NOT ADDRESSED, avec preuve
      file:line. « Tenté » n'est pas traité : le défaut spécifique doit ne
      plus exister.

    ### New Breakage in the Fix Diff

    Tout ce que la correction elle-même a cassé ou introduit, avec sévérité
    (Critical/Important/Minor) et file:line. « None » si propre.

    ### Out-of-Scope Observations

    Problèmes que tu as remarqués entièrement hors du diff de correction. Non bloquants ; le
    contrôleur les consigne au ledger pour la revue finale. « None » si aucun.

    ### Verdict

    **Fix round:** [All findings addressed, no new Critical/Important
    breakage | Findings remain open] — liste ceux qui restent ouverts.
```

**Placeholders :**
- `[MODEL]` — REQUIS : modèle du reviewer selon la section Model Selection du SKILL.md ; les
  re-revues ciblées de petits diffs de correction prennent un palier bon marché à intermédiaire
- `[BRIEF_FILE]` — le fichier de briefing de tâche (le même depuis lequel l'implémenteur a travaillé)
- `[FINDINGS]` — les constats Critical/Important et les écarts de spec de la
  revue précédente, copiés verbatim, un par puce
- `[REPORT_FILE]` — le fichier de rapport de l'implémenteur (rapports de correction ajoutés)
- `[FIX_BASE_SHA]` — le head que la revue précédente a vu
- `[HEAD_SHA]` — commit actuel
- `[DIFF_FILE]` — le chemin que `scripts/review-package PLAN_FILE FIX_BASE HEAD` a affiché

**Le re-reviewer renvoie :** les verdicts par constat (ADDRESSED / NOT ADDRESSED),
les nouvelles casses dans le diff de correction, les observations hors périmètre, et un verdict de salve.
