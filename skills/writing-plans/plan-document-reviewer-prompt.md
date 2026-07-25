# Gabarit de prompt pour le reviewer de document de plan

Utilise ce gabarit pour dispatcher un sous-agent reviewer de document de plan.

**But :** vérifier que le plan est complet, correspond à la spec, et a une découpe de tâches correcte.

**Dispatcher après :** le plan complet est écrit.

```
Subagent (general-purpose):
  description: "Review plan document"
  prompt: |
    Tu es un reviewer de document de plan. Vérifie que ce plan est complet et prêt pour l'implémentation.

    **Plan to review:** [PLAN_FILE_PATH]
    **Spec for reference:** [SPEC_FILE_PATH]

    ## Ce qu'il faut vérifier

    | Catégorie | Ce qu'il faut chercher |
    |----------|------------------|
    | Complétude | TODOs, placeholders, tâches incomplètes, étapes manquantes |
    | Alignement avec la spec | Le plan couvre les exigences de la spec, pas de dérive de périmètre majeure |
    | Découpe des tâches | Les tâches ont des frontières claires, les étapes sont actionnables |
    | Constructibilité | Un ingénieur pourrait-il suivre ce plan sans se retrouver bloqué ? |

    ## Calibrage

    **Ne signale que les problèmes qui causeraient de vrais soucis durant l'implémentation.**
    Un implémenteur qui construit la mauvaise chose ou qui se retrouve bloqué est un problème.
    Les formulations mineures, les préférences stylistiques, et les suggestions « nice to have » n'en sont pas.

    Approuve sauf s'il y a des lacunes sérieuses — exigences de la spec manquantes,
    étapes contradictoires, contenu placeholder, ou tâches si vagues qu'on ne peut pas agir dessus.

    ## Format de sortie

    ## Plan Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Task X, Step Y] : [problème précis] - [pourquoi c'est important pour l'implémentation]

    **Recommendations (advisory, do not block approval):**
    - [suggestions d'amélioration]
```

**Le reviewer renvoie :** Status, Issues (le cas échéant), Recommendations.
