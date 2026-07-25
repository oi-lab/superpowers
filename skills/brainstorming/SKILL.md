---
name: brainstorming
description: "Use before substantial creative work - creating a feature, building a component, adding functionality, or a non-trivial behavior change - pour explorer l'intention, les besoins et le design avant l'implémentation. Les changements triviaux ou d'une ligne n'en ont pas besoin."
---

# Transformer des idées en designs

Aide à transformer des idées en designs et spécifications aboutis, par un dialogue collaboratif naturel.

Commence par comprendre le contexte actuel du projet, puis pose des questions une à la fois pour affiner l'idée. Une fois que tu comprends ce que tu construis, présente le design et obtiens l'approbation de l'utilisateur.

<HARD-GATE>
N'invoque AUCUN skill d'implémentation, n'écris aucun code et ne mets en place aucun squelette de projet tant que tu n'as pas présenté un design et que ton partenaire humain ne l'a pas approuvé. La PROFONDEUR de ce design s'adapte à la tâche : une ou deux phrases pour un petit changement, un document complet pour un système. Le gate (présenter un design + obtenir l'approbation) tient toujours ; le cérémonial autour, non.
</HARD-GATE>

## Mise à l'échelle : adapte le cérémonial à la tâche

Le gate est universel ; le poids du processus ne l'est pas. Pour un petit changement bien compris, présente un design d'une phrase en ligne, obtiens un oui, et construis — saute le document de design écrit, le commit et le gate de revue séparé (étapes 6-8 de la checklist). Réserve le flux complet (spec écrite → auto-revue → revue du fichier par l'utilisateur) au travail assez substantiel pour qu'un artefact écrit partagé justifie son coût en tokens. Le travail « simple » fait quand même émerger ses hypothèses — en une phrase, pas un document.

## Checklist

Crée une tâche par item et complète-les dans l'ordre. Pour un petit changement confirmé
en ligne (voir « Mise à l'échelle » ci-dessus), fais les étapes 1, 3, 5 légèrement et saute les étapes 6-8.

1. **Explorer le contexte du projet** — vérifier les fichiers, docs, commits récents
2. **Proposer le compagnon visuel au bon moment** — PAS d'emblée. La première fois qu'une question serait vraiment plus claire montrée que décrite, propose-le à ce moment-là (dans son propre message) ; sur approbation son onglet de navigateur s'ouvre pour toi. Si aucune question visuelle ne surgit jamais, ne le propose jamais. Voir la section Compagnon Visuel ci-dessous.
3. **Poser des questions de clarification** — une à la fois, comprendre l'objectif/les contraintes/les critères de succès
4. **Proposer 2-3 approches** — avec leurs compromis et ta recommandation
5. **Présenter le design** — en sections dimensionnées à leur complexité, obtenir l'approbation de l'utilisateur après chaque section
6. **Écrire le document de design** — sauvegarder dans `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` et commiter
7. **Auto-revue de la spec** — vérification rapide en ligne des placeholders, contradictions, ambiguïtés, périmètre (voir ci-dessous)
8. **L'utilisateur relit la spec écrite** — demander à l'utilisateur de relire le fichier de spec avant de continuer
9. **Transition vers l'implémentation** — invoquer le skill writing-plans pour créer le plan d'implémentation

Le déroulé : explorer le contexte → poser les questions de clarification → proposer 2-3 approches → présenter les sections du design → (si l'utilisateur n'approuve pas, réviser et représenter) → écrire le document de design → auto-revue de la spec (corriger en ligne) → (si l'utilisateur demande des changements, retour à l'écriture du document) → une fois la spec approuvée, invoquer le skill writing-plans.

**L'état terminal est l'invocation de writing-plans.** N'invoque PAS frontend-design, mcp-builder, ni aucun autre skill d'implémentation. Le SEUL skill que tu invoques après brainstorming est writing-plans.

## Le Processus

**Comprendre l'idée :**

- Examine d'abord l'état actuel du projet (fichiers, docs, commits récents)
- Avant de poser des questions détaillées, évalue le périmètre : si la demande décrit plusieurs sous-systèmes indépendants (ex. « construire une plateforme avec chat, stockage de fichiers, facturation et analytics »), signale-le immédiatement. Ne dépense pas des questions à affiner les détails d'un projet qui doit d'abord être décomposé.
- Si le projet est trop grand pour une seule spec, aide l'utilisateur à le décomposer en sous-projets : quelles sont les pièces indépendantes, comment se relient-elles, dans quel ordre les construire ? Puis brainstorme le premier sous-projet via le flux de design normal. Chaque sous-projet a son propre cycle spec → plan → implémentation.
- Pour les projets bien dimensionnés, pose les questions une à la fois pour affiner l'idée
- Privilégie les questions à choix multiples quand c'est possible, mais l'ouvert est acceptable aussi
- Une seule question par message — si un sujet nécessite plus d'exploration, découpe-le en plusieurs questions
- Concentre-toi sur la compréhension : objectif, contraintes, critères de succès

**Explorer les approches :**

- Propose 2-3 approches différentes avec leurs compromis
- Présente les options de façon conversationnelle avec ta recommandation et ton raisonnement
- Commence par l'option que tu recommandes et explique pourquoi
- Applique YAGNI sans pitié — retire les fonctionnalités inutiles de chaque approche et design

**Présenter le design :**

- Une fois que tu crois comprendre ce que tu construis, présente le design
- Dimensionne chaque section à sa complexité : quelques phrases si c'est simple, jusqu'à 200-300 mots si c'est nuancé
- Demande après chaque section si ça semble juste jusque-là
- Couvre : architecture, composants, flux de données, gestion d'erreurs, tests
- Sois prêt à revenir en arrière et clarifier si quelque chose n'a pas de sens

**Concevoir pour l'isolation et la clarté :**

- Découpe le système en unités plus petites ayant chacune un but clair, communiquant par des interfaces bien définies, et pouvant être comprises et testées indépendamment
- Pour chaque unité, tu dois pouvoir répondre : que fait-elle, comment l'utilise-t-on, et de quoi dépend-elle ?
- Peut-on comprendre ce que fait une unité sans lire ses internes ? Peut-on changer les internes sans casser les consommateurs ? Sinon, les frontières doivent être retravaillées.
- Des unités plus petites et bien délimitées sont aussi plus faciles à manipuler pour toi — tu raisonnes mieux sur du code que tu peux tenir en contexte d'un coup, et tes éditions sont plus fiables quand les fichiers sont ciblés. Quand un fichier grossit, c'est souvent le signe qu'il en fait trop.

**Travailler dans des codebases existantes :**

- Explore la structure actuelle avant de proposer des changements. Suis les patterns existants.
- Là où du code existant a des problèmes qui affectent le travail (ex. un fichier devenu trop gros, des frontières floues, des responsabilités emmêlées), inclus des améliorations ciblées dans le design — comme le ferait un bon développeur dans le code où il intervient.
- Ne propose pas de refactoring sans lien. Reste concentré sur ce qui sert l'objectif courant.

## Après le Design

**Documentation :**

- Écris le design validé (spec) dans `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - (Les préférences de l'utilisateur sur l'emplacement de la spec priment sur ce défaut)
- Utilise le skill elements-of-style:writing-clearly-and-concisely s'il est disponible
- Commite le document de design dans git

**Auto-revue de la spec :**
Après avoir écrit le document de spec, regarde-le avec un œil neuf :

1. **Chasse aux placeholders :** des « TBD », « TODO », sections incomplètes ou besoins vagues ? Corrige-les.
2. **Cohérence interne :** des sections se contredisent-elles ? L'architecture correspond-elle aux descriptions de fonctionnalités ?
3. **Vérification de périmètre :** est-ce assez ciblé pour un seul plan d'implémentation, ou faut-il décomposer ?
4. **Vérification d'ambiguïté :** un besoin pourrait-il être interprété de deux façons ? Si oui, tranche et rends-le explicite.

Corrige les problèmes en ligne. Pas besoin de re-relire — corrige et avance.

**Gate de revue par l'utilisateur :**
Une fois la boucle de revue de la spec passée, demande à l'utilisateur de relire la spec écrite avant de continuer :

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Attends la réponse de l'utilisateur. S'il demande des changements, fais-les et relance la boucle de revue de la spec. Ne continue qu'une fois que l'utilisateur approuve.

**Implémentation :**

- Invoque le skill writing-plans pour créer un plan d'implémentation détaillé
- N'invoque AUCUN autre skill. writing-plans est l'étape suivante.

## Compagnon Visuel

Un compagnon basé navigateur pour montrer des maquettes, diagrammes et options visuelles pendant le brainstorming. Disponible comme outil — pas comme mode. Accepter le compagnon signifie qu'il est disponible pour les questions qui bénéficient d'un traitement visuel ; cela ne veut PAS dire que chaque question passe par le navigateur.

**Proposer le compagnon (au bon moment) :** Ne le propose PAS d'emblée. Attends qu'une question soit vraiment plus claire montrée que dite — une vraie question de maquette / mise en page / diagramme, pas simplement un *sujet* d'UI. La première fois que cela arrive, propose-le alors, dans son propre message :
> "This next part might be easier if I show you — I can put together mockups, diagrams, and comparisons in a browser tab as we go. It's still new and can be token-intensive. Want me to? I'll open it for you."

**Cette offre DOIT être son propre message.** Uniquement l'offre — pas de question de clarification, de résumé ni d'autre contenu. Attends la réponse de l'utilisateur. S'il accepte, démarre le serveur avec `--open` pour que son navigateur s'ouvre automatiquement sur le premier écran. S'il refuse, continue en texte seul et ne le propose plus à moins qu'il le relance.

**Décision par question :** Même après que l'utilisateur a accepté, décide POUR CHAQUE QUESTION s'il faut utiliser le navigateur ou le terminal. Le test : **l'utilisateur comprendrait-il mieux ceci en le voyant qu'en le lisant ?**

- **Utilise le navigateur** pour du contenu qui EST visuel — maquettes, wireframes, comparaisons de mises en page, diagrammes d'architecture, designs visuels côte à côte
- **Utilise le terminal** pour du contenu textuel — questions de besoins, choix conceptuels, listes de compromis, options textuelles A/B/C/D, décisions de périmètre

Une question sur un sujet d'UI n'est pas automatiquement une question visuelle. « Que signifie personnalité dans ce contexte ? » est une question conceptuelle — utilise le terminal. « Quelle mise en page de wizard fonctionne mieux ? » est une question visuelle — utilise le navigateur.

S'il accepte le compagnon, lis le guide détaillé avant de continuer :
`skills/brainstorming/visual-companion.md`
