---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Exécuter des Plans

## Vue d'ensemble

Charge le plan, relis-le de façon critique, exécute toutes les tâches, rends compte une fois terminé.

**Annonce au départ :** "I'm using the executing-plans skill to implement this plan."

**Note :** Si des subagents sont disponibles (Claude Code, Antigravity), utilise superpowers:subagent-driven-development plutôt que ce skill.

## Le Processus

### Étape 1 : Charger et relire le plan
1. Assure un espace de travail isolé via superpowers:using-git-worktrees (créer ou vérifier l'existant)
2. Lis le fichier de plan
3. Relis-le de façon critique — identifie toute préoccupation
4. Si préoccupation : soulève-la avec ton partenaire humain avant de commencer ; sinon crée les todos et procède

### Étape 2 : Exécuter les tâches

Pour chaque tâche : marque in_progress ; suis chaque étape exactement ; exécute les vérifications spécifiées ; marque completed.

### Étape 3 : Terminer le développement

Toutes les tâches complètes et vérifiées, annonce "I'm using the finishing-a-development-branch skill to complete this work." puis **REQUIRED SUB-SKILL :** Use superpowers:finishing-a-development-branch (vérifier les tests, présenter les options, exécuter le choix).

## Quand s'arrêter et demander de l'aide

**ARRÊTE immédiatement** face à un blocage (dépendance manquante, test qui échoue, instruction peu claire), une lacune critique du plan empêchant de démarrer, une instruction incomprise, ou une vérification qui échoue de façon répétée. **Demande une clarification plutôt que de deviner.**

## Quand revisiter des étapes antérieures

**Reviens à la Revue (Étape 1) quand :** le partenaire met à jour le plan suite à ton retour, ou l'approche fondamentale doit être repensée. **Ne force pas au travers des blocages.**

## À retenir
- Relis le plan de façon critique d'abord ; suis les étapes exactement, ne saute pas les vérifications
- Réfère-toi aux skills quand le plan le dit ; arrête-toi quand tu es bloqué, ne devine pas
- Ne démarre jamais l'implémentation sur main/master sans le consentement explicite de l'utilisateur
