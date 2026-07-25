---
name: brainstorming
description: "Use before substantial creative work - creating a feature, building a component, adding functionality, or a non-trivial behavior change - pour explorer l'intention, les besoins et le design avant l'implémentation. Les changements triviaux ou d'une ligne n'en ont pas besoin."
---

# Transformer des idées en designs

Transforme des idées en designs et spécifications aboutis par un dialogue collaboratif. Comprends d'abord le contexte du projet, pose des questions une à la fois, puis présente le design et obtiens l'approbation.

<HARD-GATE>
N'invoque AUCUN skill d'implémentation, n'écris aucun code et ne mets en place aucun squelette de projet tant que tu n'as pas présenté un design et que ton partenaire humain ne l'a pas approuvé. La PROFONDEUR de ce design s'adapte à la tâche : une ou deux phrases pour un petit changement, un document complet pour un système. Le gate (présenter un design + obtenir l'approbation) tient toujours ; le cérémonial autour, non.
</HARD-GATE>

## Mise à l'échelle : adapte le cérémonial à la tâche

Le gate est universel ; le poids du processus ne l'est pas. Pour un petit changement bien compris, présente un design d'une phrase en ligne, obtiens un oui, et construis — saute le document écrit, le commit et le gate de revue séparé (étapes 6-8). Réserve le flux complet (spec écrite → auto-revue → revue par l'utilisateur) au travail assez substantiel pour qu'un artefact écrit partagé justifie son coût en tokens.

## Checklist

Crée une tâche par item et complète-les dans l'ordre. Pour un petit changement confirmé en ligne, fais les étapes 1, 3, 5 légèrement et saute les étapes 6-8.

1. **Explorer le contexte du projet** — fichiers, docs, commits récents
2. **Proposer le compagnon visuel au bon moment** — PAS d'emblée ; la première fois qu'une question serait plus claire montrée que décrite, propose-le (dans son propre message). Si aucune ne surgit, ne le propose jamais. Voir section Compagnon Visuel.
3. **Poser des questions de clarification** — une à la fois : objectif, contraintes, critères de succès
4. **Proposer 2-3 approches** — avec compromis et ta recommandation
5. **Présenter le design** — en sections dimensionnées à leur complexité, approbation après chaque section
6. **Écrire le document de design** — sauvegarder dans `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` et commiter
7. **Auto-revue de la spec** — vérification en ligne : placeholders, contradictions, ambiguïtés, périmètre (voir ci-dessous)
8. **L'utilisateur relit la spec écrite** — avant de continuer
9. **Transition vers l'implémentation** — invoquer le skill writing-plans

**L'état terminal est l'invocation de writing-plans.** N'invoque PAS frontend-design, mcp-builder, ni aucun autre skill d'implémentation. Le SEUL skill que tu invoques après brainstorming est writing-plans.

## Le Processus

**Comprendre l'idée :**

- Examine d'abord l'état actuel du projet (fichiers, docs, commits récents)
- Avant de poser des questions détaillées, évalue le périmètre : si la demande décrit plusieurs sous-systèmes indépendants (ex. « plateforme avec chat, stockage, facturation et analytics »), signale-le immédiatement plutôt que d'affiner un projet qui doit d'abord être décomposé.
- Si le projet est trop grand pour une seule spec, aide l'utilisateur à le décomposer en sous-projets (pièces indépendantes, relations, ordre), puis brainstorme le premier. Chaque sous-projet a son propre cycle spec → plan → implémentation.
- Pour les projets bien dimensionnés, pose les questions une à la fois — une seule par message ; privilégie le choix multiple, l'ouvert est acceptable. Concentre-toi sur objectif, contraintes, critères de succès.

**Explorer les approches :**

- Propose 2-3 approches avec compromis, en commençant par celle que tu recommandes et pourquoi
- Applique YAGNI sans pitié — retire les fonctionnalités inutiles de chaque approche

**Présenter le design :**

- Une fois que tu crois comprendre, présente le design ; dimensionne chaque section à sa complexité (quelques phrases si simple, jusqu'à 200-300 mots si nuancé)
- Demande après chaque section si ça semble juste ; sois prêt à revenir en arrière
- Couvre : architecture, composants, flux de données, gestion d'erreurs, tests

**Concevoir pour l'isolation et la clarté :**

- Découpe le système en unités plus petites, chacune avec un but clair, communiquant par interfaces bien définies, comprises et testées indépendamment
- Pour chaque unité, réponds : que fait-elle, comment l'utilise-t-on, de quoi dépend-elle ? Peut-on comprendre ce qu'elle fait sans lire ses internes, et changer les internes sans casser les consommateurs ? Sinon, retravaille les frontières.
- Des unités petites et délimitées sont plus faciles à manipuler pour toi ; un fichier qui grossit fait souvent trop de choses.

**Travailler dans des codebases existantes :**

- Explore la structure actuelle et suis les patterns existants avant de proposer des changements
- Là où du code existant a des problèmes qui affectent le travail (fichier trop gros, frontières floues, responsabilités emmêlées), inclus des améliorations ciblées dans le design — sans refactoring sans lien.

## Après le Design

**Documentation :**

- Écris la spec validée dans `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` (les préférences de l'utilisateur priment sur ce défaut)
- Utilise le skill elements-of-style:writing-clearly-and-concisely s'il est disponible
- Commite le document dans git

**Auto-revue de la spec :** regarde le document avec un œil neuf :

1. **Chasse aux placeholders :** « TBD », « TODO », sections incomplètes, besoins vagues ? Corrige.
2. **Cohérence interne :** des sections se contredisent-elles ? L'architecture correspond-elle aux fonctionnalités ?
3. **Vérification de périmètre :** assez ciblé pour un seul plan, ou à décomposer ?
4. **Vérification d'ambiguïté :** un besoin interprétable de deux façons ? Tranche et rends-le explicite.

Corrige en ligne. Pas besoin de re-relire.

**Gate de revue par l'utilisateur :** une fois la boucle passée, demande à l'utilisateur de relire la spec avant de continuer :

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Attends la réponse. S'il demande des changements, fais-les et relance la boucle de revue. Ne continue qu'une fois approuvé.

**Implémentation :**

- Invoque le skill writing-plans pour créer un plan détaillé. N'invoque AUCUN autre skill.

## Compagnon Visuel

Un compagnon basé navigateur pour montrer maquettes, diagrammes et options visuelles pendant le brainstorming — un outil, pas un mode. L'accepter le rend disponible pour les questions qui bénéficient d'un traitement visuel ; cela ne veut PAS dire que chaque question passe par le navigateur.

**Proposer le compagnon (au bon moment) :** PAS d'emblée. Attends qu'une question soit vraiment plus claire montrée que dite — une vraie question de maquette / mise en page / diagramme, pas simplement un *sujet* d'UI. La première fois, propose-le, dans son propre message :
> "This next part might be easier if I show you — I can put together mockups, diagrams, and comparisons in a browser tab as we go. It's still new and can be token-intensive. Want me to? I'll open it for you."

**Cette offre DOIT être son propre message** — rien d'autre. Attends la réponse. S'il accepte, démarre le serveur avec `--open`. S'il refuse, continue en texte seul et ne le propose plus à moins qu'il le relance.

**Décision par question :** même après acceptation, décide POUR CHAQUE QUESTION navigateur ou terminal. Le test : **l'utilisateur comprendrait-il mieux ceci en le voyant qu'en le lisant ?**

- **Navigateur** pour du contenu qui EST visuel — maquettes, wireframes, comparaisons de mises en page, diagrammes d'architecture, designs côte à côte
- **Terminal** pour du contenu textuel — questions de besoins, choix conceptuels, compromis, options A/B/C/D, décisions de périmètre

Un sujet d'UI n'est pas automatiquement une question visuelle : « Que signifie personnalité ici ? » est conceptuel (terminal) ; « Quelle mise en page de wizard marche mieux ? » est visuel (navigateur).

S'il accepte le compagnon, lis le guide avant de continuer : `skills/brainstorming/visual-companion.md`
