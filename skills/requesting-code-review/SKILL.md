---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Demander une revue de code

Dépêche un sous-agent relecteur pour repérer les problèmes tôt. Il reçoit un contexte précisément préparé — jamais l'historique de ta session.

**Principe fondamental :** relis tôt, relis souvent.

## Quand demander une revue

**Obligatoire :**
- Après chaque tâche en développement piloté par sous-agents
- Après avoir terminé une fonctionnalité majeure
- Avant de merger sur main

**Optionnel mais utile :**
- Quand tu es bloqué (regard neuf)
- Avant un refactoring (état de référence)
- Après avoir corrigé un bug complexe

## Comment demander

**1. Récupère les SHA git :**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dépêche le sous-agent relecteur :**

Dépêche un sous-agent `general-purpose` en remplissant le gabarit dans [code-reviewer.md](code-reviewer.md)

**Champs à remplir :**
- `{DESCRIPTION}` - Résumé bref de ce que tu as construit
- `{PLAN_OR_REQUIREMENTS}` - Ce que ça doit faire
- `{BASE_SHA}` - Commit de départ
- `{HEAD_SHA}` - Commit de fin

**3. Agis sur le retour :**
- Corrige les problèmes Critical immédiatement
- Corrige les problèmes Important avant de continuer
- Note les problèmes Minor pour plus tard
- Conteste si le relecteur se trompe (avec un raisonnement)

## Exemple

```
[Task 2 terminée] → BASE_SHA/HEAD_SHA récupérés → dispatch relecteur
  DESCRIPTION: verifyIndex()/repairIndex() avec 4 types d'erreurs
  PLAN_OR_REQUIREMENTS: Task 2 du plan
Retour: Important: manque indicateurs de progression ; Minor: magic number (100)
→ [Corrige Important] → continue Task 3
```

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Je vais juste relire le diff moi-même au lieu de dépêcher un relecteur » | Tu es le coordinateur — relire le diff en ligne consomme la fenêtre de contexte dont tu as besoin pour piloter le travail. Dépêche un sous-agent relecteur : le diff et l'évaluation vivent dans son contexte, et seules les conclusions te reviennent. |
| « Le relecteur a besoin de tout l'historique de ma session pour comprendre le changement » | Donne-lui un contexte précisément préparé, jamais l'historique de ta session. Ça garde le relecteur concentré sur le produit du travail, pas sur ton cheminement de pensée. |

## Signaux d'alerte

**Ne jamais :**
- Sauter la revue parce que « c'est simple »
- Ignorer les problèmes Critical
- Continuer avec des problèmes Important non corrigés
- Discuter un retour technique valide

**Si le relecteur se trompe :**
- Conteste avec un raisonnement technique
- Montre le code/les tests qui prouvent que ça marche
- Demande des précisions

Voir le gabarit dans : [code-reviewer.md](code-reviewer.md)
