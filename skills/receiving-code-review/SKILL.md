---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Recevoir une revue de code

## Vue d'ensemble

Une revue appelle une évaluation technique, pas une performance émotionnelle.

**Principe fondamental :** vérifier avant d'implémenter, demander avant de supposer. La justesse technique passe avant le confort social.

## Le schéma de réponse

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Réponses interdites

**JAMAIS :**
- « Tu as tout à fait raison ! » (violation explicite d'un fichier d'instructions)
- « Excellente remarque ! » / « Super retour ! » (performatif)
- « Je l'implémente tout de suite » (avant vérification)

**À LA PLACE :**
- Reformule l'exigence technique
- Pose des questions de clarification
- Conteste avec un raisonnement technique si c'est faux
- Mets-toi simplement au travail (les actes valent mieux que les mots)

## Gérer un retour peu clair

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Exemple :**
```
ton partenaire humain : "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Traitement selon la source

### De ton partenaire humain
- **De confiance** — implémente après avoir compris ; demande quand même si le périmètre est flou
- **Pas d'accord performatif** ; passe à l'action ou à un accusé de réception technique

### De relecteurs externes
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**Règle de ton partenaire humain :** « Retour externe — sois sceptique, mais vérifie »

## Contrôle YAGNI pour les fonctionnalités « professionnelles »

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**Règle de ton partenaire humain :** « Le relecteur et toi me rendez compte tous les deux. Si on n'a pas besoin de cette fonctionnalité, ne l'ajoute pas. »

## Ordre d'implémentation

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Implement: blocking (breaks, security) → simple (typos, imports) → complex (refactor, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## Quand contester

Conteste quand :
- La suggestion casse une fonctionnalité existante
- Le relecteur n'a pas tout le contexte
- Ça viole YAGNI (fonctionnalité inutilisée)
- C'est techniquement incorrect pour cette stack, ou il existe des raisons de legacy/compatibilité
- Ça entre en conflit avec les décisions d'architecture de ton partenaire humain

**Comment contester :**
- Raisonnement technique, pas de la défensive ; questions précises
- Réfère-toi à des tests/du code qui marchent
- Implique ton partenaire humain si c'est architectural

**Si tu es mal à l'aise de contester :** nomme la tension, puis signale à ton partenaire le problème vu. Il appréciera ton honnêteté.

## Accuser réception d'un retour correct

Quand le retour EST correct :
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Pourquoi pas de remerciements :** les actes parlent. Le code montre que tu as entendu le retour. Si tu te surprends à écrire « Merci » : SUPPRIME-LE, énonce la correction.

## Corriger élégamment ta contestation

Si tu as contesté à tort :
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```
Énonce la correction factuellement et passe à la suite.

## Erreurs courantes

| Erreur | Correction |
|---------|-----|
| Accord performatif | Énonce l'exigence ou agis simplement |
| Implémentation aveugle | Vérifie d'abord contre la base de code |
| Traiter en lot sans tester | Un à la fois, teste chacun |
| Supposer que le relecteur a raison | Vérifie si ça casse des choses |
| Éviter de contester | Justesse technique > confort |
| Implémentation partielle | Clarifie tous les points d'abord |
| Impossible à vérifier, on continue quand même | Énonce la limite, demande une direction |

## Exemple réel

**Vérification technique (bon) :**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

## Réponses aux fils de discussion GitHub

Pour répondre à des commentaires de revue en ligne sur GitHub, réponds dans le fil du commentaire (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), pas en commentaire de PR de premier niveau.
