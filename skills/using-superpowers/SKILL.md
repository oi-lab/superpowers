---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, invoking them for substantial work while answering trivial requests directly
---

<SUBAGENT-STOP>
Si tu as été dispatché comme sous-agent pour une tâche précise, ignore ce skill.
</SUBAGENT-STOP>

## La règle (proportionnée à la tâche)

Avant d'agir sur un **travail substantiel** — créer/modifier une fonctionnalité,
refactorer, déboguer un problème non trivial, planifier, réviser du code —
vérifie s'il existe un skill applicable et **invoque-le avant toute autre action**
(y compris explorer le code ou poser des questions de clarification).

**Tâches triviales → réponds directement, sans skill** : question factuelle,
lecture ou explication d'un fichier, one-liner, commande unique, correction
évidente. N'impose pas un workflow lourd là où il n'apporte rien.

Dans le doute : si la tâche tient en **une action sûre et réversible**, traite-la
directement ; sinon, passe par le skill.

Puis annonce « J'utilise [skill] pour [but] » et suis-le. S'il a une checklist,
crée un todo par item.

**Avant le mode plan** : si tu n'as pas encore brainstormé un travail substantiel,
invoque brainstorming d'abord.

## Priorité des skills

Quand plusieurs s'appliquent, les skills de **process** d'abord (ils fixent
l'approche), puis les skills d'**implémentation**.

- « Construisons X » → brainstorming, puis implémentation.
- « Corrige ce bug » (non trivial) → systematic-debugging, puis skills du domaine.

## Workflows lourds = opt-in

`subagent-driven-development` et `dispatching-parallel-agents` **multiplient les
tokens** (chaque sous-agent reçoit son propre contexte). Ne les déclenche **pas**
par défaut : réserve-les aux gros plans à tâches multiples et indépendantes, ou
quand ton partenaire humain les demande explicitement.

## Signaux d'alerte

| Pensée | Réalité |
|--------|---------|
| « Question simple, je saute le skill » | OK si c'est vraiment trivial. Faux dès qu'il y a du travail réel. |
| « Petite tâche → workflow complet quand même » | Proportionne : design en une phrase, pas de cérémonie. |
| « Je lance des sous-agents pour aller plus vite » | Coûteux en tokens. Opt-in uniquement. |
| « Je me souviens de ce skill » | Les skills évoluent. Relis la version courante. |

## Instructions utilisateur

CLAUDE.md, AGENTS.md et les demandes directes priment sur les skills, qui priment
sur le comportement par défaut. Ne saute un workflow que si ton partenaire humain
te l'a explicitement demandé.

## Adaptation plateforme

Si ton harness apparaît ici, lis sa référence : Antigravity → `references/antigravity-tools.md`.
