---
name: using-git-worktrees
description: À utiliser au démarrage d'un travail de fonctionnalité nécessitant l'isolation de l'espace de travail courant, ou avant d'exécuter un plan d'implémentation - garantit un espace de travail isolé via les outils natifs ou, à défaut, un git worktree
---

# Utiliser les git worktrees

## Vue d'ensemble

Garantir que le travail se déroule dans un espace de travail isolé. Privilégie les outils de worktree natifs de ta plateforme. Ne recours au git worktree manuel que si aucun outil natif n'est disponible.

**Principe fondamental :** détecte d'abord une isolation existante. Puis utilise les outils natifs. Puis, à défaut, git. Ne combats jamais le harnais.

**Annonce au démarrage :** « J'utilise le skill using-git-worktrees pour mettre en place un espace de travail isolé. »

## Étape 0 : Détecter une isolation existante

**Avant de créer quoi que ce soit, vérifie si tu es déjà dans un espace de travail isolé.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Garde-fou sous-module :** `GIT_DIR != GIT_COMMON` est aussi vrai à l'intérieur d'un sous-module git. Avant de conclure « déjà dans un worktree », vérifie que tu n'es pas dans un sous-module :

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**Si `GIT_DIR != GIT_COMMON` (et pas un sous-module) :** tu es déjà dans un worktree lié. Passe à l'Étape 2 (Configuration du projet). NE crée PAS un autre worktree.

Rapporte selon l'état de la branche :
- Sur une branche : « Déjà dans un espace de travail isolé à `<path>` sur la branche `<name>`. »
- HEAD détachée : « Déjà dans un espace de travail isolé à `<path>` (HEAD détachée, géré en externe). Création de branche nécessaire à la fin. »

**Si `GIT_DIR == GIT_COMMON` (ou dans un sous-module) :** tu es dans un checkout de dépôt normal.

L'utilisateur a-t-il déjà indiqué sa préférence de worktree dans tes instructions ? Sinon, demande son consentement avant de créer un worktree :

> « Souhaitez-vous que je mette en place un worktree isolé ? Cela protège votre branche courante des changements. »

Honore toute préférence déjà déclarée sans redemander. Si l'utilisateur refuse, travaille sur place et passe à l'Étape 2.

## Étape 1 : Créer l'espace de travail isolé

**Tu disposes de deux mécanismes. Essaie-les dans cet ordre.**

### 1a. Outils de worktree natifs (préférés)

L'utilisateur a demandé un espace de travail isolé (consentement de l'Étape 0). As-tu déjà un moyen de créer un worktree ? Ce peut être un outil nommé `EnterWorktree`, `WorktreeCreate`, une commande `/worktree`, ou un flag `--worktree`. Si oui, utilise-le et passe à l'Étape 2.

Les outils natifs gèrent automatiquement le placement du répertoire, la création de branche et le nettoyage. Utiliser `git worktree add` alors que tu as un outil natif crée un état fantôme que ton harnais ne peut ni voir ni gérer.

Ne passe à l'Étape 1b que si aucun outil de worktree natif n'est disponible.

### 1b. Repli sur git worktree

**À n'utiliser que si l'Étape 1a ne s'applique pas** — aucun outil de worktree natif disponible. Crée un worktree manuellement avec git.

#### Choix du répertoire

Suis cet ordre de priorité. Une préférence explicite de l'utilisateur prime toujours sur l'état observé du système de fichiers.

1. **Vérifie dans tes instructions une préférence de répertoire de worktree déclarée.** Si l'utilisateur en a déjà spécifié une, utilise-la sans demander.

2. **Cherche un répertoire de worktree local au projet existant :**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   S'il existe, utilise-le. Si les deux existent, `.worktrees` gagne.

3. **Sans autre indication disponible**, utilise par défaut `.worktrees/` à la racine du projet.

#### Vérification de sécurité (répertoires locaux au projet uniquement)

**Tu DOIS vérifier que le répertoire est ignoré avant de créer le worktree :**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**S'il n'est PAS ignoré :** ajoute-le au .gitignore, committe le changement, puis continue.

**Pourquoi c'est critique :** évite de committer accidentellement le contenu du worktree dans le dépôt.

#### Créer le worktree

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Repli sandbox :** si `git worktree add` échoue avec une erreur de permission (refus du sandbox), dis à l'utilisateur que le sandbox a bloqué la création du worktree et que tu travailles dans le répertoire courant à la place. Puis lance la configuration et les tests de référence sur place.

## Étape 2 : Configuration du projet

Détecte automatiquement et lance la configuration appropriée :

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Étape 3 : Vérifier une base de référence propre

Lance les tests pour t'assurer que l'espace de travail démarre propre :

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**Si les tests échouent :** rapporte les échecs, demande s'il faut continuer ou investiguer.

**Si les tests passent :** rapporte que c'est prêt.

### Rapport

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Référence rapide

| Situation | Action |
|-----------|--------|
| Déjà dans un worktree lié | Sauter la création (Étape 0) |
| Dans un sous-module | Traiter comme dépôt normal (garde-fou Étape 0) |
| Outil de worktree natif disponible | L'utiliser (Étape 1a) |
| Aucun outil natif | Repli git worktree (Étape 1b) |
| `.worktrees/` existe | L'utiliser (vérifier qu'il est ignoré) |
| `worktrees/` existe | L'utiliser (vérifier qu'il est ignoré) |
| Les deux existent | Utiliser `.worktrees/` |
| Aucun n'existe | Vérifier le fichier d'instructions, puis défaut `.worktrees/` |
| Répertoire non ignoré | Ajouter au .gitignore + committer |
| Erreur de permission à la création | Repli sandbox, travailler sur place |
| Tests échouent au démarrage | Rapporter les échecs + demander |
| Pas de package.json/Cargo.toml | Sauter l'installation des dépendances |

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Je ne suis manifestement pas dans un worktree — inutile de vérifier » | Lance l'Étape 0. L'isolation créée par le harnais et les sous-modules trompent l'œil ; les commandes de détection tranchent. |
| « `git worktree add` est plus rapide que chercher un outil natif » | Un outil natif (ex. `EnterWorktree`) gère le placement, le branchage et le nettoyage. Le contourner est l'erreur nº 1 : il crée un état fantôme que ton harnais ne peut ni voir ni gérer. |
| « Le répertoire de worktree est sûrement déjà ignoré » | Lance `git check-ignore`. Un répertoire de worktree non ignoré committe tout l'arbre dans le dépôt. |
| « N'importe quel nom de répertoire convient » | Les instructions explicites priment sur un répertoire local existant, qui prime sur le défaut `.worktrees/`. |
| « L'espace est neuf — les tests de référence peuvent attendre » | Une base de référence sale rend ambigu tout échec ultérieur. Lance les tests maintenant ; passer outre des échecs est la décision de ton partenaire humain. |
