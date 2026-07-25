---
name: using-git-worktrees
description: À utiliser au démarrage d'un travail de fonctionnalité nécessitant l'isolation de l'espace de travail courant, ou avant d'exécuter un plan d'implémentation - garantit un espace de travail isolé via les outils natifs ou, à défaut, un git worktree
---

# Utiliser les git worktrees

## Vue d'ensemble

**Principe fondamental :** garantir un espace de travail isolé — détecte d'abord une isolation existante, puis outils natifs, puis à défaut git manuel. Ne combats jamais le harnais.

**Annonce au démarrage :** « J'utilise le skill using-git-worktrees pour mettre en place un espace de travail isolé. »

## Étape 0 : Détecter une isolation existante

**Avant de créer quoi que ce soit, vérifie si tu es déjà dans un espace isolé.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Garde-fou sous-module :** `GIT_DIR != GIT_COMMON` est aussi vrai dans un sous-module git. Avant de conclure « déjà dans un worktree », vérifie que tu n'es pas dans un sous-module :

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**Si `GIT_DIR != GIT_COMMON` (et pas un sous-module) :** tu es déjà dans un worktree lié. Passe à l'Étape 2. NE crée PAS un autre worktree. Rapporte selon l'état de la branche :
- Sur une branche : « Déjà isolé à `<path>` sur la branche `<name>`. »
- HEAD détachée : « Déjà isolé à `<path>` (HEAD détachée, géré en externe). Création de branche nécessaire à la fin. »

**Si `GIT_DIR == GIT_COMMON` (ou dans un sous-module) :** tu es dans un checkout normal. Si l'utilisateur n'a pas déjà indiqué sa préférence, demande son consentement :

> « Souhaitez-vous un worktree isolé ? Cela protège votre branche courante. »

Honore une préférence déjà déclarée sans redemander. Si refus, travaille sur place et passe à l'Étape 2.

## Étape 1 : Créer l'espace de travail isolé

**Deux mécanismes, dans cet ordre :**

### 1a. Outils de worktree natifs (préférés)

As-tu déjà un moyen de créer un worktree — outil `EnterWorktree`, commande `/worktree`, ou flag `--worktree` ? Si oui, utilise-le et passe à l'Étape 2. Les outils natifs gèrent placement, branche et nettoyage ; les contourner crée un état fantôme ingérable. Ne passe à 1b qu'à défaut d'outil natif.

### 1b. Repli sur git worktree

**À n'utiliser que si l'Étape 1a ne s'applique pas.** Crée un worktree manuellement avec git.

#### Choix du répertoire

Ordre de priorité (une préférence explicite prime sur l'état du système de fichiers) :

1. **Une préférence déclarée dans tes instructions** → utilise-la sans demander.

2. **Un répertoire de worktree local au projet existant :**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   S'il existe, utilise-le ; `.worktrees` gagne si les deux existent.

3. **Sinon**, défaut `.worktrees/` à la racine du projet.

#### Vérification de sécurité (répertoires locaux)

**Tu DOIS vérifier que le répertoire est ignoré avant de créer le worktree :**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**S'il n'est PAS ignoré :** ajoute-le au .gitignore, committe, puis continue (évite de committer le contenu du worktree dans le dépôt).

#### Créer le worktree

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Repli sandbox :** si `git worktree add` échoue par erreur de permission (sandbox), préviens l'utilisateur et travaille dans le répertoire courant ; lance la config et les tests de référence sur place.

## Étape 2 : Configuration du projet

Détecte et lance la config appropriée :

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

Lance les tests pour vérifier que l'espace de travail démarre propre :

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**Tests échouent :** rapporte les échecs, demande s'il faut continuer ou investiguer. **Tests passent :** rapporte que c'est prêt (chemin complet du worktree, nombre de tests / 0 échec, fonctionnalité à implémenter).

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
| « `git worktree add` est plus rapide que chercher un outil natif » | Un outil natif (ex. `EnterWorktree`) gère placement, branchage et nettoyage. Le contourner est l'erreur nº 1 : il crée un état fantôme que ton harnais ne peut ni voir ni gérer. |
| « Le répertoire de worktree est sûrement déjà ignoré » | Lance `git check-ignore`. Un répertoire de worktree non ignoré committe tout l'arbre dans le dépôt. |
| « N'importe quel nom de répertoire convient » | Les instructions explicites priment sur un répertoire local existant, qui prime sur le défaut `.worktrees/`. |
| « L'espace est neuf — les tests de référence peuvent attendre » | Une base de référence sale rend ambigu tout échec ultérieur. Lance les tests maintenant ; passer outre des échecs est la décision de ton partenaire humain. |
