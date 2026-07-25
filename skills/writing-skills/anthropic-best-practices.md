# Bonnes pratiques de rédaction de skills

> Apprends à écrire des skills efficaces que les agents peuvent découvrir et utiliser avec succès.

Les bons skills sont concis, bien structurés et testés en usage réel. Ce guide fournit des décisions pratiques de rédaction pour t'aider à écrire des skills que les agents découvrent et utilisent efficacement.

Pour le contexte conceptuel sur le fonctionnement des skills, voir la [présentation des Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## Principes fondamentaux

### La concision est essentielle

La [fenêtre de contexte](https://platform.claude.com/docs/en/build-with-claude/context-windows) est un bien commun. Ton skill partage la fenêtre de contexte avec tout ce que ton agent doit savoir, notamment :

* Le prompt système
* L'historique de conversation
* Les métadonnées des autres skills
* Ta requête réelle

Tous les tokens de ton skill n'ont pas un coût immédiat. Au démarrage, seules les métadonnées (nom et description) de tous les skills sont préchargées. Les agents lisent SKILL.md uniquement lorsque le skill devient pertinent, et ne lisent les fichiers supplémentaires qu'au besoin. Néanmoins, être concis dans SKILL.md reste important : une fois chargé, chaque token entre en concurrence avec l'historique de conversation et le reste du contexte.

**Hypothèse par défaut** : les agents sont déjà très intelligents.

N'ajoute que le contexte que les agents n'ont pas déjà. Remets en question chaque information :

* « L'agent a-t-il vraiment besoin de cette explication ? »
* « Puis-je supposer que l'agent sait déjà cela ? »
* « Ce paragraphe justifie-t-il son coût en tokens ? »

**Bon exemple : concis** (environ 50 tokens) :

````markdown  theme={null}
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Mauvais exemple : trop verbeux** (environ 150 tokens) :

```markdown  theme={null}
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

La version concise suppose que l'agent sait ce qu'est un PDF et comment fonctionnent les bibliothèques.

### Ajuste le degré de liberté

Adapte le niveau de précision à la fragilité et à la variabilité de la tâche.

**Liberté élevée** (instructions textuelles) :

À utiliser quand :

* Plusieurs approches sont valables
* Les décisions dépendent du contexte
* Des heuristiques guident l'approche

Exemple :

```markdown  theme={null}
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

**Liberté moyenne** (pseudocode ou scripts paramétrés) :

À utiliser quand :

* Un schéma privilégié existe
* Une certaine variation est acceptable
* La configuration influe sur le comportement

Exemple :

````markdown  theme={null}
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**Liberté faible** (scripts précis, peu ou pas de paramètres) :

À utiliser quand :

* Les opérations sont fragiles et sujettes aux erreurs
* La cohérence est critique
* Une séquence précise doit être suivie

Exemple :

````markdown  theme={null}
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

**Analogie** : imagine l'agent comme un robot qui explore un chemin :

* **Pont étroit avec un précipice de chaque côté** : il n'y a qu'une seule voie sûre. Fournis des garde-fous précis et des instructions exactes (liberté faible). Exemple : des migrations de base de données qui doivent s'exécuter dans un ordre exact.
* **Champ ouvert sans danger** : de nombreux chemins mènent au succès. Donne une direction générale et fais confiance à l'agent pour trouver la meilleure route (liberté élevée). Exemple : des revues de code où le contexte détermine la meilleure approche.

### Teste avec tous les modèles prévus

Les skills agissent comme des ajouts aux modèles, donc leur efficacité dépend du modèle sous-jacent. Teste ton skill avec tous les modèles avec lesquels tu comptes l'utiliser.

**Points de test selon le modèle** :

* **Claude Haiku** (rapide, économique) : le skill fournit-il assez d'indications ?
* **Claude Sonnet** (équilibré) : le skill est-il clair et efficace ?
* **Claude Opus** (raisonnement puissant) : le skill évite-t-il de trop expliquer ?

Ce qui fonctionne parfaitement pour Opus peut nécessiter plus de détails pour Haiku. Si tu comptes utiliser ton skill sur plusieurs modèles, vise des instructions qui fonctionnent bien avec tous.

## Structure d'un skill

<Note>
  **Frontmatter YAML** : le frontmatter de SKILL.md exige deux champs :

  * `name` - Nom lisible du skill (64 caractères maximum)
  * `description` - Description en une ligne de ce que fait le skill et quand l'utiliser (1024 caractères maximum)

  Pour tous les détails de structure d'un skill, voir la [présentation des Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure).
</Note>

### Conventions de nommage

Utilise des schémas de nommage cohérents pour faciliter la référence et la discussion. Nous recommandons la **forme en -ing (gérondif)** pour les noms de skills, car elle décrit clairement l'activité ou la capacité fournie.

**Bons exemples de nommage (gérondif)** :

* « Processing PDFs »
* « Analyzing spreadsheets »
* « Managing databases »
* « Testing code »
* « Writing documentation »

**Alternatives acceptables** :

* Groupes nominaux : « PDF Processing », « Spreadsheet Analysis »
* Orientés action : « Process PDFs », « Analyze Spreadsheets »

**À éviter** :

* Noms vagues : « Helper », « Utils », « Tools »
* Trop génériques : « Documents », « Data », « Files »
* Schémas incohérents au sein de ta collection de skills

Un nommage cohérent facilite :

* La référence aux skills dans la documentation et les conversations
* La compréhension immédiate de ce que fait un skill
* L'organisation et la recherche parmi plusieurs skills
* Le maintien d'une bibliothèque de skills professionnelle et cohérente

### Rédiger des descriptions efficaces

Le champ `description` permet la découverte du skill et doit indiquer à la fois ce que fait le skill et quand l'utiliser.

<Warning>
  **Écris toujours à la troisième personne.** La description est injectée dans le prompt système, et un point de vue incohérent peut causer des problèmes de découverte.

  * **Bon :** "Processes Excel files and generates reports"
  * **À éviter :** "I can help you process Excel files"
  * **À éviter :** "You can use this to process Excel files"
</Warning>

**Sois précis et inclus les termes-clés.** Indique à la fois ce que fait le skill et les déclencheurs/contextes précis d'utilisation.

Chaque skill a exactement un champ description. La description est critique pour la sélection du skill : les agents s'en servent pour choisir le bon skill parmi potentiellement plus de 100 skills disponibles. Ta description doit donner assez de détails pour qu'un agent sache quand sélectionner ce skill, tandis que le reste de SKILL.md fournit les détails de mise en œuvre.

Exemples efficaces :

**Skill PDF Processing :**

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Skill Excel Analysis :**

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Skill Git Commit Helper :**

```yaml  theme={null}
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

Évite les descriptions vagues comme celles-ci :

```yaml  theme={null}
description: Helps with documents
```

```yaml  theme={null}
description: Processes data
```

```yaml  theme={null}
description: Does stuff with files
```

### Schémas de divulgation progressive

SKILL.md sert de vue d'ensemble qui oriente les agents vers des ressources détaillées au besoin, comme une table des matières dans un guide d'accueil. Pour une explication du fonctionnement de la divulgation progressive, voir [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) dans la présentation.

**Conseils pratiques :**

* Garde le corps de SKILL.md sous 500 lignes pour des performances optimales
* Répartis le contenu dans des fichiers séparés à l'approche de cette limite
* Utilise les schémas ci-dessous pour organiser efficacement instructions, code et ressources

#### Vue d'ensemble visuelle : du simple au complexe

Un skill de base démarre avec un simple fichier SKILL.md contenant métadonnées et instructions :

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="Simple SKILL.md file showing YAML frontmatter and markdown body" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

À mesure que ton skill grandit, tu peux joindre du contenu supplémentaire que les agents ne chargent qu'au besoin :

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="Bundling additional reference files like reference.md and forms.md." data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

La structure complète du répertoire d'un skill peut ressembler à ceci :

```
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### Schéma 1 : guide de haut niveau avec références

````markdown  theme={null}
---
name: PDF Processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Les agents chargent FORMS.md, REFERENCE.md ou EXAMPLES.md uniquement au besoin.

#### Schéma 2 : organisation par domaine

Pour les skills couvrant plusieurs domaines, organise le contenu par domaine pour éviter de charger du contexte non pertinent. Quand un utilisateur pose une question sur les métriques de vente, l'agent n'a besoin que des schémas liés aux ventes, pas des données finance ou marketing. Cela maintient une faible consommation de tokens et un contexte ciblé.

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md theme={null}
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### Schéma 3 : détails conditionnels

Montre le contenu de base, lie vers le contenu avancé :

```markdown  theme={null}
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Les agents lisent REDLINING.md ou OOXML.md uniquement quand l'utilisateur a besoin de ces fonctionnalités.

### Évite les références profondément imbriquées

Les agents peuvent lire les fichiers partiellement lorsqu'ils sont référencés depuis d'autres fichiers référencés. Face à des références imbriquées, un agent peut utiliser des commandes comme `head -100` pour prévisualiser plutôt que de lire les fichiers en entier, ce qui donne des informations incomplètes.

**Garde les références à un seul niveau de profondeur depuis SKILL.md.** Tous les fichiers de référence doivent être liés directement depuis SKILL.md pour garantir que les agents lisent les fichiers complets au besoin.

**Mauvais exemple : trop profond** :

```markdown  theme={null}
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Bon exemple : un seul niveau de profondeur** :

```markdown  theme={null}
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### Structure les longs fichiers de référence avec une table des matières

Pour les fichiers de référence de plus de 100 lignes, place une table des matières en haut. Ainsi, les agents voient toute l'étendue des informations disponibles même en prévisualisant par lectures partielles.

**Exemple** :

```markdown  theme={null}
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

Les agents peuvent alors lire le fichier complet ou aller directement à une section précise.

Pour savoir comment cette architecture basée sur le système de fichiers permet la divulgation progressive, voir la section [Runtime environment](#runtime-environment) dans la partie Avancé ci-dessous.

## Workflows et boucles de rétroaction

### Utilise des workflows pour les tâches complexes

Découpe les opérations complexes en étapes claires et séquentielles. Pour les workflows particulièrement complexes, fournis une checklist que l'agent peut copier dans sa réponse et cocher au fur et à mesure.

**Exemple 1 : workflow de synthèse de recherche** (pour les skills sans code) :

````markdown  theme={null}
## Research synthesis workflow

Copy this checklist and track your progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in the `sources/` directory. Note the main arguments and supporting evidence.

**Step 2: Identify key themes**

Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?

**Step 3: Cross-reference claims**

For each major claim, verify it appears in the source material. Note which source supports each point.

**Step 4: Create structured summary**

Organize findings by theme. Include:
- Main claim
- Supporting evidence from sources
- Conflicting viewpoints (if any)

**Step 5: Verify citations**

Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
````

Cet exemple montre comment les workflows s'appliquent à des tâches d'analyse ne nécessitant pas de code. Le schéma de checklist fonctionne pour tout processus complexe à plusieurs étapes.

**Exemple 2 : workflow de remplissage de formulaire PDF** (pour les skills avec code) :

````markdown  theme={null}
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
````

Des étapes claires empêchent les agents de sauter des validations critiques. La checklist t'aide, toi et l'agent, à suivre la progression dans les workflows à plusieurs étapes.

### Mets en place des boucles de rétroaction

**Schéma courant** : exécuter le validateur → corriger les erreurs → répéter

Ce schéma améliore grandement la qualité des résultats.

**Exemple 1 : conformité à un guide de style** (pour les skills sans code) :

```markdown  theme={null}
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
```

Cela illustre le schéma de boucle de validation en utilisant des documents de référence au lieu de scripts. Le « validateur » est STYLE\_GUIDE.md, et l'agent effectue la vérification en lisant et comparant.

**Exemple 2 : processus d'édition de document** (pour les skills avec code) :

```markdown  theme={null}
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

La boucle de validation détecte les erreurs tôt.

## Consignes de contenu

### Évite les informations sensibles au temps

N'inclus pas d'informations qui deviendront obsolètes :

**Mauvais exemple : sensible au temps** (deviendra faux) :

```markdown  theme={null}
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Bon exemple** (utilise une section « old patterns ») :

```markdown  theme={null}
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

La section « old patterns » fournit un contexte historique sans encombrer le contenu principal.

### Utilise une terminologie cohérente

Choisis un terme et utilise-le tout au long du skill :

**Bon — cohérent** :

* Toujours « API endpoint »
* Toujours « field »
* Toujours « extract »

**Mauvais — incohérent** :

* Mélange « API endpoint », « URL », « API route », « path »
* Mélange « field », « box », « element », « control »
* Mélange « extract », « pull », « get », « retrieve »

La cohérence aide les agents à comprendre et suivre les instructions.

## Schémas courants

### Schéma de gabarit (template)

Fournis des gabarits pour le format de sortie. Adapte le niveau de rigueur à tes besoins.

**Pour des exigences strictes** (comme des réponses d'API ou des formats de données) :

````markdown  theme={null}
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**Pour un guidage souple** (quand l'adaptation est utile) :

````markdown  theme={null}
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
````

### Schéma d'exemples

Pour les skills dont la qualité de sortie dépend de la présence d'exemples, fournis des paires entrée/sortie, exactement comme dans un prompting classique :

````markdown  theme={null}
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
````

Les exemples aident les agents à saisir le style et le niveau de détail souhaités plus clairement que des descriptions seules.

### Schéma de workflow conditionnel

Guide les agents à travers les points de décision :

```markdown  theme={null}
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

<Tip>
  Si les workflows deviennent volumineux ou compliqués avec de nombreuses étapes, envisage de les déplacer dans des fichiers séparés et indique à l'agent de lire le fichier approprié selon la tâche.
</Tip>

## Évaluation et itération

### Construis d'abord les évaluations

**Crée les évaluations AVANT de rédiger une documentation extensive.** Cela garantit que ton skill résout de vrais problèmes plutôt que d'en documenter d'imaginaires.

**Développement piloté par l'évaluation :**

1. **Identifier les lacunes** : lance ton agent sur des tâches représentatives sans skill. Documente les échecs précis ou le contexte manquant
2. **Créer les évaluations** : construis trois scénarios testant ces lacunes
3. **Établir une référence** : mesure la performance de l'agent sans le skill
4. **Écrire des instructions minimales** : crée juste assez de contenu pour combler les lacunes et passer les évaluations
5. **Itérer** : exécute les évaluations, compare à la référence et affine

Cette approche garantit que tu résous de vrais problèmes plutôt que d'anticiper des besoins qui ne se concrétiseront peut-être jamais.

**Structure d'une évaluation** :

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  Cet exemple montre une évaluation pilotée par les données avec une grille de test simple. Nous ne fournissons pas actuellement de moyen intégré d'exécuter ces évaluations. Les utilisateurs peuvent créer leur propre système d'évaluation. Les évaluations sont ta source de vérité pour mesurer l'efficacité d'un skill.
</Note>

### Développe les skills de façon itérative avec l'agent

Le processus de développement de skills le plus efficace fait intervenir l'agent lui-même. Travaille avec une instance (« Agent A ») pour créer un skill qui sera utilisé par d'autres instances (« Agent B »). L'Agent A t'aide à concevoir et affiner les instructions, tandis que l'Agent B les teste dans des tâches réelles. Cela fonctionne car les modèles sous-jacents comprennent à la fois comment écrire des instructions d'agent efficaces et de quelles informations les agents ont besoin.

**Créer un nouveau skill :**

1. **Réaliser une tâche sans skill** : résous un problème avec l'Agent A par prompting classique. En travaillant, tu fournis naturellement du contexte, expliques des préférences et partages des connaissances procédurales. Remarque quelles informations tu fournis de façon répétée.

2. **Identifier le schéma réutilisable** : après la tâche, identifie le contexte que tu as fourni et qui serait utile pour des tâches similaires à l'avenir.

   **Exemple** : si tu as mené une analyse BigQuery, tu as peut-être fourni des noms de tables, des définitions de champs, des règles de filtrage (comme « toujours exclure les comptes de test ») et des schémas de requêtes courants.

3. **Demander à l'Agent A de créer un skill** : « Crée un skill qui capture ce schéma d'analyse BigQuery qu'on vient d'utiliser. Inclus les schémas de tables, les conventions de nommage et la règle sur le filtrage des comptes de test. »

   <Tip>
     Les agents modernes comprennent nativement le format et la structure des skills. Tu n'as pas besoin de prompts système spéciaux ni d'un skill « writing skills » pour obtenir de l'aide à la création de skills. Demande simplement à l'agent de créer un skill et il générera un contenu SKILL.md correctement structuré, avec un frontmatter et un corps appropriés.
   </Tip>

4. **Revoir la concision** : vérifie que l'Agent A n'a pas ajouté d'explications inutiles. Demande : « Retire l'explication de ce qu'est le win rate — l'agent le sait déjà. »

5. **Améliorer l'architecture de l'information** : demande à l'Agent A d'organiser le contenu plus efficacement. Par exemple : « Organise ça pour que le schéma de table soit dans un fichier de référence séparé. On ajoutera peut-être d'autres tables plus tard. »

6. **Tester sur des tâches similaires** : utilise le skill avec l'Agent B (une nouvelle instance avec le skill chargé) sur des cas d'usage proches. Observe si l'Agent B trouve la bonne information, applique correctement les règles et mène la tâche à bien.

7. **Itérer d'après l'observation** : si l'Agent B galère ou oublie quelque chose, reviens vers l'Agent A avec des détails : « Quand l'agent a utilisé ce skill, il a oublié de filtrer par date pour le Q4. Faut-il ajouter une section sur les schémas de filtrage par date ? »

**Itérer sur des skills existants :**

Le même schéma hiérarchique se poursuit lors de l'amélioration des skills. Tu alternes entre :

* **Travailler avec l'Agent A** (l'expert qui t'aide à affiner le skill)
* **Tester avec l'Agent B** (l'agent qui utilise le skill pour du travail réel)
* **Observer le comportement de l'Agent B** et rapporter les enseignements à l'Agent A

1. **Utiliser le skill dans des workflows réels** : donne à l'Agent B (avec le skill chargé) de vraies tâches, pas des scénarios de test

2. **Observer le comportement de l'Agent B** : note où il galère, réussit ou fait des choix inattendus

   **Exemple d'observation** : « Quand j'ai demandé à l'Agent B un rapport de ventes régional, il a écrit la requête mais a oublié d'exclure les comptes de test, alors que le skill mentionne cette règle. »

3. **Revenir vers l'Agent A pour des améliorations** : partage le SKILL.md actuel et décris ce que tu as observé. Demande : « J'ai remarqué que l'Agent B a oublié de filtrer les comptes de test quand j'ai demandé un rapport régional. Le skill mentionne le filtrage, mais peut-être qu'il n'est pas assez mis en avant ? »

4. **Revoir les suggestions de l'Agent A** : l'Agent A pourrait suggérer de réorganiser pour rendre les règles plus visibles, d'utiliser un langage plus fort comme « MUST filter » au lieu de « always filter », ou de restructurer la section workflow.

5. **Appliquer et tester les changements** : mets à jour le skill avec les affinements de l'Agent A, puis re-teste avec l'Agent B sur des demandes similaires

6. **Répéter selon l'usage** : poursuis ce cycle observer-affiner-tester à mesure que tu rencontres de nouveaux scénarios. Chaque itération améliore le skill d'après le comportement réel de l'agent, pas des hypothèses.

**Recueillir les retours de l'équipe :**

1. Partage les skills avec tes coéquipiers et observe leur usage
2. Demande : le skill s'active-t-il quand attendu ? Les instructions sont-elles claires ? Que manque-t-il ?
3. Intègre les retours pour corriger les angles morts de tes propres schémas d'usage

**Pourquoi cette approche fonctionne** : l'Agent A comprend les besoins des agents, tu apportes l'expertise métier, l'Agent B révèle les lacunes par l'usage réel, et l'affinement itératif améliore les skills d'après le comportement observé plutôt que des hypothèses.

### Observe comment les agents naviguent dans les skills

En itérant sur les skills, prête attention à la façon dont les agents les utilisent réellement en pratique. Guette :

* **Des chemins d'exploration inattendus** : l'agent lit-il les fichiers dans un ordre que tu n'avais pas prévu ? Cela peut indiquer que ta structure n'est pas aussi intuitive que tu le pensais
* **Des connexions ratées** : l'agent oublie-t-il de suivre les références vers des fichiers importants ? Tes liens doivent peut-être être plus explicites ou visibles
* **Une sur-dépendance à certaines sections** : si l'agent lit sans cesse le même fichier, demande-toi si ce contenu ne devrait pas être dans le SKILL.md principal
* **Du contenu ignoré** : si l'agent n'accède jamais à un fichier joint, il est peut-être inutile ou mal signalé dans les instructions principales

Itère d'après ces observations plutôt que d'après des hypothèses. Le `name` et la `description` des métadonnées de ton skill sont particulièrement critiques. Les agents s'en servent pour décider de déclencher ou non le skill face à la tâche courante. Assure-toi qu'ils décrivent clairement ce que fait le skill et quand l'utiliser.

## Anti-schémas à éviter

### Évite les chemins à la Windows

Utilise toujours des barres obliques dans les chemins de fichiers, même sous Windows :

* ✓ **Bon** : `scripts/helper.py`, `reference/guide.md`
* ✗ **À éviter** : `scripts\helper.py`, `reference\guide.md`

Les chemins de type Unix fonctionnent sur toutes les plateformes, tandis que les chemins de type Windows provoquent des erreurs sur les systèmes Unix.

### Évite de proposer trop d'options

Ne présente pas plusieurs approches sauf si nécessaire :

````markdown  theme={null}
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

## Avancé : skills avec code exécutable

Les sections ci-dessous concernent les skills incluant des scripts exécutables. Si ton skill n'utilise que des instructions markdown, passe directement à la [Checklist des skills efficaces](#checklist-for-effective-skills).

### Résous, ne renvoie pas la balle

Quand tu écris des scripts pour des skills, gère les conditions d'erreur plutôt que de renvoyer la balle à l'agent.

**Bon exemple : gérer les erreurs explicitement** :

```python  theme={null}
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```

**Mauvais exemple : renvoyer la balle à l'agent** :

```python  theme={null}
def process_file(path):
    # Just fail and let the agent figure it out
    return open(path).read()
```

Les paramètres de configuration doivent aussi être justifiés et documentés pour éviter les « constantes vaudou » (loi d'Ousterhout). Si tu ne connais pas la bonne valeur, comment l'agent la déterminera-t-il ?

**Bon exemple : auto-documenté** :

```python  theme={null}
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**Mauvais exemple : nombres magiques** :

```python  theme={null}
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### Fournis des scripts utilitaires

Même si ton agent pouvait écrire un script, des scripts pré-écrits offrent des avantages :

**Avantages des scripts utilitaires** :

* Plus fiables que du code généré
* Économisent des tokens (pas besoin d'inclure le code dans le contexte)
* Gagnent du temps (pas de génération de code)
* Assurent la cohérence entre les usages

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="Bundling executable scripts alongside instruction files" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

Le schéma ci-dessus montre comment les scripts exécutables fonctionnent aux côtés des fichiers d'instructions. Le fichier d'instructions (forms.md) référence le script, et l'agent peut l'exécuter sans en charger le contenu dans le contexte.

**Distinction importante** : indique clairement dans tes instructions si l'agent doit :

* **Exécuter le script** (le plus courant) : « Run `analyze_form.py` to extract fields »
* **Le lire comme référence** (pour une logique complexe) : « See `analyze_form.py` for the field extraction algorithm »

Pour la plupart des scripts utilitaires, l'exécution est préférable car plus fiable et efficace. Voir la section [Runtime environment](#runtime-environment) ci-dessous pour les détails sur l'exécution des scripts.

**Exemple** :

````markdown  theme={null}
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### Utilise l'analyse visuelle

Quand les entrées peuvent être rendues sous forme d'images, fais-les analyser par l'agent :

````markdown  theme={null}
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. The agent can see field locations and types visually
````

<Note>
  Dans cet exemple, tu devrais écrire le script `pdf_to_images.py`.
</Note>

Les capacités de vision de l'agent aident à comprendre les mises en page et les structures.

### Crée des sorties intermédiaires vérifiables

Quand les agents accomplissent des tâches complexes et ouvertes, ils peuvent commettre des erreurs. Le schéma « planifier-valider-exécuter » détecte les erreurs tôt : l'agent crée d'abord un plan dans un format structuré, puis valide ce plan avec un script avant de l'exécuter.

**Exemple** : imagine demander à l'agent de mettre à jour 50 champs de formulaire dans un PDF à partir d'un tableur. Sans validation, il pourrait référencer des champs inexistants, créer des valeurs contradictoires, oublier des champs requis ou appliquer les mises à jour de travers.

**Solution** : utilise le schéma de workflow montré plus haut (remplissage de formulaire PDF), mais ajoute un fichier intermédiaire `changes.json` qui est validé avant d'appliquer les changements. Le workflow devient : analyser → **créer le fichier de plan** → **valider le plan** → exécuter → vérifier.

**Pourquoi ce schéma fonctionne :**

* **Détecte les erreurs tôt** : la validation trouve les problèmes avant d'appliquer les changements
* **Vérifiable par machine** : les scripts fournissent une vérification objective
* **Planification réversible** : l'agent peut itérer sur le plan sans toucher aux originaux
* **Débogage clair** : les messages d'erreur pointent vers des problèmes précis

**Quand l'utiliser** : opérations par lots, changements destructifs, règles de validation complexes, opérations à fort enjeu.

**Astuce de mise en œuvre** : rends les scripts de validation verbeux avec des messages d'erreur précis comme « Field 'signature\_date' not found. Available fields: customer\_name, order\_total, signature\_date\_signed » pour aider l'agent à corriger les problèmes.

### Dépendances de paquets

Les skills s'exécutent dans l'environnement d'exécution de code avec des limitations propres à chaque plateforme :

* **claude.ai** : peut installer des paquets depuis npm et PyPI et récupérer depuis des dépôts GitHub
* **API Anthropic** : n'a aucun accès réseau ni installation de paquets à l'exécution

Liste les paquets requis dans ton SKILL.md et vérifie leur disponibilité dans la [documentation de l'outil d'exécution de code](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).

### Environnement d'exécution

Les skills s'exécutent dans un environnement d'exécution de code avec accès au système de fichiers, commandes bash et exécution de code. Pour l'explication conceptuelle de cette architecture, voir [The Skills architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#the-skills-architecture) dans la présentation.

**Comment cela influe sur ta rédaction :**

**Comment les agents accèdent aux skills :**

1. **Métadonnées préchargées** : au démarrage, le nom et la description du frontmatter YAML de tous les skills sont chargés dans le prompt système
2. **Fichiers lus à la demande** : les agents utilisent leurs outils de lecture pour accéder à SKILL.md et aux autres fichiers du système de fichiers au besoin
3. **Scripts exécutés efficacement** : les scripts utilitaires peuvent être exécutés via bash sans charger leur contenu complet dans le contexte. Seule la sortie du script consomme des tokens
4. **Pas de pénalité de contexte pour les gros fichiers** : les fichiers de référence, données ou documentation ne consomment pas de tokens de contexte tant qu'ils ne sont pas lus

* **Les chemins de fichiers comptent** : les agents naviguent dans ton répertoire de skill comme un système de fichiers. Utilise des barres obliques (`reference/guide.md`), pas des antislashs
* **Nomme les fichiers de façon descriptive** : utilise des noms qui indiquent le contenu : `form_validation_rules.md`, pas `doc2.md`
* **Organise pour la découverte** : structure les répertoires par domaine ou fonctionnalité
  * Bon : `reference/finance.md`, `reference/sales.md`
  * Mauvais : `docs/file1.md`, `docs/file2.md`
* **Joins des ressources complètes** : inclus des docs d'API complètes, des exemples extensifs, de gros jeux de données ; aucune pénalité de contexte tant qu'ils ne sont pas consultés
* **Préfère les scripts pour les opérations déterministes** : écris `validate_form.py` plutôt que de demander à l'agent de générer le code de validation
* **Rends l'intention d'exécution claire** :
  * « Run `analyze_form.py` to extract fields » (exécuter)
  * « See `analyze_form.py` for the extraction algorithm » (lire comme référence)
* **Teste les schémas d'accès aux fichiers** : vérifie que l'agent peut naviguer dans ta structure de répertoires en testant avec de vraies requêtes

**Exemple :**

```
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

Quand l'utilisateur pose une question sur le chiffre d'affaires, l'agent lit SKILL.md, voit la référence à `reference/finance.md` et invoque bash pour lire uniquement ce fichier. Les fichiers sales.md et product.md restent sur le système de fichiers, consommant zéro token de contexte tant qu'ils ne sont pas nécessaires. Ce modèle basé sur le système de fichiers est ce qui permet la divulgation progressive : les agents peuvent naviguer et charger sélectivement exactement ce que chaque tâche requiert.

Pour tous les détails sur l'architecture technique, voir [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) dans la présentation des Skills.

### Références aux outils MCP

Si ton skill utilise des outils MCP (Model Context Protocol), utilise toujours des noms d'outils pleinement qualifiés pour éviter les erreurs « tool not found ».

**Format** : `ServerName:tool_name`

**Exemple** :

```markdown  theme={null}
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

Où :

* `BigQuery` et `GitHub` sont les noms des serveurs MCP
* `bigquery_schema` et `create_issue` sont les noms des outils au sein de ces serveurs

Sans le préfixe du serveur, les agents peuvent ne pas localiser l'outil, surtout quand plusieurs serveurs MCP sont disponibles.

### Ne suppose pas que les outils sont installés

Ne suppose pas que les paquets sont disponibles :

````markdown  theme={null}
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## Notes techniques

### Exigences du frontmatter YAML

Le frontmatter de SKILL.md exige les champs `name` (64 caractères max) et `description` (1024 caractères max). Voir la [présentation des Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure) pour tous les détails de structure.

### Budgets de tokens

Garde le corps de SKILL.md sous 500 lignes pour des performances optimales. Si ton contenu dépasse cette limite, découpe-le en fichiers séparés à l'aide des schémas de divulgation progressive décrits plus haut. Pour les détails d'architecture, voir la [présentation des Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work).

## Checklist des skills efficaces

Avant de partager un skill, vérifie :

### Qualité de base

* [ ] La description est précise et inclut les termes-clés
* [ ] La description indique à la fois ce que fait le skill et quand l'utiliser
* [ ] Le corps de SKILL.md fait moins de 500 lignes
* [ ] Les détails supplémentaires sont dans des fichiers séparés (si besoin)
* [ ] Aucune information sensible au temps (ou placée en section « old patterns »)
* [ ] Terminologie cohérente partout
* [ ] Les exemples sont concrets, pas abstraits
* [ ] Les références de fichiers sont à un seul niveau de profondeur
* [ ] La divulgation progressive est utilisée à bon escient
* [ ] Les workflows ont des étapes claires

### Code et scripts

* [ ] Les scripts résolvent les problèmes au lieu de renvoyer la balle à l'agent
* [ ] La gestion des erreurs est explicite et utile
* [ ] Aucune « constante vaudou » (toutes les valeurs sont justifiées)
* [ ] Paquets requis listés dans les instructions et vérifiés comme disponibles
* [ ] Les scripts ont une documentation claire
* [ ] Aucun chemin à la Windows (uniquement des barres obliques)
* [ ] Étapes de validation/vérification pour les opérations critiques
* [ ] Boucles de rétroaction incluses pour les tâches critiques en qualité

### Tests

* [ ] Au moins trois évaluations créées
* [ ] Testé avec Haiku, Sonnet et Opus
* [ ] Testé avec des scénarios d'usage réels
* [ ] Retours de l'équipe intégrés (le cas échéant)

## Prochaines étapes

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    Crée ton premier skill
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    Crée et gère des skills dans Claude Code
  </Card>

  <Card title="Use Skills with the API" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    Charge et utilise des skills par programmation
  </Card>
</CardGroup>
