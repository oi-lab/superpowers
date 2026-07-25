---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Écrire des skills

## Vue d'ensemble

**Écrire un skill, C'EST du TDD appliqué à de la documentation de processus.** Tu écris des cas de test (scénarios de pression avec sous-agents), tu les regardes échouer (référence), tu écris le skill, tu regardes les tests passer (les agents se conforment), tu refactores (fermer les échappatoires).

**Les skills personnels vivent dans le répertoire skills de ton runtime** (`~/.claude/skills/` sur Claude Code ; Antigravity reconnaît aussi `~/.agents/skills/`).

**Principe fondamental :** si tu n'as pas regardé un agent échouer sans le skill, tu ne sais pas si le skill enseigne la bonne chose.

**PRÉREQUIS OBLIGATOIRE :** tu DOIS comprendre superpowers:test-driven-development, qui définit le cycle RED-GREEN-REFACTOR, avant d'utiliser ce skill.

**Guide officiel :** pour les bonnes pratiques officielles d'Anthropic, voir anthropic-best-practices.md (complémentaire à l'approche TDD de ce skill).

Un **skill** est un guide de référence pour des techniques, patterns ou outils réutilisables et éprouvés — **PAS** un récit de comment tu as résolu un problème une fois.

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

**Créer quand :** la technique n'était pas intuitivement évidente ; tu la référencerais sur d'autres projets ; le pattern s'applique largement ; d'autres en bénéficieraient.

