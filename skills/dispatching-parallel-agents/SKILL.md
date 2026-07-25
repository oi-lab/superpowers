---
name: dispatching-parallel-agents
description: À utiliser UNIQUEMENT quand ton partenaire humain demande explicitement des agents parallèles, ou pour un lot vraiment important d'échecs indépendants - déployer des sous-agents en éventail duplique le contexte et est gourmand en tokens (opt-in). Pour une poignée de tâches, gère-les toi-même.
---

# Déployer des agents en parallèle

## Vue d'ensemble

Tu délègues des tâches à des agents spécialisés au contexte isolé. En façonnant précisément leurs instructions et leur contexte, tu les gardes concentrés. Ils ne doivent jamais hériter du contexte ou de l'historique de ta session — tu construis exactement ce dont ils ont besoin. Cela préserve aussi ton propre contexte pour la coordination.

Plusieurs échecs sans rapport (fichiers de test, sous-systèmes, bugs différents) s'investiguent en parallèle : chaque investigation est indépendante.

**Principe central :** un agent par domaine de problème indépendant, travaillant simultanément.

## Quand l'utiliser

Décision : plusieurs échecs indépendants → un agent par domaine ; échecs liés → un seul agent investigue tout. Agents sans état partagé → dispatch parallèle ; sinon → séquentiel.

**Utilise quand :**
- 3+ fichiers de test échouent avec des causes racines différentes
- Plusieurs sous-systèmes cassés indépendamment
- Chaque problème se comprend sans le contexte des autres
- Aucun état partagé entre les investigations

**N'utilise pas quand :**
- Les échecs sont liés (corriger l'un peut corriger les autres)
- Besoin de comprendre l'état complet du système
- Les agents interféreraient entre eux

## Le pattern

### 1. Identifier les domaines indépendants

Groupe les échecs selon ce qui est cassé (ex. fichier A : approbation d'outils ; fichier B : complétion par lots ; fichier C : abandon). Chaque domaine est indépendant — corriger l'un n'affecte pas les autres.

### 2. Créer des tâches d'agent ciblées

Chaque agent reçoit :
- **Périmètre précis :** un fichier de test ou un sous-système
- **Objectif clair :** faire passer ces tests
- **Contraintes :** ne pas modifier d'autre code
- **Sortie attendue :** résumé de ce que tu as trouvé et corrigé

### 3. Déployer en parallèle

Émets tous les dispatches dans la même réponse — ils s'exécutent en parallèle :

```text
Subagent (general-purpose): "Fix agent-tool-abort.test.ts failures"
Subagent (general-purpose): "Fix batch-completion-behavior.test.ts failures"
Subagent (general-purpose): "Fix tool-approval-race-conditions.test.ts failures"
# All three run concurrently.
```

Plusieurs dispatches dans une réponse = parallèle. Un par réponse = séquentiel.

### 4. Revoir et intégrer

Quand les agents reviennent :
- Lis chaque résumé
- Vérifie que les corrections n'entrent pas en conflit
- Lance la suite de tests complète
- Intègre tous les changements

## Structure du prompt d'agent

Un bon prompt est : **ciblé** (un seul domaine), **autonome** (tout le contexte nécessaire), **précis sur la sortie** (ce que l'agent doit retourner).

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by:
   - Replacing arbitrary timeouts with event-based waiting
   - Fixing bugs in abort implementation if found
   - Adjusting test expectations if testing changed behavior

Do NOT just increase timeouts - find the real issue.

Return: Summary of what you found and what you fixed.
```

## Erreurs courantes

| ❌ | ✅ |
|----|----|
| Trop large : « Fix all the tests » — l'agent se perd | Précis : « Fix agent-tool-abort.test.ts » |
| Sans contexte : « Fix the race condition » | Avec contexte : colle erreurs et noms de test |
| Sans contraintes : l'agent refactorise tout | Avec contraintes : « Do NOT change production code » |
| Sortie vague : « Fix it » | Précise : « Return summary of root cause and changes » |

## Quand NE PAS l'utiliser

- **Échecs liés :** corriger l'un peut corriger les autres — investigue-les ensemble d'abord
- **Besoin du contexte complet :** comprendre exige de voir tout le système
- **Débogage exploratoire :** tu ne sais pas encore ce qui est cassé
- **État partagé :** les agents interféreraient (mêmes fichiers, mêmes ressources)

## Vérification

Après le retour des agents :
1. **Revoir chaque résumé** — comprends ce qui a changé
2. **Vérifier les conflits** — les agents ont-ils édité le même code ?
3. **Lancer la suite complète** — vérifie que toutes les corrections fonctionnent ensemble
4. **Contrôle par sondage** — les agents peuvent commettre des erreurs systématiques
