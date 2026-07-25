# Remonter à la cause racine

## Vue d'ensemble

Les bugs se manifestent souvent profondément dans la pile d'appels (git init dans le mauvais répertoire, fichier créé au mauvais endroit, base de données ouverte avec le mauvais chemin). Ton instinct est de corriger là où l'erreur apparaît, mais c'est traiter un symptôme.

**Principe central :** remonte à rebours la chaîne d'appels jusqu'à trouver le déclencheur d'origine, puis corrige à la source.

## Quand l'utiliser

Si le bug apparaît profondément dans la pile et que tu peux remonter à rebours, remonte jusqu'au déclencheur d'origine — et, mieux encore, ajoute aussi de la défense en profondeur. Si tu ne peux pas remonter (impasse), corrige au point du symptôme.

**Utilise quand :**
- L'erreur se produit profondément dans l'exécution (pas au point d'entrée)
- La stack trace montre une longue chaîne d'appels
- L'origine des données invalides n'est pas claire
- Il faut trouver quel test/code déclenche le problème

## Le processus de traçage

### 1. Observe le symptôme
```
Error: git init failed in ~/project/packages/core
```

### 2. Trouve la cause immédiate
**Quel code cause directement ceci ?**
```typescript
await execFileAsync('git', ['init'], { cwd: projectDir });
```

### 3. Demande : qu'est-ce qui a appelé ceci ?
```typescript
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  → called by Session.initializeWorkspace()
  → called by Session.create()
  → called by test at Project.create()
```

### 4. Continue de remonter
**Quelle valeur a été passée ?**
- `projectDir = ''` (chaîne vide !)
- Une chaîne vide comme `cwd` se résout en `process.cwd()`
- C'est le répertoire du code source !

### 5. Trouve le déclencheur d'origine
**D'où venait la chaîne vide ?**
```typescript
const context = setupCoreTest(); // Returns { tempDir: '' }
Project.create('name', context.tempDir); // Accessed before beforeEach!
```

## Ajouter des stack traces

Quand tu ne peux pas tracer manuellement, ajoute de l'instrumentation :

```typescript
// Before the problematic operation
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });

  await execFileAsync('git', ['init'], { cwd: directory });
}
```

**Critique :** utilise `console.error()` dans les tests (pas le logger — il peut ne pas s'afficher).

**Lance et capture :**
```bash
npm test 2>&1 | grep 'DEBUG git init'
```

**Analyse les stack traces :**
- Cherche les noms de fichiers de test
- Trouve le numéro de ligne qui déclenche l'appel
- Identifie le pattern (même test ? même paramètre ?)

## Trouver quel test cause la pollution

Si quelque chose apparaît durant les tests mais que tu ne sais pas quel test :

Utilise le script de bissection `find-polluter.sh` de ce répertoire :

```bash
./find-polluter.sh '.git' 'src/**/*.test.ts'
```

Lance les tests un par un, s'arrête au premier pollueur. Voir le script pour l'usage.

## Exemple réel : projectDir vide

**Symptôme :** `.git` créé dans `packages/core/` (code source)

**Chaîne de traçage :**
1. `git init` s'exécute dans `process.cwd()` ← paramètre cwd vide
2. WorktreeManager appelé avec un projectDir vide
3. Session.create() a passé une chaîne vide
4. Le test a accédé à `context.tempDir` avant beforeEach
5. setupCoreTest() renvoie `{ tempDir: '' }` initialement

**Cause racine :** initialisation de variable au niveau du module accédant à une valeur vide

**Correction :** fait de tempDir un getter qui lève une erreur s'il est accédé avant beforeEach

**Défense en profondeur ajoutée en plus :**
- Couche 1 : Project.create() valide le répertoire
- Couche 2 : WorkspaceManager valide qu'il n'est pas vide
- Couche 3 : garde NODE_ENV qui refuse git init hors de tmpdir
- Couche 4 : journalisation de la stack trace avant git init

## Principe clé

Une fois la cause immédiate trouvée, remonte niveau par niveau tant que ce n'est pas la source ; à la source, corrige puis ajoute une validation à chaque couche pour rendre le bug impossible. **Ne corrige JAMAIS uniquement là où l'erreur apparaît.** Remonte jusqu'au déclencheur d'origine.

## Astuces de stack trace

**Dans les tests :** utilise `console.error()` et non le logger — le logger peut être supprimé
**Avant l'opération :** journalise avant l'opération dangereuse, pas après son échec
**Inclus le contexte :** répertoire, cwd, variables d'environnement, timestamps
**Capture la pile :** `new Error().stack` montre la chaîne d'appels complète

## Impact concret

D'une session de débogage (2025-10-03) :
- Cause racine trouvée via un traçage sur 5 niveaux
- Corrigé à la source (validation par getter)
- 4 couches de défense ajoutées
- 1847 tests passés, zéro pollution
