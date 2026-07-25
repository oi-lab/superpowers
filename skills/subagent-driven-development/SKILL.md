---
name: subagent-driven-development
description: À utiliser UNIQUEMENT pour de gros plans d'implémentation comportant de nombreuses tâches indépendantes, et seulement quand ton partenaire humain demande explicitement une exécution par sous-agents - déploie un sous-agent neuf par tâche, ce qui est gourmand en tokens (opt-in). Pour les plans ordinaires, exécute-les toi-même.
---

# Développement piloté par sous-agents

Exécute un plan en déployant un sous-agent implémenteur neuf par tâche, une revue de tâche (conformité au spec + qualité du code) après chacune, et une revue large de toute la branche à la fin.

**Pourquoi des sous-agents :** tu délègues les tâches à des agents spécialisés au contexte isolé. En façonnant précisément leurs instructions et leur contexte, tu garantis qu'ils restent concentrés et réussissent. Ils ne doivent jamais hériter du contexte ou de l'historique de ta session — tu construis exactement ce dont ils ont besoin. Cela préserve aussi ton propre contexte pour le travail de coordination.

**Principe central :** sous-agent neuf par tâche + revue de tâche (spec + qualité) + revue finale large = haute qualité, itération rapide

**Narration :** entre les appels d'outils, narre au plus une courte ligne — le registre (ledger) et les résultats d'outils portent la trace.

**Exécution continue :** ne t'arrête pas pour faire un point avec ton partenaire humain entre les tâches. Exécute toutes les tâches du plan sans t'arrêter. Les seules raisons de s'arrêter sont : un statut BLOCKED que tu ne peux pas résoudre, une ambiguïté qui empêche réellement d'avancer, ou toutes les tâches terminées. Les « Dois-je continuer ? » et les résumés de progression font perdre du temps — on t'a demandé d'exécuter le plan, alors exécute-le.

## Quand l'utiliser

Décision : tu as un plan d'implémentation, dont les tâches sont majoritairement indépendantes, et tu restes dans cette session → subagent-driven-development. Si tu passes en session parallèle → executing-plans. Pas de plan, ou tâches fortement couplées → exécution manuelle ou brainstorm d'abord.

