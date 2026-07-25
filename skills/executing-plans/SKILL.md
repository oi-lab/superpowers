---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Exécuter des Plans

## Vue d'ensemble

Charge le plan, relis-le de façon critique, exécute toutes les tâches, rends compte une fois terminé.

**Annonce au départ :** "I'm using the executing-plans skill to implement this plan."

**Note :** Superpowers fonctionne bien mieux avec accès aux subagents (Claude Code et Antigravity remplissent tous deux ce critère). Si des subagents sont disponibles, utilise superpowers:subagent-driven-development plutôt que ce skill.

## Le Processus

### Étape 1 : Charger et relire le plan
1. Assure un espace de travail isolé : utilise superpowers:using-git-worktrees pour en créer un ou vérifier celui existant
2. Lis le fichier de plan
3. Relis-le de façon critique — identifie toute question ou préoccupation sur le plan
4. En cas de préoccupation : soulève-la avec ton partenaire humain avant de commencer
5. Sans préoccupation : crée les todos pour les items du plan et procède

### Étape 2 : Exécuter les tâches

Pour chaque tâche :
1. Marque comme in_progress
2. Suis chaque étape exactement (le plan a des étapes en petites bouchées)
3. Exécute les vérifications comme spécifié
4. Marque comme completed

### Étape 3 : Terminer le développement

Après que toutes les tâches sont complètes et vérifiées :
- Annonce : "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL :** Use superpowers:finishing-a-development-branch
- Suis ce skill pour vérifier les tests, présenter les options, exécuter le choix

## Quand s'arrêter et demander de l'aide

**ARRÊTE l'exécution immédiatement quand :**
- Tu heurtes un blocage (dépendance manquante, test qui échoue, instruction peu claire)
- Le plan a des lacunes critiques empêchant de démarrer
- Tu ne comprends pas une instruction
- Une vérification échoue de façon répétée

**Demande une clarification plutôt que de deviner.**

## Quand revisiter des étapes antérieures

**Reviens à la Revue (Étape 1) quand :**
- Le partenaire met à jour le plan suite à ton retour
- L'approche fondamentale doit être repensée

**Ne force pas au travers des blocages** — arrête-toi et demande.

## À retenir
- Relis le plan de façon critique d'abord
- Suis les étapes du plan exactement
- Ne saute pas les vérifications
- Réfère-toi aux skills quand le plan le dit
- Arrête-toi quand tu es bloqué, ne devine pas
- Ne démarre jamais l'implémentation sur la branche main/master sans le consentement explicite de l'utilisateur