**Ne pas créer pour :** solutions ponctuelles ; pratiques standard documentées ailleurs ; conventions spécifiques au projet (→ fichier d'instructions) ; contraintes mécaniques (si vérifiable par regex/validation, automatise — réserve la documentation aux jugements).

## Types de skills

- **Technique** — méthode concrète avec étapes (condition-based-waiting, root-cause-tracing)
- **Pattern** — façon de penser les problèmes (flatten-with-flags, test-invariants)
- **Référence** — docs d'API, guides de syntaxe, documentation d'outil (office docs)

## Structure de répertoire

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Espace de noms plat.** **Fichiers séparés pour :** référence lourde (100+ lignes) ; outils réutilisables (scripts, gabarits). **Garde en ligne :** principes, concepts, patterns de code (< 50 lignes), tout le reste.

## Structure de SKILL.md

**Frontmatter (YAML) :**
- Deux champs requis : `name` et `description` (voir [agentskills.io/specification](https://agentskills.io/specification) pour tous les champs) ; max 1024 caractères au total
- `name` : lettres, chiffres et tirets uniquement (pas de parenthèses ni caractères spéciaux)
- `description` : à la troisième personne, décrit UNIQUEMENT quand l'utiliser (PAS ce que ça fait) ; commence par « Use when... » ; inclut symptômes/situations précis ; **NE JAMAIS résumer le workflow** (voir SDO) ; sous 500 caractères si possible

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview        # What is this? Core principle in 1-2 sentences.
## When to Use     # Flowchart inline SI décision non-évidente ; bullets SYMPTÔMES + use cases ; quand NE PAS
## Core Pattern    # (techniques/patterns) comparaison code before/after
## Quick Reference # Table ou bullets scannables
## Implementation  # Code inline pour patterns simples ; lien vers fichier pour référence lourde/outils
## Common Mistakes # Ce qui foire + fixes
## Real-World Impact (optional)  # Résultats concrets
```

## Optimisation de la découverte des skills (SDO)

**Critique pour la découverte :** les futurs agents doivent TROUVER ton skill

### 1. Champ description riche

**But :** ton agent lit la description pour décider quels skills charger. Fais qu'elle réponde à : « Dois-je lire ce skill maintenant ? »

**CRITIQUE : Description = quand l'utiliser, PAS ce que fait le skill.** La description décrit UNIQUEMENT les conditions de déclenchement. NE résume PAS le workflow.

**Pourquoi :** si la description résume le workflow, l'agent peut la suivre au lieu de lire le skill. Une description « revue de code entre les tâches » a poussé un agent à ne faire QU'UNE revue, alors que le flowchart en montrait DEUX. Ramenée à « Use when executing implementation plans with independent tasks » (sans résumé), l'agent a lu le flowchart et suivi les deux étapes. Le résumé de workflow crée un raccourci que les agents emprunteront à la place du corps du skill.

**Contenu :**
- Déclencheurs, symptômes et situations concrets ; commence par « Use when... »
- Décris le *problème* (race conditions), pas les *symptômes propres à un langage* (setTimeout, sleep)
- Déclencheurs agnostiques de la techno, sauf si le skill est lui-même spécifique à une techno (alors rends-le explicite)
- Troisième personne (injecté dans le system prompt)
- **NE JAMAIS résumer le processus ou le workflow**

```yaml
# ❌ Résume le workflow - l'agent le suit au lieu de lire le skill
description: Use when executing plans - dispatches subagent per task with code review between tasks
# ❌ Première personne / trop abstrait
description: I can help you with async tests when they're flaky
# ❌ Mentionne une techno alors que le skill n'y est pas spécifique
description: Use when tests use setTimeout/sleep and are flaky
# ✅ Conditions de déclenchement seules, décrit le problème
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently
# ✅ Skill spécifique à une techno, déclencheur explicite
description: Use when using React Router and handling authentication redirects
```

### 2. Couverture des mots-clés

Utilise les mots qu'un agent chercherait :
- Messages d'erreur : "Hook timed out", "ENOTEMPTY", "race condition"
- Symptômes : "flaky", "hanging", "zombie", "pollution"
- Synonymes : "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Outils : commandes réelles, noms de librairies, types de fichiers

### 3. Nommage descriptif

**Voix active, verbe/ce que tu FAIS en premier ; les gérondifs (-ing) marchent pour les processus :**
- ✅ `condition-based-waiting` > `async-test-helpers`
- ✅ `flatten-with-flags` > `data-structure-refactoring`
- ✅ `root-cause-tracing` > `debugging-techniques`
- ✅ `creating-skills`, `testing-skills` (actif, décrit l'action)

### 4. Efficacité en tokens (critique)

**Problème :** getting-started et les skills fréquemment référencés se chargent dans CHAQUE conversation. Chaque token compte.

**Nombres de mots cibles :**
- workflows getting-started : <150 mots chacun
- skills fréquemment chargés : <200 mots au total
- autres skills : <500 mots (reste concis)

**Techniques :**
- **Déplace les détails vers l'aide de l'outil :** au lieu de documenter tous les flags, « Run --help for details. »
- **Références croisées :** ne répète pas un workflow, réfère le skill (`**REQUIRED:** Use [other-skill]`).
- **Compresse les exemples :** garde-les minimaux (ex. « Partner: "How did we handle auth errors?" / You: Searching... / [Dispatch subagent → synthesis] »).
- **Élimine la redondance :** ne répète pas les skills référencés, l'évident, ni plusieurs exemples du même pattern.

**Vérification :**
```bash
wc -w skills/path/SKILL.md
# getting-started workflows: aim for <150 each
# Other frequently-loaded: aim for <200 total
```

### 5. Références croisées vers d'autres skills

Nom du skill seul, avec marqueurs d'exigence explicites :
- ✅ `**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development`
- ✅ `**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging`
- ❌ `See skills/testing/test-driven-development` (pas clair si requis)
- ❌ `@skills/testing/test-driven-development/SKILL.md`

**Pourquoi pas de liens @ :** la syntaxe `@` force le chargement immédiat, consommant 200k+ de contexte avant que tu en aies besoin.

## Usage des flowcharts

Décision : est-ce une décision où tu pourrais te tromper ? Si oui → petit flowchart en ligne ; sinon → markdown ordinaire.

**Flowcharts UNIQUEMENT pour :** points de décision non évidents ; boucles de processus où tu pourrais t'arrêter trop tôt ; décisions « A vs B ».

**JAMAIS pour :** matériel de référence (→ tables, listes) ; exemples de code (→ blocs markdown) ; instructions linéaires (→ listes numérotées) ; labels sans sémantique (step1, helper2).

Voir `graphviz-conventions.dot` dans ce répertoire pour le style graphviz.

**Visualiser pour ton partenaire humain :** `render-graphs.js` rend les flowcharts d'un skill en SVG :
```bash
./render-graphs.js ../some-skill           # Each diagram separately
./render-graphs.js ../some-skill --combine # All diagrams in one SVG
```

## Exemples de code

**Un excellent exemple vaut mieux que plusieurs médiocres.** Choisis le langage le plus pertinent (test → TS/JS, débogage → Shell/Python, données → Python).

**Bon exemple :** complet et exécutable, commenté sur le POURQUOI, issu d'un scénario réel, montre clairement le pattern, prêt à adapter.

**À éviter :** implémenter dans 5+ langages, gabarits à trous, exemples artificiels. Un seul excellent exemple suffit.

## Organisation des fichiers

- **Auto-suffisant** (`SKILL.md` seul) : tout tient inline, aucune référence lourde.
- **Avec outil réutilisable** (`SKILL.md` + `example.ts`) : l'outil est du code réutilisable, pas juste un récit.
- **Avec référence lourde** (`SKILL.md` + `pptxgenjs.md` 600 lignes + `ooxml.md` + `scripts/`) : matériel de référence trop volumineux pour l'inline.

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

Chaque type exige une approche de test différente :

| Type (exemples) | Tester avec | Critère de réussite |
|---|---|---|
| **Discipline** (TDD, verification-before-completion) | Questions académiques ; scénarios de pression ; pressions combinées (temps + coût irrécupérable + épuisement) ; identifier rationalisations + contres | Suit la règle sous pression maximale |
| **Technique** (condition-based-waiting, root-cause-tracing) | Application ; variation (cas limites) ; information manquante (lacunes ?) | Applique la technique à un scénario nouveau |
| **Pattern** (reducing-complexity, information-hiding) | Reconnaissance (quand ça s'applique) ; application ; contre-exemples (quand NE PAS) | Identifie quand/comment appliquer le pattern |
| **Référence** (API, commandes, librairies) | Récupération (trouve l'info ?) ; application ; lacunes (cas courants couverts ?) | Trouve et applique correctement l'info |

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

**Pourquoi les interdictions se retournent contre les problèmes de forme :** sous incitation concurrente (« rends le prompt auto-suffisant »), les agents négocient avec « ne fais pas X ». En tests de formulation, le bras interdiction a produit nettement plus de contenu indésirable que le bras recette (distributions séparées), tendant pire que le contrôle sans consigne. Micro-teste ton cas, mais ne saute jamais à l'interdiction par défaut. Une recette ne laisse rien à négocier.

**Règles quelle que soit la forme :**
- **Pas de clauses de nuance.** « Ne fais pas X sauf si ça compte » rouvre la négociation — une seule clause a dégradé une recette gagnante de constante à bruitée. Exprime une vraie exception comme son propre conditionnel sur un prédicat observable.
- **Les clauses d'exemption ne délimitent pas.** « Cette limite ne s'applique pas aux blocs de code » supprime quand même les blocs de code. Restructure pour que la règle ne puisse pas atteindre ce qui doit être exempté.

## Blinder les skills contre la rationalisation

Les skills de discipline (comme le TDD) doivent résister à la rationalisation ; les agents trouveront des échappatoires sous pression.

**Périmètre :** pour les échecs de discipline — un agent qui connaît la règle et la saute sous pression. Pour une sortie mal formée ou un élément omis, le blindage par interdiction se retourne contre toi ; utilise « Accorde la forme à l'échec ».

**Note de psychologie :** comprendre POURQUOI les techniques de persuasion marchent aide à les appliquer. Voir persuasion-principles.md pour le fondement de recherche (Cialdini, 2021 ; Meincke et al., 2025) sur autorité, engagement, rareté, preuve sociale, unité.

### Ferme chaque échappatoire explicitement

N'énonce pas juste la règle — interdis les contournements précis :

```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

### Traite les arguments « esprit vs lettre »

Ajoute un principe fondateur tôt — ceci coupe court aux rationalisations « je suis l'esprit » :

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Construis la table de rationalisation

Capture les rationalisations des tests de référence. Chaque excuse va dans la table :

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

### Crée une liste de signaux d'alerte

Pour que les agents s'auto-contrôlent quand ils rationalisent :

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

Ajoute à la description les symptômes de quand tu es SUR LE POINT de violer la règle :

```yaml
description: use when implementing any feature or bugfix, before writing implementation code
```

## RED-GREEN-REFACTOR pour les skills

- **RED : écris le test qui échoue (référence).** Lance un scénario de pression avec un sous-agent SANS le skill. Documente les choix, les rationalisations (mot pour mot), les pressions déclenchantes. Tu dois voir ce que les agents font naturellement avant d'écrire le skill.
- **GREEN : écris le skill minimal.** Traite ces rationalisations précises, rien pour des cas hypothétiques. Relance les mêmes scénarios AVEC le skill : l'agent devrait se conformer.
- **REFACTOR : ferme les échappatoires.** Nouvelle rationalisation ? Ajoute un contre explicite. Re-teste jusqu'à ce que ce soit à toute épreuve.

### Micro-teste la formulation avant les scénarios complets

Les scénarios de pression complets sont la barrière finale mais lents et coûteux. Vérifie d'abord la formulation avec des micro-tests :

1. **Un échantillon à contexte neuf par appel** — appel API brut, ou sous-agent one-shot sans accès API. System prompt = le contexte réaliste où vivra la consigne (skill ou gabarit complet, pas la consigne isolée) ; message utilisateur = une tâche qui tente l'échec.
2. **Inclus toujours un contrôle sans consigne.** Si le contrôle ne présente pas l'échec, il n'y a rien à corriger — arrête.
3. **5+ répétitions par variante.** Les échantillons uniques mentent.
4. **Lis manuellement chaque correspondance signalée.** Échos de gabarit et contre-exemples cités se font passer pour des occurrences ; les comptages automatiques seuls surestiment échec comme réussite.
5. **La variance est une métrique.** Quand une consigne prend, les répétitions convergent. Cinq interprétations sur cinq répétitions = formulation non contraignante — resserre la forme avant d'ajouter des mots.

Les micro-tests vérifient la formulation ; ils ne remplacent pas les scénarios de pression pour les skills de discipline.

**Méthodologie de test :** voir [testing-skills-with-subagents.md](testing-skills-with-subagents.md) pour la méthodologie complète (écrire des scénarios de pression ; types de pression : temps, coût irrécupérable, autorité, épuisement ; boucher les trous ; méta-test).

## Anti-patterns

- **❌ Exemple narratif** (« Dans la session 2025-10-03... ») : trop spécifique, pas réutilisable.
- **❌ Dilution multi-langage** (example-js.js, -py.py, -go.go) : qualité médiocre, charge de maintenance.
- **❌ Code dans les flowcharts** (labels « import fs », « read file ») : impossible à copier-coller.
- **❌ Labels génériques** (helper1, step3) : les labels devraient avoir une signification sémantique.

## STOP : avant de passer au skill suivant

**Après avoir écrit N'IMPORTE QUEL skill, tu DOIS T'ARRÊTER et compléter le déploiement.** NE PAS : créer plusieurs skills en lot sans tester chacun ; passer au suivant avant que l'actuel soit vérifié ; sauter les tests parce que « le lot est plus efficace ».

La checklist de déploiement ci-dessous est OBLIGATOIRE pour CHAQUE skill. Déployer un skill non testé = déployer du code non testé.

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

Comment les futurs agents trouvent ton skill : rencontre un problème (« tests flaky ») → cherche (grep les descriptions) → trouve le SKILL (description correspond) → parcourt la vue d'ensemble → lit les patterns (référence rapide) → charge l'exemple (au moment d'implémenter).

**Optimise pour ce flux** — place les termes consultables tôt et souvent.
