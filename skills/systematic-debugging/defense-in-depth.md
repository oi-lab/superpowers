# Validation en défense en profondeur

## Vue d'ensemble

Quand tu corriges un bug causé par des données invalides, ajouter une validation à un seul endroit paraît suffisant. Mais cette vérification unique peut être contournée par d'autres chemins de code, un refactoring, ou des mocks.

**Principe central :** valide à CHAQUE couche que les données traversent. Rends le bug structurellement impossible.

## Pourquoi plusieurs couches

Validation unique : « On a corrigé le bug »
Plusieurs couches : « On a rendu le bug impossible »

Des couches différentes attrapent des cas différents :
- La validation à l'entrée attrape la plupart des bugs
- La logique métier attrape les cas limites
- Les gardes d'environnement empêchent les dangers propres à un contexte
- La journalisation de debug aide quand les autres couches échouent

## Les quatre couches

### Couche 1 : validation au point d'entrée
**But :** rejeter une entrée manifestement invalide à la frontière de l'API

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### Couche 2 : validation de la logique métier
**But :** s'assurer que les données ont du sens pour cette opération

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### Couche 3 : gardes d'environnement
**But :** empêcher les opérations dangereuses dans des contextes spécifiques

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `Refusing git init outside temp dir during tests: ${directory}`
      );
    }
  }
  // ... proceed
}
```

### Couche 4 : instrumentation de debug
**But :** capturer le contexte pour l'analyse forensique

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... proceed
}
```

## Appliquer le pattern

Quand tu trouves un bug :

1. **Trace le flux de données** — d'où vient la mauvaise valeur ? Où est-elle utilisée ?
2. **Cartographie tous les points de contrôle** — liste chaque point que les données traversent
3. **Ajoute une validation à chaque couche** — entrée, métier, environnement, debug
4. **Teste chaque couche** — essaie de contourner la couche 1, vérifie que la couche 2 l'attrape

## Exemple issu d'une session

Bug : un `projectDir` vide a causé un `git init` dans le code source

**Flux de données :**
1. Setup de test → chaîne vide
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` s'exécute dans `process.cwd()`

**Quatre couches ajoutées :**
- Couche 1 : `Project.create()` valide non vide/existe/inscriptible
- Couche 2 : `WorkspaceManager` valide que projectDir n'est pas vide
- Couche 3 : `WorktreeManager` refuse git init hors de tmpdir dans les tests
- Couche 4 : journalisation de la stack trace avant git init

**Résultat :** les 1847 tests passés, bug impossible à reproduire

## Constat clé

Les quatre couches étaient nécessaires. Durant les tests, chaque couche a attrapé des bugs que les autres ont manqués :
- Des chemins de code différents contournaient la validation d'entrée
- Des mocks contournaient les vérifications de logique métier
- Des cas limites sur d'autres plateformes exigeaient des gardes d'environnement
- La journalisation de debug a identifié un mauvais usage structurel

**Ne t'arrête pas à un seul point de validation.** Ajoute des vérifications à chaque couche.
