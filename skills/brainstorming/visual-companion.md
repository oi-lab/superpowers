# Guide du compagnon visuel

Compagnon de brainstorming visuel en navigateur, pour montrer des maquettes, des diagrammes et des options.

## Quand l'utiliser

Décide question par question, pas session par session. Le test : **l'utilisateur comprendrait-il mieux en le voyant qu'en le lisant ?**

**Utilise le navigateur** quand le contenu est lui-même visuel :

- **Maquettes d'UI** — wireframes, mises en page, structures de navigation, designs de composants
- **Diagrammes d'architecture** — composants système, flux de données, cartes de relations
- **Comparaisons visuelles côte à côte** — comparer deux mises en page, deux jeux de couleurs, deux directions de design
- **Finition du design** — quand la question porte sur le look and feel, l'espacement, la hiérarchie visuelle
- **Relations spatiales** — machines à états, organigrammes, relations entre entités rendues sous forme de diagrammes

**Utilise le terminal** quand le contenu est textuel ou tabulaire :

- **Questions d'exigences et de périmètre** — « que signifie X ? », « quelles fonctionnalités sont dans le périmètre ? »
- **Choix conceptuels A/B/C** — trancher entre des approches décrites avec des mots
- **Listes d'arbitrages** — pour/contre, tableaux comparatifs
- **Décisions techniques** — design d'API, modélisation de données, choix d'approche architecturale
- **Questions de clarification** — tout ce dont la réponse est des mots, pas une préférence visuelle

Une question *portant sur* un sujet d'UI n'est pas automatiquement une question visuelle. « Quel type d'assistant veux-tu ? » est conceptuel — utilise le terminal. « Laquelle de ces mises en page d'assistant te semble juste ? » est visuel — utilise le navigateur.

## Comment ça marche

Le serveur surveille un répertoire à la recherche de fichiers HTML et sert le plus récent au navigateur. Tu écris du contenu HTML dans `screen_dir`, l'utilisateur le voit dans son navigateur et peut cliquer pour sélectionner des options. Les sélections sont enregistrées dans `state_dir/events`, que tu lis à ton tour suivant.

