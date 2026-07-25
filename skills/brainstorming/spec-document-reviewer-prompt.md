# Gabarit de prompt pour le reviewer de document de spec

Utilise ce gabarit pour dispatcher un sous-agent reviewer de document de spec.

**But :** vérifier que la spec est complète, cohérente et prête pour la planification de l'implémentation.

**Dispatcher après :** le document de spec est écrit dans docs/superpowers/specs/

```
Subagent (general-purpose):
  description: "Review spec document"
  prompt: |
    Tu es un reviewer de document de spec. Vérifie que cette spec est complète et prête pour la planification.

    **Spec to review:** [SPEC_FILE_PATH]

    ## Ce qu'il faut vérifier

    | Catégorie | Ce qu'il faut chercher |
    |----------|------------------|
    | Complétude | TODOs, placeholders, « TBD », sections incomplètes |
    | Cohérence | Contradictions internes, exigences conflictuelles |
    | Clarté | Exigences assez ambiguës pour amener quelqu'un à construire la mauvaise chose |
    | Périmètre | Assez focalisé pour un seul plan — ne couvre pas plusieurs sous-systèmes indépendants |
    | YAGNI | Fonctionnalités non demandées, sur-ingénierie |

    ## Calibrage

    **Ne signale que les problèmes qui causeraient de vrais soucis durant la planification.**
    Une section manquante, une contradiction, ou une exigence si ambiguë qu'elle pourrait être
    interprétée de deux façons différentes — ce sont des problèmes. Les améliorations mineures de formulation,
    les préférences stylistiques, et « des sections moins détaillées que d'autres » n'en sont pas.

    Approuve sauf s'il y a des lacunes sérieuses qui mèneraient à un plan défectueux.

    ## Format de sortie

    ## Spec Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Section X] : [problème précis] - [pourquoi c'est important pour la planification]

    **Recommendations (advisory, do not block approval):**
    - [suggestions d'amélioration]
```

**Le reviewer renvoie :** Status, Issues (le cas échéant), Recommendations.
