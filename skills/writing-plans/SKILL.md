---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Écrire des Plans

## Vue d'ensemble

Écris des plans d'implémentation complets en supposant que l'ingénieur n'a aucun contexte de notre codebase et un goût douteux : un développeur compétent qui ne connaît presque rien à notre outillage, notre domaine, ni la conception de tests. Documente tout — quels fichiers toucher par tâche, le code, les tests, la doc à consulter, comment tester — en tâches en petites bouchées. DRY. YAGNI. TDD. Commits fréquents.

**Annonce au départ :** "I'm using the writing-plans skill to create the implementation plan."

**Contexte :** Un worktree isolé, si utilisé, aurait dû être créé via le skill `superpowers:using-git-worktrees` à l'exécution.

**Sauvegarde les plans dans :** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` (les préférences de l'utilisateur priment sur ce défaut)

## Vérification de périmètre

Si la spec couvre plusieurs sous-systèmes indépendants, elle aurait dû être découpée en specs de sous-projets pendant le brainstorming. Sinon, suggère de découper en plans séparés — un par sous-système, chacun produisant un logiciel fonctionnel et testable à lui seul.

## Structure des fichiers

Avant de définir les tâches, cartographie quels fichiers seront créés ou modifiés et leur responsabilité — c'est là que les décisions de décomposition se figent.

- Conçois des unités aux frontières claires et interfaces bien définies ; chaque fichier a une seule responsabilité claire.
- Tes éditions sont plus fiables quand les fichiers sont ciblés : préfère les petits fichiers aux gros qui en font trop.
- Les fichiers qui changent ensemble vivent ensemble. Découpe par responsabilité, pas par couche technique.
- Dans les codebases existantes, suis les patterns établis ; ne restructure pas unilatéralement, mais si un fichier que tu modifies est devenu ingérable, inclure un découpage est raisonnable.

Chaque tâche produit des changements autonomes ayant du sens indépendamment.

## Bien dimensionner les tâches

Une tâche est la plus petite unité qui porte son propre cycle de test et mérite le gate d'un relecteur neuf. Replie installation, configuration, squelette et documentation dans la tâche dont le livrable en a besoin ; ne découpe que là où un relecteur pourrait rejeter une tâche tout en approuvant sa voisine. Chaque tâche se termine par un livrable testable indépendamment.

## Granularité en petites bouchées

**Chaque étape est une action (2-5 minutes) :** « écrire le test qui échoue », « l'exécuter pour vérifier qu'il échoue », « implémenter le code minimal », « exécuter les tests et vérifier qu'ils passent », « commiter » — chacune une étape.

## En-tête du document de plan

**Chaque plan DOIT commencer par cet en-tête :**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## Structure d'une tâche

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Pas de placeholders

Chaque étape doit contenir le contenu réel dont un ingénieur a besoin. Ce sont des **échecs de plan** — ne les écris jamais :
- « TBD », « TODO », « implement later », « fill in details »
- « Add appropriate error handling » / « add validation » / « handle edge cases »
- « Write tests for the above » (sans le vrai code de test)
- « Similar to Task N » (répète le code — l'ingénieur peut lire les tâches dans le désordre)
- Des étapes qui décrivent quoi faire sans montrer comment (blocs de code requis pour les étapes de code)
- Des références à des types, fonctions ou méthodes non définis dans aucune tâche

## Auto-revue

Après avoir écrit le plan complet, confronte-le à la spec avec un œil neuf. Checklist que tu exécutes toi-même — pas une délégation à un subagent.

**1. Couverture de la spec :** pour chaque section/besoin, peux-tu pointer une tâche qui l'implémente ? Liste les manques.

**2. Chasse aux placeholders :** cherche les red flags de « Pas de placeholders » ci-dessus. Corrige-les.

**3. Cohérence des types :** les types, signatures et noms utilisés dans les tâches ultérieures correspondent-ils à ce que tu as défini avant ? `clearLayers()` en Task 3 mais `clearFullLayers()` en Task 7 est un bug.

Corrige en ligne, pas besoin de re-relire. Un besoin de la spec sans tâche → ajoute la tâche.

## Passage à l'exécution

Après avoir sauvegardé le plan, propose le choix d'exécution :

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

- **Subagent-Driven :** REQUIRED SUB-SKILL Use superpowers:subagent-driven-development — un subagent neuf par tâche + revue en deux étapes
- **Inline Execution :** REQUIRED SUB-SKILL Use superpowers:executing-plans — exécution par lots avec checkpoints