**Fragments de contenu vs documents complets :** si ton fichier HTML commence par `<!DOCTYPE` ou `<html`, le serveur le sert tel quel (il injecte juste le script d'aide). Sinon, le serveur enrobe automatiquement ton contenu dans le template de cadre — ajoutant l'en-tête, le thème CSS, l'état de connexion et toute l'infrastructure interactive. **Écris des fragments de contenu par défaut.** N'écris des documents complets que lorsque tu as besoin d'un contrôle total sur la page.

## Démarrer une session

```bash
# Démarre APRÈS que l'utilisateur a approuvé le compagnon. --open ouvre automatiquement
# son navigateur sur le premier écran ; --project-dir persiste les maquettes et permet le
# redémarrage sur le même port.
scripts/start-server.sh --project-dir /path/to/project --open

# Renvoie : {"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

Enregistre `screen_dir` et `state_dir` depuis la réponse. Avec `--open`, le navigateur s'ouvre de lui-même quand tu pousses le premier écran — tu n'as pas besoin de demander à l'utilisateur de l'ouvrir, mais partage quand même l'URL en secours (les configurations headless/distantes ne s'ouvrent pas automatiquement).

**L'URL contient une clé de session (`?key=…`).** Le serveur rejette toute requête sans elle, alors donne toujours à l'utilisateur l'URL **complète** du champ `url` — ne retire jamais la query string, et ne distribue jamais un simple `http://host:port`. La clé protège l'accès HTTP et WebSocket, pour qu'un onglet de navigateur égaré ou une autre machine du réseau ne puisse pas lire les écrans ni injecter d'événements. Après le premier chargement, le navigateur mémorise la clé via un cookie, donc les rechargements et les ressources `/files/*` fonctionnent sans la répéter.

**Trouver les infos de connexion :** le serveur écrit son JSON de démarrage dans `$STATE_DIR/server-info`. Si tu as lancé le serveur en arrière-plan sans capturer stdout, lis ce fichier pour obtenir l'URL et le port. Avec `--project-dir`, regarde `<project>/.superpowers/brainstorm/` pour le répertoire de session.

**Note :** passe la racine du projet en `--project-dir` pour que les maquettes persistent dans `.superpowers/brainstorm/` et survivent aux redémarrages du serveur. Sans cela, les fichiers vont dans `/tmp` et sont nettoyés. Rappelle à l'utilisateur d'ajouter `.superpowers/` à `.gitignore` si ce n'est pas déjà fait.

**Lancer le serveur selon la plateforme :**

**Claude Code :**
```bash
# Le mode par défaut fonctionne — le script met lui-même le serveur en arrière-plan.
scripts/start-server.sh --project-dir /path/to/project --open
```

Sous Windows, le script détecte automatiquement et bascule en mode premier plan (ce qui bloque l'appel d'outil). Utilise `run_in_background: true` sur l'appel à l'outil Bash pour que le serveur survive d'un tour de conversation à l'autre, puis lis `$STATE_DIR/server-info` au tour suivant pour obtenir l'URL et le port.

**Autres environnements :** le serveur doit continuer à tourner en arrière-plan d'un tour de conversation à l'autre. Si ton environnement tue les processus détachés, utilise `--foreground` et lance la commande avec le mécanisme d'exécution en arrière-plan de ta plateforme.

Si l'URL est injoignable depuis ton navigateur (fréquent en configuration distante/conteneurisée), lie un hôte non-loopback :

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

Utilise `--url-host` pour contrôler le nom d'hôte imprimé dans le JSON d'URL renvoyé.

## La boucle

1. **Vérifie que le serveur est vivant**, puis **écris du HTML** dans un nouveau fichier de `screen_dir` :
   - **Requis : confirme que le serveur est vivant avant de faire référence à l'URL ou de pousser un écran.** Vérifie que `$STATE_DIR/server-info` existe et que `$STATE_DIR/server-stopped` n'existe pas. S'il s'est arrêté, redémarre-le avec `start-server.sh` en utilisant le **même `--project-dir`** — il réutilise le même port, donc l'onglet ouvert de l'utilisateur se reconnecte de lui-même (il affiche une surcouche « paused » pendant l'arrêt) et tu n'as pas besoin d'envoyer une nouvelle URL. Le serveur s'arrête automatiquement après 4 heures d'inactivité (configurable avec `--idle-timeout-minutes`).
   - Utilise des noms de fichiers sémantiques : `platform.html`, `visual-style.html`, `layout.html`
   - **Ne réutilise jamais un nom de fichier** — chaque écran obtient un fichier neuf
   - Utilise ton outil de création de fichier — **n'utilise jamais cat/heredoc** (ça déverse du bruit dans le terminal)
   - Le serveur sert automatiquement le fichier le plus récent

2. **Dis à l'utilisateur à quoi s'attendre et termine ton tour :**
   - Rappelle-lui l'URL (à chaque étape, pas seulement la première)
   - Donne un bref résumé textuel de ce qui est à l'écran (p. ex. « J'affiche 3 options de mise en page pour la page d'accueil »)
   - Demande-lui de répondre dans le terminal : « Jette un œil et dis-moi ce que tu en penses. Clique pour sélectionner une option si tu veux. »

3. **À ton tour suivant** — après que l'utilisateur a répondu dans le terminal :
   - Lis `$STATE_DIR/events` s'il existe — il contient les interactions navigateur de l'utilisateur (clics, sélections) sous forme de lignes JSON
   - Fusionne avec le texte terminal de l'utilisateur pour avoir le tableau complet
   - Le message terminal est le retour principal ; `state_dir/events` fournit les données d'interaction structurées

4. **Itère ou avance** — si le retour change l'écran courant, écris un nouveau fichier (p. ex. `layout-v2.html`). Ne passe à la question suivante que lorsque l'étape courante est validée.

5. **Décharge en revenant au terminal** — quand l'étape suivante n'a pas besoin du navigateur (p. ex. une question de clarification, une discussion d'arbitrage), pousse un écran d'attente pour effacer le contenu périmé :

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   Cela évite que l'utilisateur reste à fixer un choix déjà résolu alors que la conversation a avancé. Quand la prochaine question visuelle se présente, pousse un nouveau fichier de contenu comme d'habitude.

6. Répète jusqu'à la fin.

## Écrire des fragments de contenu

Écris juste le contenu qui va à l'intérieur de la page. Le serveur l'enrobe automatiquement dans le template de cadre (en-tête, thème CSS, état de connexion et toute l'infrastructure interactive).

**Exemple minimal :**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

C'est tout. Pas de `<html>`, pas de CSS, pas de balises `<script>`. Le serveur fournit tout cela.

## Classes CSS disponibles

Le template de cadre fournit ces classes CSS pour ton contenu :

### Options (choix A/B/C)

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-sélection :** ajoute `data-multiselect` au conteneur pour laisser les utilisateurs sélectionner plusieurs options. Chaque clic bascule le style sélectionné de l'élément.

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### Cards (designs visuels)

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Conteneur de maquette

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Vue partagée (côte à côte)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pour/Contre

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Éléments de maquette (briques de wireframe)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typographie et sections

- `h2` — titre de page
- `h3` — titre de section
- `.subtitle` — texte secondaire sous le titre
- `.section` — bloc de contenu avec marge basse
- `.label` — petit texte de label en majuscules

## Format des événements navigateur

Quand l'utilisateur clique sur des options dans le navigateur, ses interactions sont enregistrées dans `$STATE_DIR/events` (un objet JSON par ligne). Le fichier est vidé automatiquement quand tu pousses un nouvel écran.

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

Le flux d'événements complet montre le chemin d'exploration de l'utilisateur — il peut cliquer plusieurs options avant de se décider. Le dernier événement `choice` est généralement la sélection finale, mais le motif des clics peut révéler une hésitation ou des préférences qui valent la peine d'être creusées.

Si `$STATE_DIR/events` n'existe pas, l'utilisateur n'a pas interagi avec le navigateur — utilise seulement son texte terminal.

## Conseils de design

- **Ajuste la fidélité à la question** — wireframes pour la mise en page, finition pour les questions de finition
- **Explique la question sur chaque page** — « Quelle mise en page paraît plus professionnelle ? » et non juste « Choisis-en une »
- **Itère avant d'avancer** — si le retour change l'écran courant, écris une nouvelle version
- **2 à 4 options max** par écran
- **Utilise du vrai contenu quand ça compte** — pour un portfolio de photographie, utilise de vraies images (Unsplash). Le contenu factice masque les problèmes de design.
- **Garde les maquettes simples** — concentre-toi sur la mise en page et la structure, pas sur un design au pixel près

## Nommage des fichiers

- Utilise des noms sémantiques : `platform.html`, `visual-style.html`, `layout.html`
- Ne réutilise jamais un nom de fichier — chaque écran doit être un nouveau fichier
- Pour les itérations : ajoute un suffixe de version comme `layout-v2.html`, `layout-v3.html`
- Le serveur sert le fichier le plus récent par date de modification

## Nettoyage

```bash
scripts/stop-server.sh $SESSION_DIR
```

Si la session a utilisé `--project-dir`, les fichiers de maquette persistent dans `.superpowers/brainstorm/` pour référence ultérieure. Seules les sessions `/tmp` sont supprimées à l'arrêt.

## Référence

- Template de cadre (référence CSS) : `scripts/frame-template.html`
- Script d'aide (côté client) : `scripts/helper.js`
