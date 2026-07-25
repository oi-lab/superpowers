---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Écrire des skills

## Vue d'ensemble

**Écrire un skill, C'EST du développement piloté par les tests (TDD) appliqué à de la documentation de processus.**

**Les skills personnels vivent dans le répertoire skills de ton runtime** (`~/.claude/skills/` sur Claude Code). Antigravity reconnaît aussi `~/.agents/skills/` comme alias inter-runtime.

Tu écris des cas de test (scénarios de pression avec des sous-agents), tu les regardes échouer (comportement de référence), tu écris le skill (documentation), tu regardes les tests passer (les agents se conforment), et tu refactores (fermer les échappatoires).

**Principe fondamental :** si tu n'as pas regardé un agent échouer sans le skill, tu ne sais pas si le skill enseigne la bonne chose.

**PRÉREQUIS OBLIGATOIRE :** tu DOIS comprendre superpowers:test-driven-development avant d'utiliser ce skill. Ce skill-là définit le cycle fondamental RED-GREEN-REFACTOR. Le présent skill adapte le TDD à la documentation.

**Guide officiel :** pour les bonnes pratiques officielles d'Anthropic sur l'écriture de skills, voir anthropic-best-practices.md. Ce document fournit des patterns et lignes directrices complémentaires à l'approche centrée TDD de ce skill.

## Qu'est-ce qu'un skill ?

Un **skill** est un guide de référence pour des techniques, patterns ou outils éprouvés. Les skills aident les futurs agents à trouver et appliquer des approches efficaces.

**Les skills SONT :** des techniques réutilisables, des patterns, des outils, des guides de référence

**Les skills NE SONT PAS :** des récits de comment tu as résolu un problème une fois

## Correspondance TDD pour les skills

| Concept TDD | Création de skill |
|-------------|----------------|
| **Cas de test** | Scénario de pression avec sous-agent |
| **Code de production** | Document skill (SKILL.md) |
| **Test échoue (RED)** | L'agent viole la règle sans le skill (référence) |
| **Test passe (GREEN)** | L'agent se conforme avec le skill présent |
| **Refactor** | Fermer les échappatoires en maintenant la conformité |
| **Écrire le test d'abord** | Lancer le scénario de référence AVANT d'écrire le skill |
| **Regarder échouer** | Documenter les rationalisations exactes de l'agent |
| **Code minimal** | Écrire le skill traitant ces violations précises |
| **Regarder passer** | Vérifier que l'agent se conforme désormais |
| **Cycle refactor** | Trouver de nouvelles rationalisations → boucher → re-vérifier |

Tout le processus de création de skill suit RED-GREEN-REFACTOR.

## Quand créer un skill

**Créer quand :**
- La technique ne t'était pas intuitivement évidente
- Tu la référencerais à nouveau sur d'autres projets
- Le pattern s'applique largement (pas spécifique à un projet)
- D'autres en bénéficieraient

