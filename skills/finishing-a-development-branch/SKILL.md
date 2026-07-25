---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work
---

# Terminer une branche de développement

## Vue d'ensemble

**Principe fondamental :** vérifier les tests → détecter l'environnement → présenter les options → exécuter le choix → nettoyer.

**Annonce au début :** « J'utilise le skill finishing-a-development-branch. »

## Étape 1 : Vérifier les tests

Lance la suite complète (`npm test` / `cargo test` / `pytest` / `go test ./...`).

**Si les tests échouent**, rapporte et arrête-toi — le menu ne vient qu'après une suite au vert :

```
Tests failing (<N> failures). Must fix before completing:

[Show failures]
```

**Si les tests passent :** continue à l'étape 2.

## Étape 2 : Détecter l'environnement

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

Détermine le menu à afficher et le nettoyage :

| État | Menu | Nettoyage |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (dépôt normal) | 3 options standard | Aucun worktree |
| `GIT_DIR != GIT_COMMON`, branche nommée | 3 options standard | Selon provenance (étape 6) |
| `GIT_DIR != GIT_COMMON`, HEAD détachée | 2 options (pas de merge) | Externe — laisser |

## Étape 3 : Déterminer la branche de base

La branche de base est celle d'où ce travail est parti — en général nommée dans le plan, la conversation, ou l'upstream. Si inconnue, demande : « Cette branche est partie de <estimation> - correct ? » Merger sur la mauvaise base coûte cher à défaire.

## Étape 4 : Présenter les options

**Dépôt normal et worktree à branche nommée — exactement ces 3 options :**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**HEAD détachée — exactement ces 2 options :**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Présente le menu exactement tel qu'écrit. Jeter le travail n'arrive qu'en réponse à une demande explicite de ton partenaire humain (voir plus bas). Attends sa réponse ; la décision d'intégration lui revient.

## Étape 5 : Exécuter le choix

### Option 1 : Merger localement

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

Si les tests échouent sur le résultat mergé : arrête-toi, laisse worktree et branche en place, investigue — rien n'a été poussé, le merge est local et récupérable.

Une fois au vert : nettoie le worktree (étape 6), puis supprime la branche :

```bash
git branch -d <feature-branch>
```

### Option 2 : Pousser et créer une PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

Crée ensuite la pull/merge request contre <base-branch> avec l'outillage de la forge (sa CLI, ou l'URL affichée au push), en suivant le gabarit de PR et les conventions du dépôt s'ils existent, et rapporte l'URL à ton partenaire humain.

Garde le worktree — ton partenaire humain itère dessus sur les retours de la PR.

### Option 3 : Garder tel quel

Rapporte : « Je garde la branche <name>. Worktree préservé à <path>. »

### Si ton partenaire humain demande de jeter le travail

Uniquement sur demande explicite. Confirme d'abord :

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Attends cette confirmation exacte :

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Puis nettoie le worktree (étape 6) et force la suppression :

```bash
git branch -D <feature-branch>
```

## Étape 6 : Nettoyer l'espace de travail

**S'exécute pour l'option 1 et les jetages confirmés.** Les options 2 et 3 préservent le worktree. Les deux appelants ont déjà changé de répertoire vers la racine du dépôt principal (le retrait doit s'exécuter depuis l'extérieur du worktree) et utilisent `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` capturés à l'étape 2.

**Si `GIT_DIR == GIT_COMMON` :** dépôt normal, aucun worktree. Terminé.

**Si `WORKTREE_PATH` est sous `.worktrees/` ou `worktrees/` :** Superpowers a créé ce worktree — nettoie :

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**Sinon :** l'hôte possède cet espace de travail — laisse-le en place. Si ta plateforme fournit un outil de sortie d'espace de travail, utilise-le.

## Référence rapide

| Option | Merge | Push | Garde le worktree | Nettoie la branche |
|--------|-------|------|---------------|----------------|
| 1. Merger localement | oui | - | - | oui |
| 2. Créer une PR | - | oui | oui | - |
| 3. Garder tel quel | - | - | oui | - |
| Jeter (sur demande explicite uniquement) | - | - | - | oui (forcé) |

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Les tests sont passés plus tôt » | Lance la suite sur l'arbre à intégrer. Un run au vert ne prouve que l'arbre sur lequel il a tourné. |
| « De toute évidence il veut merger » | L'intégration est la décision de ton partenaire humain. Présente le menu et attends. |
| « Il semble en avoir fini — je vais proposer de jeter » | Le menu est complet tel qu'écrit. Le jetage n'arrive que sur demande explicite. |
| « "Ouais, dégage ça" vaut confirmation » | Seul le mot tapé `discard` autorise la suppression. |
| « La PR est en place, le worktree encombre » | Les retours de PR se corrigent dans ce worktree. Il reste jusqu'à l'intégration. |
| « Cet autre worktree a l'air périmé — je le nettoie aussi » | Ne nettoie que les worktrees sous `.worktrees/` ou `worktrees/`. Le reste appartient à l'hôte. |
| « L'échec du résultat mergé est sûrement instable » | Un résultat mergé qui échoue arrête tout. Branche et worktree restent pendant que tu investigues. |
| « La branche de base est évidemment main » | Confirme le point de fork ou demande. Merger sur la mauvaise base coûte cher. |
| « Le push a été rejeté — un force-push réglera ça » | Le remote a bougé. Investigue ; ne force-push que sur demande explicite de ton partenaire humain. |
