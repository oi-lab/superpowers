# Superpowers

Superpowers est une méthodologie de développement logiciel complète pour tes agents
de code, bâtie sur un ensemble de skills composables et quelques instructions
initiales qui garantissent que l'agent les utilise.

> **Fork personnel (oi-lab).** Ce fork est optimisé pour réduire la consommation de
> tokens et faciliter la relecture :
> - Cible **Claude Code et Antigravity uniquement** — le support des autres harnais
>   (Codex, Cursor, Copilot, Gemini, Kimi, OpenCode, Pi) a été retiré.
> - **Zéro télémétrie** : plus aucun asset distant ni appel sortant.
> - Skill **`communication-compacte`** actif par défaut (sortie dense, précision
>   technique préservée).
> - Déclenchement des skills **proportionné à la tâche** (les tâches triviales ne
>   passent pas par un workflow lourd ; les sous-agents parallèles sont opt-in).
> - Contenu des skills **traduit en français**.

## Comment ça marche

Dès que tu lances ton agent de code et qu'il voit que tu construis quelque chose, il
ne se jette *pas* sur le code. Il prend du recul et cherche à comprendre ce que tu
veux vraiment faire. Une fois une spec dégagée de la conversation, il te la présente
par morceaux assez courts pour être lus.

Après ta validation du design, l'agent produit un plan d'implémentation assez clair
pour être suivi à la lettre, en insistant sur le TDD rouge/vert, YAGNI et DRY. Puis,
sur ton « go », il exécute — en solo pour l'ordinaire, ou via des sous-agents pour
les gros plans (opt-in). Les skills se déclenchent automatiquement, proportionnés à
l'ampleur de la tâche.

## Installation

### Claude Code

Superpowers est disponible via le [marketplace officiel des plugins Claude](https://claude.com/plugins/superpowers).

#### Marketplace officiel

```bash
/plugin install superpowers@claude-plugins-official
```

#### Marketplace Superpowers

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

> Pour installer CE fork, utilise ton propre marketplace/dépôt pointant sur
> `oi-lab/superpowers` plutôt que le dépôt upstream.

### Antigravity

Installe Superpowers comme plugin depuis ce dépôt :

```bash
agy plugin install https://github.com/oi-lab/superpowers
```

Antigravity exécute le hook `session-start` du plugin, donc Superpowers est actif dès
le premier message. Réinstalle avec la même commande pour mettre à jour.

## Le workflow de base

1. **brainstorming** — avant d'écrire du code. Affine l'idée par questions, explore
   les alternatives, présente le design par sections. La profondeur s'adapte à la
   tâche (une phrase pour un petit changement, un document pour un système).
2. **using-git-worktrees** — après l'approbation du design. Crée un espace de travail
   isolé sur une nouvelle branche, lance le setup, vérifie une baseline de tests propre.
3. **writing-plans** — avec le design approuvé. Découpe le travail en tâches en petites
   bouchées, chacune avec chemins exacts, code complet, étapes de vérification.
4. **subagent-driven-development** (opt-in) ou **executing-plans** — exécute le plan.
   Sous-agent par tâche avec revue en deux étapes, ou exécution par lots avec points
   de contrôle humains.
5. **test-driven-development** — pendant l'implémentation. Impose RED-GREEN-REFACTOR.
6. **requesting-code-review** / **receiving-code-review** — entre les tâches.
7. **finishing-a-development-branch** — quand les tâches sont finies. Vérifie les
   tests, présente les options (merge/PR/garder/jeter), nettoie le worktree.

## Ce qu'il y a dedans

### Bibliothèque de skills

**Communication**
- **communication-compacte** — mode de sortie compact par défaut (spécifique à ce fork)

**Bootstrap**
- **using-superpowers** — introduction au système de skills, règle de déclenchement proportionné

**Tests**
- **test-driven-development** — cycle RED-GREEN-REFACTOR

**Débogage**
- **systematic-debugging** — recherche de cause racine en 4 phases
- **verification-before-completion** — vérifier que c'est réellement corrigé

**Collaboration**
- **brainstorming** — affinage de design par le dialogue
- **writing-plans** / **executing-plans** — plans d'implémentation détaillés / exécution par lots
- **dispatching-parallel-agents** — workflows de sous-agents concurrents (opt-in)
- **requesting-code-review** / **receiving-code-review** — demander / recevoir une revue
- **using-git-worktrees** — branches de dev parallèles
- **finishing-a-development-branch** — décision merge/PR
- **subagent-driven-development** — itération rapide avec revue en deux étapes (opt-in)

**Méta**
- **writing-skills** — créer de nouveaux skills

## Philosophie

- **Test-Driven Development** — écrire les tests d'abord
- **Systématique plutôt qu'ad hoc** — le process plutôt que la devinette
- **Réduction de complexité** — la simplicité comme objectif premier
- **Preuve plutôt qu'affirmation** — vérifier avant de déclarer le succès
- **Proportionnalité** — l'effort du process s'adapte à l'ampleur de la tâche

## Tests

- **`tests/`** — le code non-LLM du plugin fonctionne-t-il ? Tests d'intégration
  bash/node pour le serveur brainstorm et les utilitaires. Voir `docs/testing.md`.
- **`evals/`** — les agents se comportent-ils correctement sur de vraies sessions LLM ?
  Harnais `drill` pilotant de vraies sessions Claude Code.

## Télémétrie

Aucune. Ce fork ne charge aucun asset distant et ne fait aucun appel sortant. Le
branding du compagnon visuel est en texte seul, entièrement autonome.

## Licence

Licence MIT — voir le fichier LICENSE.

## Crédits

Superpowers est créé à l'origine par [Jesse Vincent](https://blog.fsck.com) et
l'équipe de [Prime Radiant](https://primeradiant.com). Ce dépôt en est un fork
personnel (oi-lab) modifié pour un usage avec Claude Code.

- Projet d'origine : https://github.com/obra/superpowers
- Annonce de sortie : https://blog.fsck.com/2025/10/09/superpowers/