**vs. Executing Plans (session parallèle) :**
- Même session (pas de changement de contexte)
- Sous-agent neuf par tâche (pas de pollution de contexte)
- Revue après chaque tâche (conformité spec + qualité du code), revue large à la fin
- Itération plus rapide (pas d'humain dans la boucle entre les tâches)

## Le processus

Vue d'ensemble du flux (détaillée dans les sections suivantes) :

1. **Setup** : worktree, vérification du ledger, lecture du plan, revue préalable.
2. **Par tâche :** dispatch de l'implémenteur (`./implementer-prompt.md`) → réponds à ses questions si besoin → il implémente, teste, commit, s'auto-relit → génère le paquet de revue et dispatch du relecteur de tâche (`./task-reviewer-prompt.md`) → si spec ✅ et qualité approuvée : consigne la complétion au ledger, marque le todo. Sinon : si un finding contredit le texte du plan, demande à ton partenaire humain qui prévaut ; puis entre dans la boucle de correction (5 rounds max — R≤3 reprends l'implémenteur, R≥4 implémenteur neuf sur modèle plus capable), chaque round suivi d'une re-revue scopée (`./re-review-prompt.md`). Au round 5 non résolu, le disjoncteur saute : arbitre chaque finding ouvert ; si un finding porteur subsiste, STOP et rapporte BLOCKED ; sinon parque les findings au ledger avec leurs décisions.
3. **À la fin :** dispatch du relecteur final (`../requesting-code-review/code-reviewer.md`) sur le modèle le plus capable. Findings finaux → UN dispatch de correction, une re-revue scopée, arbitrage des résidus. Revue finale propre → supprime le workspace de ce plan → utilise superpowers:finishing-a-development-branch.

## Setup

Assure-toi que le travail se déroule dans un workspace isolé : utilise superpowers:using-git-worktrees pour en créer un ou vérifier l'existant. Ne démarre jamais l'implémentation sur une branche main/master sans le consentement explicite de ton partenaire humain.

La mémoire conversationnelle ne survit pas à la compaction. Dans de vraies sessions, des contrôleurs ayant perdu le fil ont re-dispatché des séquences entières de tâches déjà terminées — l'échec le plus coûteux observé. Suis la progression dans un fichier ledger, pas seulement dans les todos.

- Chaque plan possède un workspace : au démarrage du skill, lance le `scripts/sdd-workspace PLAN_FILE` de ce skill — il imprime le répertoire git-ignoré du plan (`<repo-root>/.superpowers/sdd/<plan-basename>/`), foyer de chaque artefact de CE plan : ledger, briefs, rapports, paquets de revue. Le répertoire d'un autre plan n'est jamais à toi pour le lire ou l'écrire.
- Vérifie le ledger de ce plan à `<workspace>/progress.md`. Si sa première ligne nomme ton fichier de plan, les tâches ayant une ligne `Task <N>: complete` sont FAITES — ne les re-dispatch pas ; reprends à la première tâche sans cette ligne. Une tâche dont la dernière ligne est un round de correction est en cours de boucle : reprends la boucle au round suivant. Un ledger dont la première ligne nomme un autre fichier de plan — ou un ledger égaré à l'ancien chemin plat `.superpowers/sdd/progress.md` — est la progression d'un autre plan : laisse-le en place et démarre le tien, neuf.
- Crée le ledger avec son identité en première ligne : `# SDD ledger — plan: <plan file path>`.
- Le ledger est ta carte de récupération : les commits qu'il nomme existent dans git même quand ton contexte ne se souvient plus de les avoir créés. Après une compaction, fie-toi au ledger et à `git log` plutôt qu'à ta propre mémoire.
- `git clean -fdx` détruira le workspace (c'est du scratch git-ignoré) ; si cela arrive, récupère depuis `git log`.

Lis le plan une fois, note son contexte et ses Global Constraints, et crée un todo par tâche.

Avant de dispatcher la Tâche 1, scanne le plan une fois pour repérer les conflits :

- des tâches qui se contredisent entre elles ou contredisent les Global Constraints du plan
- tout ce que le plan mandate explicitement mais que le barème de revue traite comme un défaut (un test qui n'affirme rien, une duplication verbatim d'un bloc de logique)

Présente tout ce que tu trouves à ton partenaire humain en une seule question groupée — chaque finding à côté du texte du plan qui le mandate, en demandant lequel prévaut — avant le début de l'exécution, pas une interruption par découverte en cours de plan. Si le scan est propre, avance sans commentaire. La boucle de revue reste le filet pour les conflits qui n'émergent que de l'implémentation.

## Sélection du modèle

Utilise le modèle le moins puissant capable de tenir chaque rôle, pour économiser le coût et gagner en vitesse.

**Tâches d'implémentation mécaniques** (fonctions isolées, specs clairs, 1-2 fichiers) : modèle rapide et bon marché. La plupart des tâches d'implémentation sont mécaniques quand le plan est bien spécifié.

**Tâches d'intégration et de jugement** (coordination multi-fichiers, reconnaissance de patterns, débogage) : modèle standard.

**Tâches d'architecture et de conception** : le modèle le plus capable disponible. La revue finale de toute la branche en fait partie — dispatch-la sur le modèle le plus capable disponible, pas le modèle par défaut de la session.

**Tâches de revue** : choisis le modèle au jugement équivalent, calibré sur la taille, la complexité et le risque du diff. Un petit diff mécanique n'a pas besoin du modèle le plus capable ; un changement de concurrence subtil, si. Les re-revues scopées de petits diffs de correction prennent un tier bon marché à moyen.

**Escalade de la boucle de correction (rounds 4-5)** : utilise un modèle d'au moins un tier au-dessus de l'implémenteur bloqué.

**Spécifie toujours explicitement le modèle en dispatchant un sous-agent.** Un modèle omis hérite du modèle de ta session — souvent le plus capable et le plus cher — ce qui défait silencieusement cette section.

**Le nombre de tours prime sur le prix des tokens.** Le coût en temps réel et en contexte croît avec le nombre de tours d'un sous-agent, et les modèles les moins chers prennent régulièrement 2-3× plus de tours sur du travail multi-étapes — coûtant plus au total. Utilise un modèle de tier moyen comme plancher pour les relecteurs et pour les implémenteurs travaillant à partir de descriptions en prose. Quand le texte du plan contient le code complet à écrire, l'implémentation est de la transcription plus des tests : utilise le tier le moins cher pour cet implémenteur. Les corrections mécaniques mono-fichier prennent aussi le tier le moins cher.

**Signaux de complexité de tâche (tâches d'implémentation) :**
- Touche 1-2 fichiers avec un spec complet → modèle bon marché
- Touche plusieurs fichiers avec des enjeux d'intégration → modèle standard
- Requiert du jugement de conception ou une compréhension large du codebase → modèle le plus capable

## La boucle de tâche

Tout ce que tu colles dans un prompt de dispatch — et tout ce qu'un sous-agent te renvoie — reste résident dans ton contexte pour le reste de la session et est relu à chaque tour ultérieur. Transmets les artefacts sous forme de fichiers.

### 1. Dispatcher l'implémenteur

Enregistre BASE (`git rev-parse HEAD`) avant de dispatcher — le paquet de revue et les diffs des rounds de correction en ont besoin.

- **Brief de tâche :** avant de dispatcher un implémenteur, lance le `scripts/task-brief PLAN_FILE N` de ce skill — il extrait le texte complet de la tâche dans un fichier nommé de façon unique et imprime le chemin. Compose le dispatch pour que le brief reste la source unique des exigences. Ton dispatch doit contenir : (1) une ligne sur la place de cette tâche dans le projet ; (2) le chemin du brief, introduit par « lis ceci d'abord — ce sont tes exigences, avec les valeurs exactes à utiliser verbatim » ; (3) les interfaces et décisions des tâches précédentes que le brief ne peut pas connaître ; (4) ta résolution de toute ambiguïté repérée dans le brief ; (5) le chemin du fichier de rapport et le contrat de rapport. Les valeurs exactes (nombres, chaînes magiques, signatures, cas de test) n'apparaissent que dans le brief. Ne fais jamais lire tout le fichier de plan à un sous-agent.
- **Fichier de rapport :** nomme le fichier de rapport de l'implémenteur d'après le brief (brief `…/task-N-brief.md` → rapport `…/task-N-report.md`) et mets-le dans le prompt de dispatch. L'implémenteur écrit le rapport complet là-bas et ne renvoie que le statut, les commits, un résumé de test en une ligne, et les préoccupations.
- Un prompt de dispatch décrit une tâche, pas l'historique de la session. Ne colle pas les résumés cumulés des tâches précédentes (« état après les Tâches 1-3 ») dans les dispatches ultérieurs — dans une vraie session, un dispatch a atteint 42k caractères dont 99 % d'historique collé. Un sous-agent neuf a besoin de sa tâche, des interfaces qu'il touche, et des contraintes globales. Rien d'autre.
- Si une tâche précédente a parqué un finding dans la zone que cette tâche touche, porte un pointeur vers cette entrée du ledger dans le dispatch.
- Enregistre l'identité de l'agent implémenteur depuis le résultat du dispatch — les rounds de correction 1-3 reprennent cet agent.
- Ne dispatch jamais plusieurs sous-agents d'implémentation en parallèle (conflits).

Template : [implementer-prompt.md](implementer-prompt.md)

### 2. Traiter le rapport

Les sous-agents implémenteurs rapportent l'un de quatre statuts. Traite chacun comme il faut :

**DONE :** génère le paquet de revue (`scripts/review-package PLAN_FILE BASE HEAD`, depuis le répertoire de ce skill — il imprime le chemin de fichier unique qu'il a écrit ; BASE est le commit enregistré avant de dispatcher l'implémenteur — jamais `HEAD~1`, qui laisse silencieusement tomber tous les commits d'une tâche multi-commits sauf le dernier), puis dispatch le relecteur de tâche avec le chemin imprimé.

**DONE_WITH_CONCERNS :** l'implémenteur a terminé le travail mais a signalé des doutes. Lis les préoccupations avant de continuer. Si elles portent sur la correction ou le périmètre, traite-les avant la revue. Si ce sont des observations (ex. « ce fichier devient volumineux »), note-les et passe à la revue.

**NEEDS_CONTEXT :** l'implémenteur a besoin d'informations non fournies. Fournis le contexte manquant et re-dispatch.

**BLOCKED :** l'implémenteur ne peut pas terminer la tâche. Évalue le blocage :
1. Si c'est un problème de contexte, fournis plus de contexte et re-dispatch avec le même modèle
2. Si la tâche demande plus de raisonnement, re-dispatch avec un modèle plus capable
3. Si la tâche est trop grande, découpe-la en morceaux plus petits
4. Si le plan lui-même est faux, escalade vers l'humain

**Ne jamais** ignorer une escalade ni forcer le même modèle à réessayer sans changement. Si l'implémenteur dit qu'il est bloqué, quelque chose doit changer.

Si l'implémenteur pose des questions — avant de commencer ou en cours de tâche — réponds clairement et complètement, fournis du contexte supplémentaire si besoin, et ne le précipite pas dans l'implémentation.

### 3. Revoir la tâche

Les revues par tâche sont des portes (gates) au périmètre de la tâche. La revue large a lieu une fois, à la revue finale de toute la branche. Ne saute jamais la revue de tâche, et n'accepte jamais un rapport auquel il manque l'un des verdicts — la conformité au spec ET la qualité de la tâche sont toutes deux requises. L'auto-relecture de l'implémenteur ne remplace jamais la revue de tâche ; les deux sont nécessaires.

- Remets au relecteur son diff sous forme de fichier : lance le `scripts/review-package PLAN_FILE BASE HEAD` de ce skill et passe au relecteur le chemin de fichier qu'il imprime (ou, sans bash : `git log --oneline`, `git diff --stat`, et `git diff -U10` pour la plage, redirigés vers un seul fichier nommé de façon unique). La sortie n'entre jamais dans ton propre contexte, et le relecteur voit la liste des commits, le résumé statistique et le diff complet avec contexte en un seul Read. Utilise le BASE enregistré avant de dispatcher l'implémenteur — jamais `HEAD~1`, qui tronque silencieusement les tâches multi-commits. Ne dispatch jamais un relecteur de tâche sans fichier de diff.
- **Entrées du relecteur :** le relecteur de tâche reçoit trois chemins — le même fichier de brief, le fichier de rapport, et le paquet de revue — plus les contraintes globales qui lient la tâche.
- Le bloc de contraintes globales que tu remets au relecteur est sa lentille d'attention. Copie les exigences contraignantes verbatim depuis la section Global Constraints du plan ou depuis le spec : valeurs exactes, formats exacts, et les relations énoncées entre composants (« même layout que X », « correspond à Y »). Le template du relecteur porte déjà les règles de processus (YAGNI, hygiène de test, méthode de revue) — le bloc de contraintes est pour ce que le spec de CE projet exige.
- N'ajoute pas de directives ouvertes comme « vérifie tous les usages » ou « lance les tests de course si utile » sans une raison concrète et spécifique à la tâche.
- Ne demande pas à un relecteur de relancer des tests que l'implémenteur a déjà lancés sur le même code — le rapport de l'implémenteur porte la preuve des tests.
- Ne pré-juge pas les findings à la place du relecteur — n'instruis jamais un relecteur d'ignorer ou de ne pas signaler un problème précis. Si tu crois qu'un finding serait un faux positif, laisse le relecteur le soulever et arbitre-le dans la boucle de revue. Si le prompt que tu écris contient « ne signale pas », « ne traite pas X comme un défaut », « au plus Mineur », ou « le plan a choisi » — stop : tu pré-juges, généralement pour t'épargner une boucle de revue.

Le relecteur de tâche peut rapporter des items « ⚠️ Impossible à vérifier depuis le diff » — des exigences vivant dans du code non modifié ou s'étendant sur plusieurs tâches. Ils ne bloquent pas le reste de la revue, mais tu dois résoudre chacun toi-même avant de marquer la tâche complète : c'est toi qui détiens le plan et le contexte inter-tâches qui manquent au relecteur. Si tu confirmes qu'un item est un vrai manque, traite-le comme une revue de spec échouée — il entre dans la boucle de correction avec les autres findings.

Template : [task-reviewer-prompt.md](task-reviewer-prompt.md)

### 4. La boucle de correction

La boucle se déclenche quand la revue rapporte spec ❌, tout finding Critical ou Important, ou un item ⚠️ que tu as confirmé comme vrai manque.

Avant le début de la boucle, deux issues la quittent immédiatement :

- Consigne les findings Minor dans le ledger de progression au fur et à mesure (`Task <N>: minor (deferred): <une-ligne>`), et pointe la revue finale de toute la branche vers cette liste pour qu'elle trie lesquels doivent être corrigés avant le merge. Un récapitulatif que personne ne lit est un rejet silencieux. Les findings Minor n'entrent jamais dans la boucle.
- Un finding étiqueté plan-mandated — ou tout finding qui contredit ce que le texte du plan exige — est la décision de l'humain, comme toute contradiction de plan : présente le finding et le texte du plan, demande lequel prévaut. Ne rejette pas le finding parce que le plan le mandate, et ne dispatch pas une correction qui contredit le plan sans demander.

Tout le reste entre dans la boucle. Un round de correction est un dispatch de correction plus une re-revue scopée. Cinq rounds maximum par tâche :

**Rounds 1-3 — reprends l'implémenteur d'origine.** Envoie-lui les findings ouverts verbatim. Son contexte est intact : il connaît la tâche, le code, et ses propres choix. Si ton harness ne peut pas envoyer un autre message à un sous-agent vivant, dispatch un implémenteur neuf portant le chemin du brief, le chemin du fichier de rapport, et les findings — le fichier de rapport est la mémoire persistante dans les deux cas.

**Rounds 4-5 — dispatch un implémenteur neuf sur un modèle plus capable** (selon Sélection du modèle), avec le chemin du brief, le chemin du fichier de rapport, les findings ouverts, et ce cadrage : « Un implémenteur précédent a tenté cette tâche [N] fois ; elle est à toi maintenant. Lis le fichier de rapport pour ce qui a été tenté. » Une boucle qui survit à trois reprises signifie généralement que l'implémenteur ne voit pas son propre problème — regard neuf et montée en capacité en un seul mouvement.

**Chaque round, dans les deux cas :** l'implémenteur corrige, relance les tests couvrant le code amendé, ajoute son rapport de correction au même fichier de rapport, et renvoie le contrat court. Avant de re-dispatcher le relecteur, confirme que le rapport de correction contient les tests couvrants, la commande lancée, et la sortie ; dispatch la re-revue une fois les trois présents. Nomme les fichiers de test couvrants dans le message de correction — une correction d'une ligne n'a pas besoin de toute la suite.

**La re-revue est scopée.** Lance `scripts/review-package PLAN_FILE FIX_BASE HEAD` où FIX_BASE est le head que la revue précédente a vu, et dispatch [re-review-prompt.md](re-review-prompt.md) avec la liste des findings, le brief, le fichier de rapport, et le chemin du diff imprimé. Le re-relecteur verdicte chaque finding ADDRESSED ou NOT ADDRESSED et signale toute nouvelle casse dans le seul diff de correction. Une nouvelle casse Critical/Important dans le diff de correction rejoint la liste des findings ouverts. Les observations hors périmètre vont au ledger comme mineurs différés — elles n'étendent jamais la boucle.

**Après chaque round,** ajoute au ledger :
`Task <N>: fix round <R>/5 (<X> addressed, <Y> open — <finding one-liners>; commits <a7>..<b7>)`

Ne corrige jamais les findings toi-même dans la session contrôleur — ton contexte reste propre pour la coordination, et les corrections du contrôleur sautent la revue.

**Le disjoncteur.** Quand la re-revue du round 5 laisse encore des findings ouverts, arrête de dispatcher. Arbitre chaque finding ouvert toi-même — c'est toi qui détiens le plan et le contexte inter-tâches qui manquent au relecteur :

- **Le relecteur a tort, ou le point est contestable :** parque-le — `Task <N>: parked — <finding> — ruling: <pourquoi le code tient>`. La revue finale voit les deux versions.
- **Réel, mais rien en aval ne s'appuie dessus :** parque-le de la même façon, avec une décision disant qu'il est réel et différé.
- **Réel et porteur** — une tâche ultérieure s'appuie dessus, ou il révèle un défaut du plan : STOP. Ajoute `Task <N>: BLOCKED — <raison>` et rapporte à ton partenaire humain avec le finding, le texte du plan qu'il percute, et l'historique des corrections. Parquer un échec structurel laisse chaque tâche dépendante s'appuyer dessus et remet à la revue finale un problème qu'elle ne peut pas corriger non plus.

Arbitre uniquement au plafond. Arbitrer plus tôt pour terminer une boucle, c'est pré-juger sous un autre nom. Chaque arbitrage est une entrée de ledger — un rejet silencieux est interdit.

### 5. Terminer la tâche

Quand la revue revient propre — ou que chaque finding ouvert est parqué avec une décision au plafond — ajoute la ligne de complétion au ledger dans le même message que tes autres écritures :

- `Task <N>: complete (commits <base7>..<head7>, review clean)`
- `Task <N>: complete (commits <base7>..<head7>, <K> parked)` après un disjoncteur sauté

Puis marque le todo complet et passe à la suite. Ne passe jamais à la tâche suivante tant que la revue a des problèmes Critical/Important ouverts qui ne sont ni corrigés ni parqués-avec-décision au plafond.

## Revue finale

La revue finale de toute la branche reçoit aussi un paquet : lance `scripts/review-package PLAN_FILE MERGE_BASE HEAD` (MERGE_BASE = le commit d'où la branche est partie, ex. `git merge-base main HEAD`) et inclus le chemin imprimé dans le dispatch de revue finale, pour que le relecteur final lise un seul fichier au lieu de re-dériver le diff de branche avec des commandes git. Dispatch sur le modèle le plus capable disponible (voir Sélection du modèle), en utilisant [code-reviewer.md](../requesting-code-review/code-reviewer.md) de superpowers:requesting-code-review. Pointe-le vers les lignes deferred-minor et parked du ledger pour qu'il trie lesquelles doivent être corrigées avant le merge.

Si la revue finale de toute la branche renvoie des findings, dispatch UN seul sous-agent de correction avec la liste complète des findings — pas un correcteur par finding. Les correcteurs par finding reconstruisent chacun le contexte et relancent les suites ; dans une vraie session, la vague de correction de revue finale a coûté plus que toutes ses tâches réunies. Puis lance exactement une re-revue scopée de la vague de correction (`scripts/review-package PLAN_FILE FIX_BASE HEAD` sur la plage de correction, [re-review-prompt.md](re-review-prompt.md)). Arbitre tout finding résiduel comme dans le disjoncteur de la boucle de tâche : parque avec décisions, ou arrête sur les findings porteurs. Il n'y a pas de seconde vague de correction — les findings porteurs résiduels remontent à ton partenaire humain quand finishing-a-development-branch présente les options.

## Finir

Quand la revue finale de toute la branche est propre et ses corrections mergées, supprime le workspace de ce plan (`rm -rf <workspace>`) — l'historique git est le registre désormais. Les répertoires voisins appartiennent à d'autres plans ; ne les touche pas.

Utilise superpowers:finishing-a-development-branch.

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Assez proche sur la conformité au spec » | Le relecteur a trouvé des manques au spec = pas terminé. Corrige ou atteins le plafond et arbitre — ce sont les seules issues. |
| « Je vais le corriger moi-même, dispatcher c'est de la surcharge » | Les corrections du contrôleur polluent ton contexte et sautent la revue. Reprends l'implémenteur. |
| « Un round de plus va converger » | Passé le plafond, les rounds ne convergent pas — l'échec est structurel. Arbitre et route. |
| « Le relecteur va juste trouver autre chose de toute façon » | Les re-revues scopées vérifient les corrections ; elles ne peuvent pas divaguer. Les nouveaux findings sur du code intouché vont au ledger, pas à la boucle. |
| « Ce finding est manifestement faux, je le laisse tomber » | Tu n'arbitres qu'au plafond, et chaque décision est une entrée de ledger. Les rejets silencieux sont interdits. |
| « La correction était petite, saute la re-revue » | Les corrections non relues sont la façon dont les régressions atterrissent. Chaque round finit par une re-revue scopée. |
| « Les revues ralentissent la boucle » | La boucle sans revues n'est que du brassage non vérifié. Les revues sont les freins et la direction de la boucle. |
| « La tenue du ledger est de la surcharge » | Le ledger est ce qui survit à la compaction. Des contrôleurs sans ledger ont re-dispatché des séquences entières de tâches déjà terminées. |

## Exemple de déroulement

```
You: I'm using Subagent-Driven Development to execute this plan.

[Setup: worktree verified]
[Read plan file once: docs/superpowers/plans/feature-plan.md]
[Resolve workspace: scripts/sdd-workspace docs/superpowers/plans/feature-plan.md — no ledger inside, fresh start]
[Create todos for all tasks]

Task 1: Hook installation script

[Run task-brief for Task 1; dispatch implementer with brief + report paths + context]

Implementer: "Before I begin - should the hook be installed at user or system level?"

You: "User level (~/.config/superpowers/hooks/)"

Implementer: [Later]
  - Implemented install-hook command
  - Added tests, 5/5 passing
  - Self-review: Found I missed --force flag, added it
  - Committed

[Run review-package PLAN_FILE BASE HEAD; dispatch task reviewer with the printed path]
Task reviewer: Spec ✅ - all requirements met, nothing extra.
  Strengths: Good test coverage, clean. Issues: None. Task quality: Approved.

[Ledger: Task 1: complete (commits a1b2c3d..d4e5f6a, review clean)]

Task 2: Recovery modes

[Run task-brief for Task 2; dispatch implementer with brief + report paths + context]

Implementer: [No questions]
  - Added verify/repair modes
  - 8/8 tests passing
  - Committed

[Run review-package PLAN_FILE BASE HEAD; dispatch task reviewer with the printed path]
Task reviewer: Spec ❌:
  - Missing: Progress reporting (spec says "report every 100 items")
  Issues (Important): Magic number (100)

[Fix round 1: resume the implementer with both findings]
Implementer: Added progress reporting, extracted PROGRESS_INTERVAL constant.
  Re-ran test/recovery.test.js — 10/10 passing. Fix report appended.

[Run review-package PLAN_FILE FIX_BASE HEAD; dispatch scoped re-review]
Re-reviewer: Missing progress reporting — ADDRESSED (src/recovery.js:41).
  Magic number — ADDRESSED (src/recovery.js:7). New breakage: none.
  Verdict: all findings addressed.

[Ledger: Task 2: fix round 1/5 (2 addressed, 0 open; commits d4e5f6a..b7c8d9e)]
[Ledger: Task 2: complete (commits d4e5f6a..b7c8d9e, review clean)]

...

[After all tasks]
[Run review-package PLAN_FILE MERGE_BASE HEAD; dispatch final code-reviewer, most capable model]
Final reviewer: All requirements met. Deferred minors triaged: none block merge.

[Delete this plan's workspace — the record now lives in git]

Done! Using superpowers:finishing-a-development-branch.
```
