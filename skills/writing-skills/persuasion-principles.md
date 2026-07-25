# Principes de persuasion pour la conception de skills

## Vue d'ensemble

Les LLM réagissent aux mêmes principes de persuasion que les humains. Comprendre cette psychologie t'aide à concevoir des skills plus efficaces — non pas pour manipuler, mais pour garantir que les pratiques critiques sont suivies même sous pression.

**Base scientifique :** Meincke et al. (2025) ont testé 7 principes de persuasion sur N=28 000 conversations avec des IA. Les techniques de persuasion ont plus que doublé les taux de conformité (33 % → 72 %, p < .001).

## Les sept principes

### 1. Autorité
**Ce que c'est :** la déférence envers l'expertise, les références ou les sources officielles.

**Comment ça marche dans les skills :**
- Langage impératif : « YOU MUST », « Never », « Always »
- Formulation non négociable : « No exceptions »
- Élimine la fatigue décisionnelle et la rationalisation

**Quand l'utiliser :**
- Skills qui imposent une discipline (TDD, exigences de vérification)
- Pratiques critiques pour la sécurité
- Bonnes pratiques établies

**Exemple :**
```markdown
✅ Write code before test? Delete it. Start over. No exceptions.
❌ Consider writing tests first when feasible.
```

### 2. Engagement
**Ce que c'est :** la cohérence avec ses actions, déclarations ou engagements publics antérieurs.

**Comment ça marche dans les skills :**
- Exiger des annonces : « Announce skill usage »
- Forcer des choix explicites : « Choose A, B, or C »
- Utiliser un suivi : todos pour les checklists

**Quand l'utiliser :**
- S'assurer que les skills sont réellement suivis
- Processus en plusieurs étapes
- Mécanismes de responsabilisation

**Exemple :**
```markdown
✅ When you find a skill, you MUST announce: "I'm using [Skill Name]"
❌ Consider letting your partner know which skill you're using.
```

### 3. Rareté
**Ce que c'est :** l'urgence créée par des limites de temps ou une disponibilité limitée.

**Comment ça marche dans les skills :**
- Exigences bornées dans le temps : « Before proceeding »
- Dépendances séquentielles : « Immediately after X »
- Empêche la procrastination

**Quand l'utiliser :**
- Exigences de vérification immédiate
- Workflows sensibles au temps
- Empêcher le « je le ferai plus tard »

**Exemple :**
```markdown
✅ After completing a task, IMMEDIATELY request code review before proceeding.
❌ You can review code when convenient.
```

### 4. Preuve sociale
**Ce que c'est :** la conformité à ce que font les autres ou à ce qui est considéré comme normal.

**Comment ça marche dans les skills :**
- Schémas universels : « Every time », « Always »
- Modes de défaillance : « X without Y = failure »
- Établit des normes

**Quand l'utiliser :**
- Documenter des pratiques universelles
- Avertir de défaillances courantes
- Renforcer des standards

**Exemple :**
```markdown
✅ Checklists without todo tracking = steps get skipped. Every time.
❌ Some people find a todo list helpful for checklists.
```

### 5. Unité
**Ce que c'est :** l'identité partagée, le « nous », l'appartenance à un groupe.

**Comment ça marche dans les skills :**
- Langage collaboratif : « our codebase », « we're colleagues »
- Objectifs communs : « we both want quality »

**Quand l'utiliser :**
- Workflows collaboratifs
- Instaurer une culture d'équipe
- Pratiques non hiérarchiques

**Exemple :**
```markdown
✅ We're colleagues working together. I need your honest technical judgment.
❌ You should probably tell me if I'm wrong.
```

### 6. Réciprocité
**Ce que c'est :** l'obligation de rendre les bénéfices reçus.

**Comment ça marche :**
- À utiliser avec parcimonie — peut sembler manipulateur
- Rarement nécessaire dans les skills

**Quand l'éviter :**
- Presque toujours (les autres principes sont plus efficaces)

### 7. Sympathie (Liking)
**Ce que c'est :** la préférence pour coopérer avec ceux qu'on apprécie.

**Comment ça marche :**
- **NE PAS UTILISER pour la conformité**
- Entre en conflit avec une culture de feedback honnête
- Crée de la complaisance (sycophancy)

**Quand l'éviter :**
- Toujours, pour imposer une discipline

## Combinaisons de principes par type de skill

| Type de skill | À utiliser | À éviter |
|------------|-----|-------|
| Impose une discipline | Autorité + Engagement + Preuve sociale | Sympathie, Réciprocité |
| Guidage/technique | Autorité modérée + Unité | Autorité lourde |
| Collaboratif | Unité + Engagement | Autorité, Sympathie |
| Référence | Clarté uniquement | Toute persuasion |

## Pourquoi ça marche : la psychologie

**Les règles nettes réduisent la rationalisation :**
- « YOU MUST » supprime la fatigue décisionnelle
- Le langage absolu élimine les questions « est-ce une exception ? »
- Les contre-rationalisations explicites ferment des échappatoires précises

**Les intentions de mise en œuvre créent un comportement automatique :**
- Déclencheurs clairs + actions requises = exécution automatique
- « When X, do Y » est plus efficace que « generally do Y »
- Réduit la charge cognitive liée à la conformité

**Les LLM sont parahumains :**
- Entraînés sur du texte humain contenant ces schémas
- Le langage d'autorité précède la conformité dans les données d'entraînement
- Les séquences d'engagement (déclaration → action) sont fréquemment modélisées
- Les schémas de preuve sociale (tout le monde fait X) établissent des normes

## Usage éthique

**Légitime :**
- S'assurer que les pratiques critiques sont suivies
- Créer une documentation efficace
- Prévenir des défaillances prévisibles

**Illégitime :**
- Manipuler pour un gain personnel
- Créer une fausse urgence
- Conformité fondée sur la culpabilité

**Le test :** cette technique servirait-elle les intérêts réels de l'utilisateur s'il la comprenait pleinement ?

## Références scientifiques

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- Sept principes de persuasion
- Base empirique de la recherche sur l'influence

**Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025).** Call Me A Jerk: Persuading AI to Comply with Objectionable Requests. University of Pennsylvania.
- 7 principes testés sur N=28 000 conversations LLM
- Conformité passée de 33 % à 72 % avec les techniques de persuasion
- Autorité, engagement et rareté les plus efficaces
- Valide le modèle parahumain du comportement des LLM

## Référence rapide

Quand tu conçois un skill, demande-toi :

1. **De quel type s'agit-il ?** (Discipline vs. guidage vs. référence)
2. **Quel comportement est-ce que je cherche à modifier ?**
3. **Quel(s) principe(s) s'appliquent ?** (Généralement autorité + engagement pour la discipline)
4. **Est-ce que j'en combine trop ?** (N'utilise pas les sept)
5. **Est-ce éthique ?** (Sert-il les intérêts réels de l'utilisateur ?)