**Ne pas créer pour :**
- Des solutions ponctuelles
- Des pratiques standard bien documentées ailleurs
- Des conventions spécifiques au projet (mets-les dans ton fichier d'instructions)
- Des contraintes mécaniques (si c'est vérifiable par regex/validation, automatise — réserve la documentation aux jugements)

## Types de skills

### Technique
Méthode concrète avec des étapes à suivre (condition-based-waiting, root-cause-tracing)

### Pattern
Façon de penser les problèmes (flatten-with-flags, test-invariants)

### Référence
Docs d'API, guides de syntaxe, documentation d'outil (office docs)

## Structure de répertoire

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Espace de noms plat** - tous les skills dans un seul espace de noms consultable

**Fichiers séparés pour :**
1. **Référence lourde** (100+ lignes) - docs d'API, syntaxe exhaustive
2. **Outils réutilisables** - scripts, utilitaires, gabarits

**Garde en ligne :**
- Principes et concepts
- Patterns de code (< 50 lignes)
- Tout le reste

## Structure de SKILL.md

**Frontmatter (YAML) :**
- Deux champs requis : `name` et `description` (voir [agentskills.io/specification](https://agentskills.io/specification) pour tous les champs supportés)
- Max 1024 caractères au total
- `name` : lettres, chiffres et tirets uniquement (pas de parenthèses ni caractères spéciaux)
- `description` : à la troisième personne, décrit UNIQUEMENT quand l'utiliser (PAS ce que ça fait)
  - Commence par « Use when... » pour cibler les conditions de déclenchement
  - Inclut symptômes, situations et contextes précis
  - **NE JAMAIS résumer le processus ou le workflow du skill** (voir section SDO pour le pourquoi)
  - Garde sous 500 caractères si possible

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision non-obvious]

Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)
Before/after code comparison

## Quick Reference
Table or bullets for scanning common operations

## Implementation
Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes
What goes wrong + fixes

## Real-World Impact (optional)
Concrete results
```

## Optimisation de la découverte des skills (SDO)

**Critique pour la découverte :** les futurs agents doivent TROUVER ton skill

### 1. Champ description riche

**But :** ton agent lit la description pour décider quels skills charger pour une tâche donnée. Fais qu'elle réponde à : « Dois-je lire ce skill maintenant ? »

**Format :** commence par « Use when... » pour cibler les conditions de déclenchement

**CRITIQUE : Description = quand l'utiliser, PAS ce que fait le skill**

La description doit UNIQUEMENT décrire les conditions de déclenchement. NE résume PAS le processus ou le workflow du skill dans la description.

**Pourquoi c'est important :** les tests ont révélé que lorsqu'une description résume le workflow du skill, un agent peut suivre la description au lieu de lire le contenu complet du skill. Une description disant « revue de code entre les tâches » a poussé un agent à ne faire QU'UNE revue, alors que le flowchart du skill en montrait clairement DEUX (conformité au spec puis qualité du code).

Quand la description est devenue simplement « Use when executing implementation plans with independent tasks » (aucun résumé de workflow), l'agent a correctement lu le flowchart et suivi le processus de revue en deux étapes.

**Le piège :** les descriptions qui résument le workflow créent un raccourci que les agents emprunteront. Le corps du skill devient de la documentation que les agents sautent.

```yaml
# ❌ BAD: Summarizes workflow - agents may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ❌ BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks in the current session

# ✅ GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

**Contenu :**
- Utilise des déclencheurs, symptômes et situations concrets qui signalent que ce skill s'applique
- Décris le *problème* (race conditions, comportement incohérent), pas les *symptômes propres à un langage* (setTimeout, sleep)
- Garde les déclencheurs agnostiques de la techno sauf si le skill est lui-même spécifique à une techno
- Si le skill est spécifique à une techno, rends-le explicite dans le déclencheur
- Écris à la troisième personne (injecté dans le system prompt)
- **NE JAMAIS résumer le processus ou le workflow du skill**

```yaml
# ❌ BAD: Too abstract, vague, doesn't include when to use
description: For async testing

# ❌ BAD: First person
description: I can help you with async tests when they're flaky

# ❌ BAD: Mentions technology but skill isn't specific to it
description: Use when tests use setTimeout/sleep and are flaky

# ✅ GOOD: Starts with "Use when", describes problem, no workflow
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently

# ✅ GOOD: Technology-specific skill with explicit trigger
description: Use when using React Router and handling authentication redirects
```

### 2. Couverture des mots-clés

Utilise les mots qu'un agent chercherait :
- Messages d'erreur : "Hook timed out", "ENOTEMPTY", "race condition"
- Symptômes : "flaky", "hanging", "zombie", "pollution"
- Synonymes : "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Outils : commandes réelles, noms de librairies, types de fichiers

### 3. Nommage descriptif

**Utilise la voix active, verbe en premier :**
- ✅ `creating-skills` pas `skill-creation`
- ✅ `condition-based-waiting` pas `async-test-helpers`

### 4. Efficacité en tokens (critique)

**Problème :** getting-started et les skills fréquemment référencés se chargent dans CHAQUE conversation. Chaque token compte.

**Nombres de mots cibles :**
- workflows getting-started : <150 mots chacun
- skills fréquemment chargés : <200 mots au total
- autres skills : <500 mots (reste concis)

**Techniques :**

**Déplace les détails vers l'aide de l'outil :**
```bash
# ❌ BAD: Document all flags in SKILL.md
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: Reference --help
search-conversations supports multiple modes and filters. Run --help for details.
```

**Utilise les références croisées :**
```markdown
# ❌ BAD: Repeat workflow details
When searching, dispatch subagent with template...
[20 lines of repeated instructions]

# ✅ GOOD: Reference other skill
Always use subagents (50-100x context savings). REQUIRED: Use [other-skill-name] for workflow.
```

**Compresse les exemples :**
```markdown
# ❌ BAD: Verbose example (42 words)
your human partner: "How did we handle authentication errors in React Router before?"
You: I'll search past conversations for React Router authentication patterns.
[Dispatch subagent with search query: "React Router authentication error handling 401"]

# ✅ GOOD: Minimal example (20 words)
Partner: "How did we handle auth errors in React Router?"
You: Searching...
[Dispatch subagent → synthesis]
```

**Élimine la redondance :**
- Ne répète pas ce qui est dans les skills référencés
- N'explique pas ce qui est évident d'après la commande
- N'inclus pas plusieurs exemples du même pattern

**Vérification :**
```bash
wc -w skills/path/SKILL.md
# getting-started workflows: aim for <150 each
# Other frequently-loaded: aim for <200 total
```

**Nomme par ce que tu FAIS ou l'intuition centrale :**
- ✅ `condition-based-waiting` > `async-test-helpers`
- ✅ `using-skills` pas `skill-usage`
- ✅ `flatten-with-flags` > `data-structure-refactoring`
- ✅ `root-cause-tracing` > `debugging-techniques`

**Les gérondifs (-ing) marchent bien pour les processus :**
- `creating-skills`, `testing-skills`, `debugging-with-logs`
- Actif, décrit l'action que tu entreprends

### 5. Références croisées vers d'autres skills

**Quand tu écris de la documentation qui référence d'autres skills :**

Utilise le nom du skill seul, avec des marqueurs d'exigence explicites :
- ✅ Bon : `**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`
- ✅ Bon : `**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging`
- ❌ Mauvais : `See skills/testing/test-driven-development` (pas clair si requis)
- ❌ Mauvais : `@skills/testing/test-driven-development/SKILL.md` (force le chargement, brûle du contexte)

**Pourquoi pas de liens @ :** la syntaxe `@` force le chargement des fichiers immédiatement, consommant 200k+ de contexte avant que tu en aies besoin.

## Usage des flowcharts

La décision : as-tu besoin de montrer une information ? Si oui, est-ce une décision où tu pourrais te tromper ? Si oui → petit flowchart en ligne ; sinon → markdown ordinaire.

**Utilise les flowcharts UNIQUEMENT pour :**
- Points de décision non évidents
- Boucles de processus où tu pourrais t'arrêter trop tôt
- Décisions « quand utiliser A vs B »

**N'utilise jamais les flowcharts pour :**
- Matériel de référence → tables, listes
- Exemples de code → blocs markdown
- Instructions linéaires → listes numérotées
- Labels sans signification sémantique (step1, helper2)

Voir `graphviz-conventions.dot` dans ce répertoire pour les règles de style graphviz.

**Visualiser pour ton partenaire humain :** utilise `render-graphs.js` dans ce répertoire pour rendre les flowcharts d'un skill en SVG :
```bash
./render-graphs.js ../some-skill           # Each diagram separately
./render-graphs.js ../some-skill --combine # All diagrams in one SVG
```

## Exemples de code

**Un excellent exemple vaut mieux que plusieurs médiocres**

Choisis le langage le plus pertinent :
- Techniques de test → TypeScript/JavaScript
- Débogage système → Shell/Python
- Traitement de données → Python

**Bon exemple :**
- Complet et exécutable
- Bien commenté, expliquant le POURQUOI
- Issu d'un scénario réel
- Montre clairement le pattern
- Prêt à adapter (pas un gabarit générique)

**À éviter :**
- Implémenter dans 5+ langages
- Créer des gabarits à trous
- Écrire des exemples artificiels

Tu es bon pour porter du code - un seul excellent exemple suffit.

## Organisation des fichiers

### Skill auto-suffisant
```
defense-in-depth/
  SKILL.md    # Everything inline
```
Quand : tout le contenu tient, aucune référence lourde nécessaire

### Skill avec outil réutilisable
```
condition-based-waiting/
  SKILL.md    # Overview + patterns
  example.ts  # Working helpers to adapt
```
Quand : l'outil est du code réutilisable, pas juste un récit

### Skill avec référence lourde
```
pptx/
  SKILL.md       # Overview + workflows
  pptxgenjs.md   # 600 lines API reference
  ooxml.md       # 500 lines XML structure
  scripts/       # Executable tools
```
Quand : le matériel de référence est trop volumineux pour l'inline

## La Loi de Fer (identique au TDD)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Ceci s'applique aux NOUVEAUX skills ET aux MODIFICATIONS de skills existants.

Écrire le skill avant de tester ? Supprime-le. Recommence.
Modifier un skill sans tester ? Même violation.

**Aucune exception :**
- Pas pour les « simples ajouts »
- Pas pour « juste ajouter une section »
- Pas pour les « mises à jour de documentation »
- Ne garde pas les changements non testés comme « référence »
- N'« adapte » pas pendant que tu lances les tests
- Supprimer veut dire supprimer

**PRÉREQUIS OBLIGATOIRE :** le skill superpowers:test-driven-development explique pourquoi ceci compte. Les mêmes principes s'appliquent à la documentation.

## Tester tous les types de skills

Des types de skills différents exigent des approches de test différentes :

### Skills de discipline (règles/exigences)

**Exemples :** TDD, verification-before-completion, designing-before-coding

**Tester avec :**
- Questions académiques : comprennent-ils les règles ?
- Scénarios de pression : se conforment-ils sous stress ?
- Pressions multiples combinées : temps + coût irrécupérable + épuisement
- Identifier les rationalisations et ajouter des contres explicites

**Critère de réussite :** l'agent suit la règle sous pression maximale

### Skills de technique (guides pratiques)

**Exemples :** condition-based-waiting, root-cause-tracing, defensive-programming

**Tester avec :**
- Scénarios d'application : appliquent-ils la technique correctement ?
- Scénarios de variation : gèrent-ils les cas limites ?
- Tests d'information manquante : les instructions ont-elles des lacunes ?

**Critère de réussite :** l'agent applique avec succès la technique à un scénario nouveau

### Skills de pattern (modèles mentaux)

**Exemples :** reducing-complexity, concepts d'information-hiding

**Tester avec :**
- Scénarios de reconnaissance : reconnaissent-ils quand le pattern s'applique ?
- Scénarios d'application : savent-ils utiliser le modèle mental ?
- Contre-exemples : savent-ils quand NE PAS l'appliquer ?

**Critère de réussite :** l'agent identifie correctement quand/comment appliquer le pattern

### Skills de référence (documentation/API)

**Exemples :** documentation d'API, références de commandes, guides de librairies

**Tester avec :**
- Scénarios de récupération : trouvent-ils la bonne information ?
- Scénarios d'application : savent-ils utiliser correctement ce qu'ils ont trouvé ?
- Test de lacunes : les cas d'usage courants sont-ils couverts ?

**Critère de réussite :** l'agent trouve et applique correctement l'information de référence

## Rationalisations courantes pour sauter les tests

| Excuse | Réalité |
|--------|---------|
| « Le skill est manifestement clair » | Clair pour toi ≠ clair pour d'autres agents. Teste-le. |
| « Ce n'est qu'une référence » | Les références peuvent avoir des lacunes, des passages flous. Teste la récupération. |
| « Tester c'est exagéré » | Les skills non testés ont des problèmes. Toujours. 15 min de test épargnent des heures. |
| « Je testerai si des problèmes émergent » | Problèmes = les agents ne peuvent pas utiliser le skill. Teste AVANT de déployer. |
| « Trop fastidieux à tester » | Tester est moins fastidieux que déboguer un mauvais skill en production. |
| « Je suis sûr qu'il est bon » | L'excès de confiance garantit les problèmes. Teste quand même. |
| « La revue académique suffit » | Lire ≠ utiliser. Teste des scénarios d'application. |
| « Pas le temps de tester » | Déployer un skill non testé fait perdre plus de temps à le réparer plus tard. |

**Tout ceci signifie : teste avant de déployer. Aucune exception.**

## Accorde la forme à l'échec

Avant d'écrire une consigne, classe l'échec de référence. La forme qui blinde un type d'échec en aggrave un autre de façon mesurable.

| Échec de référence | Bonne forme | Mauvaise forme |
|---|---|---|
| Saute/viole une règle sous pression (sait mieux, le fait quand même) | Interdiction + table de rationalisation + signaux d'alerte (voir Blindage plus bas) | Consigne molle (« préfère... », « envisage... ») |
| Se conforme, mais la sortie a la mauvaise forme (prompt boursouflé, verdict noyé, spec ressassée) | Recette ou contrat positif : énonce ce que la sortie EST — ses parties, dans l'ordre | Liste d'interdictions (« ne ressasse pas », « ne narre jamais ») |
| Omet un élément requis de ce qu'il produit déjà | Structurel : champ ou emplacement REQUIS dans le gabarit qu'il remplit | Rappels en prose près du gabarit |
| Le comportement devrait dépendre d'une condition | Conditionnel indexé sur un prédicat observable (« si le brief existe, réfère-t'y ») | Règle inconditionnelle + clauses d'exemption |

**Pourquoi les interdictions se retournent contre les problèmes de forme :** sous une incitation concurrente (« rends le prompt auto-suffisant »), les agents négocient avec « ne fais pas X ». Dans des tests de formulation en tête-à-tête sur des consignes de prompt de dispatch, le bras interdiction a produit nettement plus du contenu indésirable que le bras recette (distributions entièrement séparées), et tendait pire que même le contrôle sans consigne — micro-teste ton propre cas plutôt que de supposer, mais ne saute jamais à l'interdiction par défaut. Une recette ne laisse rien à négocier : la sortie correspond à la forme énoncée ou non.

**Règles quelle que soit la forme choisie :**
- **Pas de clauses de nuance.** « Ne fais pas X sauf si ça compte » rouvre la négociation — ajouter une seule clause de nuance à une recette gagnante l'a dégradée de constante à bruitée dans les mêmes tests de formulation. Exprime une vraie exception comme son propre conditionnel sur un prédicat observable.
- **Les clauses d'exemption ne délimitent pas.** « Cette limite ne s'applique pas aux blocs de code » supprime quand même les blocs de code. Si une partie de la sortie doit être exemptée, restructure pour que la règle ne puisse pas l'atteindre.

## Blinder les skills contre la rationalisation

Les skills qui imposent une discipline (comme le TDD) doivent résister à la rationalisation. Les agents sont malins et trouveront des échappatoires sous pression.

**Périmètre :** cette boîte à outils est pour les échecs de discipline — un agent qui connaît la règle et la saute sous pression. Pour une sortie mal formée ou un élément omis, le blindage par interdiction se retourne contre toi ; utilise les formes de « Accorde la forme à l'échec » à la place.

**Note de psychologie :** comprendre POURQUOI les techniques de persuasion marchent aide à les appliquer systématiquement. Voir persuasion-principles.md pour le fondement de recherche (Cialdini, 2021 ; Meincke et al., 2025) sur les principes d'autorité, d'engagement, de rareté, de preuve sociale et d'unité.

### Ferme chaque échappatoire explicitement

Ne te contente pas d'énoncer la règle - interdis les contournements précis :

<Bad>
```markdown
Write code before test? Delete it.
```
</Bad>

<Good>
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```
</Good>

### Traite les arguments « esprit vs lettre »

Ajoute un principe fondateur tôt :

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

Ceci coupe court à toute une classe de rationalisations « je suis l'esprit ».

### Construis la table de rationalisation

Capture les rationalisations des tests de référence (voir section Test plus bas). Chaque excuse que font les agents va dans la table :

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

### Crée une liste de signaux d'alerte

Rends facile pour les agents de s'auto-contrôler quand ils rationalisent :

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

### Mets à jour la SDO pour les symptômes de violation

Ajoute à la description : les symptômes de quand tu es SUR LE POINT de violer la règle :

```yaml
description: use when implementing any feature or bugfix, before writing implementation code
```

## RED-GREEN-REFACTOR pour les skills

Suis le cycle TDD :

### RED : écris le test qui échoue (référence)

Lance un scénario de pression avec un sous-agent SANS le skill. Documente le comportement exact :
- Quels choix ont-ils faits ?
- Quelles rationalisations ont-ils utilisées (mot pour mot) ?
- Quelles pressions ont déclenché les violations ?

C'est « regarder le test échouer » - tu dois voir ce que les agents font naturellement avant d'écrire le skill.

### GREEN : écris le skill minimal

Écris un skill qui traite ces rationalisations précises. N'ajoute pas de contenu supplémentaire pour des cas hypothétiques.

Relance les mêmes scénarios AVEC le skill. L'agent devrait désormais se conformer.

### REFACTOR : ferme les échappatoires

L'agent a trouvé une nouvelle rationalisation ? Ajoute un contre explicite. Re-teste jusqu'à ce que ce soit à toute épreuve.

### Micro-teste la formulation avant les scénarios complets

Les runs de scénarios de pression complets sont la barrière finale, mais ils sont lents et coûteux par itération. Vérifie d'abord la formulation elle-même avec des micro-tests :

1. **Un échantillon à contexte neuf par appel** — un appel API brut, ou un sous-agent one-shot si tu n'as pas d'accès API. System prompt = le contexte réaliste où vivra la consigne (le skill ou gabarit de prompt complet, pas la consigne isolée) ; message utilisateur = une tâche qui tente l'échec.
2. **Inclus toujours un contrôle sans consigne.** Si le contrôle ne présente pas l'échec, il n'y a rien à corriger — arrête, n'écris pas la consigne.
3. **5+ répétitions par variante.** Les échantillons uniques mentent.
4. **Lis manuellement chaque correspondance signalée.** Score par programme si tu veux, mais les échos de gabarit et les contre-exemples cités se font passer pour des occurrences ; les comptages automatiques seuls surestiment échec comme réussite.
5. **La variance est une métrique.** Quand une consigne prend, les répétitions convergent vers la même forme. Cinq interprétations différentes sur cinq répétitions signifient que la formulation n'est pas contraignante — resserre la forme avant d'ajouter des mots.

Les micro-tests vérifient la formulation ; ils ne remplacent pas les scénarios de pression pour les skills de discipline.

**Méthodologie de test :** voir [testing-skills-with-subagents.md](testing-skills-with-subagents.md) pour la méthodologie de test complète :
- Comment écrire des scénarios de pression
- Types de pression (temps, coût irrécupérable, autorité, épuisement)
- Boucher les trous systématiquement
- Techniques de méta-test

## Anti-patterns

### ❌ Exemple narratif
« Dans la session 2025-10-03, on a trouvé qu'un projectDir vide causait... »
**Pourquoi mauvais :** trop spécifique, pas réutilisable

### ❌ Dilution multi-langage
example-js.js, example-py.py, example-go.go
**Pourquoi mauvais :** qualité médiocre, charge de maintenance

### ❌ Code dans les flowcharts
Mettre du code en labels de flowchart (par ex. des étapes « import fs », « read file »).
**Pourquoi mauvais :** impossible à copier-coller, difficile à lire

### ❌ Labels génériques
helper1, helper2, step3, pattern4
**Pourquoi mauvais :** les labels devraient avoir une signification sémantique

## STOP : avant de passer au skill suivant

**Après avoir écrit N'IMPORTE QUEL skill, tu DOIS T'ARRÊTER et compléter le processus de déploiement.**

**NE PAS :**
- Créer plusieurs skills en lot sans tester chacun
- Passer au skill suivant avant que l'actuel soit vérifié
- Sauter les tests parce que « le lot est plus efficace »

**La checklist de déploiement ci-dessous est OBLIGATOIRE pour CHAQUE skill.**

Déployer des skills non testés = déployer du code non testé. C'est une violation des standards de qualité.

## Checklist de création de skill (adaptée du TDD)

**IMPORTANT : crée un todo pour CHAQUE élément de la checklist ci-dessous.**

**Phase RED - écrire le test qui échoue :**
- [ ] Créer des scénarios de pression (3+ pressions combinées pour les skills de discipline)
- [ ] Lancer les scénarios SANS le skill - documenter le comportement de référence mot pour mot
- [ ] Identifier les patterns dans les rationalisations/échecs

**Phase GREEN - écrire le skill minimal :**
- [ ] Le nom n'utilise que lettres, chiffres, tirets (pas de parenthèses/caractères spéciaux)
- [ ] Frontmatter YAML avec champs requis `name` et `description` (max 1024 chars ; voir [spec](https://agentskills.io/specification))
- [ ] La description commence par « Use when... » et inclut des déclencheurs/symptômes précis
- [ ] La description est écrite à la troisième personne
- [ ] Mots-clés partout pour la recherche (erreurs, symptômes, outils)
- [ ] Vue d'ensemble claire avec principe fondamental
- [ ] Traite les échecs de référence précis identifiés en RED
- [ ] La forme de la consigne accorde le type d'échec (voir Accorde la forme à l'échec)
- [ ] Pour les consignes de mise en forme du comportement : formulation micro-testée contre un contrôle sans consigne (5+ répétitions, chaque correspondance signalée lue manuellement) — N/A pour les skills de pure référence
- [ ] Code en ligne OU lien vers un fichier séparé
- [ ] Un excellent exemple (pas multi-langage)
- [ ] Lancer les scénarios AVEC le skill - vérifier que les agents se conforment désormais

**Phase REFACTOR - fermer les échappatoires :**
- [ ] Identifier les NOUVELLES rationalisations des tests
- [ ] Ajouter des contres explicites (si skill de discipline)
- [ ] Construire la table de rationalisation à partir de toutes les itérations de test
- [ ] Créer la liste de signaux d'alerte
- [ ] Re-tester jusqu'à ce que ce soit à toute épreuve

**Contrôles de qualité :**
- [ ] Petit flowchart seulement si la décision est non évidente
- [ ] Table de référence rapide
- [ ] Section des erreurs courantes
- [ ] Pas de storytelling narratif
- [ ] Fichiers annexes uniquement pour des outils ou de la référence lourde

**Déploiement :**
- [ ] Committer le skill dans git et pousser sur ton fork (si configuré)
- [ ] Envisager de contribuer en retour via une PR (si largement utile)

## Workflow de découverte

Comment les futurs agents trouvent ton skill :

1. **Rencontre un problème** (« les tests sont flaky »)
2. **Cherche dans les skills** (grep les descriptions, parcourt les catégories)
3. **Trouve le SKILL** (la description correspond)
4. **Parcourt la vue d'ensemble** (est-ce pertinent ?)
5. **Lit les patterns** (table de référence rapide)
6. **Charge l'exemple** (seulement au moment d'implémenter)

**Optimise pour ce flux** - place les termes consultables tôt et souvent.
