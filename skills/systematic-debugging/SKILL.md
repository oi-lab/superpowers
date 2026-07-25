---
name: systematic-debugging
description: À utiliser face à tout bug, échec de test ou comportement inattendu, avant de proposer des correctifs
---

# Débogage systématique

## Vue d'ensemble

**Principe fondamental :** TOUJOURS trouver la cause racine avant de tenter un correctif. Corriger un symptôme est un échec.

**Violer la lettre de ce processus, c'est violer l'esprit du débogage.**

## La loi d'airain

```
AUCUN CORRECTIF SANS AVOIR D'ABORD ENQUÊTÉ SUR LA CAUSE RACINE
```

Tant que la Phase 1 n'est pas terminée, tu ne peux pas proposer de correctif.

## Quand l'utiliser

Pour TOUT problème technique : échecs de test, bugs en production, comportement inattendu, problèmes de performance, échecs de build, problèmes d'intégration.

**Surtout quand :**
- Tu es sous pression temporelle (l'urgence rend le devinage tentant)
- « Juste un petit correctif rapide » semble évident
- Tu as déjà tenté plusieurs correctifs
- Le correctif précédent n'a pas marché
- Tu ne comprends pas entièrement le problème

**Ne saute pas le processus quand :**
- Le problème semble simple (les bugs simples ont aussi une cause racine)
- Tu es pressé (précipiter garantit le retravail)
- Le manager veut que ce soit corrigé MAINTENANT (la méthode systématique est plus rapide que le tâtonnement)

## Les quatre phases

Tu DOIS terminer chaque phase avant de passer à la suivante.

### Phase 1 : Enquête sur la cause racine

**AVANT de tenter TOUT correctif :**

1. **Lis attentivement les messages d'erreur**
   - Ne saute pas les erreurs ou avertissements
   - Ils contiennent souvent la solution exacte
   - Lis les stack traces en entier
   - Note les numéros de ligne, chemins de fichier, codes d'erreur

2. **Reproduis de façon fiable**
   - Peux-tu le déclencher de manière fiable ? Quelles sont les étapes exactes ? Cela arrive-t-il à chaque fois ?
   - Si non reproductible → collecte plus de données, ne devine pas

3. **Vérifie les changements récents**
   - Qu'est-ce qui a changé et pourrait causer ça ? (git diff, commits récents, nouvelles dépendances, changements de config, différences d'environnement)

4. **Collecte des preuves dans les systèmes multi-composants**

   **QUAND le système a plusieurs composants (CI → build → signature, API → service → base de données) :**

   **AVANT de proposer un correctif, ajoute de l'instrumentation de diagnostic.** Pour CHAQUE frontière entre composants : logue les données qui entrent, celles qui sortent, vérifie la propagation de l'environnement/config, contrôle l'état à chaque couche. Lance une fois pour obtenir des preuves montrant OÙ ça casse, puis identifie le composant fautif et enquête dessus spécifiquement.

   **Exemple (système multi-couches) :**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **Cela révèle** quelle couche échoue (secrets → workflow ✓, workflow → build ✗).

5. **Trace le flux de données**

   **QUAND l'erreur est profonde dans la pile d'appels :**

   Voir `root-cause-tracing.md` dans ce répertoire pour la technique complète de traçage à rebours.

   **Version rapide :** Où naît la mauvaise valeur ? Qui a appelé ça avec la mauvaise valeur ? Continue de remonter jusqu'à la source. Corrige à la source, pas au symptôme.

### Phase 2 : Analyse des motifs

**Trouve le motif avant de corriger :**

1. **Trouve des exemples qui fonctionnent**
   - Repère du code similaire qui marche dans la même base de code
   - Qu'est-ce qui fonctionne et ressemble à ce qui est cassé ?

2. **Compare aux références**
   - Si tu implémentes un motif, lis l'implémentation de référence EN ENTIER
   - Ne survole pas — lis chaque ligne
   - Comprends le motif à fond avant de l'appliquer

3. **Identifie les différences**
   - Qu'est-ce qui diffère entre ce qui marche et ce qui est cassé ?
   - Liste chaque différence, aussi minime soit-elle
   - Ne suppose pas « ça ne peut pas compter »

4. **Comprends les dépendances**
   - De quels autres composants cela a-t-il besoin ? Quels réglages, config, environnement ? Quelles hypothèses fait-il ?

### Phase 3 : Hypothèse et test

**Méthode scientifique :**

1. **Formule une seule hypothèse**
   - Énonce clairement : « Je pense que X est la cause racine parce que Y »
   - Écris-la. Sois précis, pas vague.

2. **Teste au minimum**
   - Fais le PLUS PETIT changement possible pour tester l'hypothèse
   - Une variable à la fois. Ne corrige pas plusieurs choses en même temps.

3. **Vérifie avant de continuer**
   - Ça a marché ? Oui → Phase 4
   - Ça n'a pas marché ? Formule une NOUVELLE hypothèse
   - N'EMPILE PAS d'autres correctifs par-dessus

4. **Quand tu ne sais pas**
   - Dis « Je ne comprends pas X ». Ne prétends pas savoir. Demande de l'aide. Cherche davantage.

### Phase 4 : Implémentation

**Corrige la cause racine, pas le symptôme :**

1. **Crée un cas de test qui échoue**
   - Reproduction la plus simple possible, test automatisé si possible, script de test ponctuel si aucun framework
   - OBLIGATOIRE avant de corriger
   - Utilise le skill `superpowers:test-driven-development` pour écrire de vrais tests qui échouent

2. **Implémente un seul correctif**
   - Traite la cause racine identifiée. UN changement à la fois.
   - Pas d'améliorations « tant que j'y suis ». Pas de refactoring groupé.

3. **Vérifie le correctif**
   - Le test passe-t-il maintenant ? Aucun autre test cassé ? Le problème est-il réellement résolu ?
   - Utilise le skill `superpowers:verification-before-completion` avant de crier victoire

4. **Si le correctif ne marche pas**
   - STOP
   - Compte : combien de correctifs as-tu tentés ?
   - Si < 3 : retourne en Phase 1, réanalyse avec les nouvelles informations
   - **Si ≥ 3 : STOP et remets l'architecture en question (étape 5 ci-dessous)**
   - NE tente PAS un correctif nº 4 sans discussion architecturale

5. **Si 3 correctifs ou plus ont échoué : remets l'architecture en question**

   **Motif indiquant un problème d'architecture :**
   - Chaque correctif révèle un nouvel état partagé / couplage / problème à un endroit différent
   - Les correctifs exigent un « refactoring massif »
   - Chaque correctif crée de nouveaux symptômes ailleurs

   **STOP et remets en cause les fondamentaux :**
   - Ce motif est-il fondamentalement sain ? Persiste-t-on « par pure inertie » ? Faut-il refactorer l'architecture plutôt que continuer à corriger des symptômes ?

   **Discutes-en avec ton partenaire humain avant de tenter d'autres correctifs.**

   Ce n'est PAS une hypothèse ratée — c'est une mauvaise architecture.

## Signaux d'alarme — STOP et suis le processus

Si tu te surprends à penser :
- « Correctif rapide pour l'instant, j'enquêterai plus tard »
- « Change juste X et vois si ça marche »
- « Ajoute plusieurs changements, lance les tests »
- « Saute le test, je vérifierai manuellement »
- « C'est probablement X, corrigeons ça »
- « Je ne comprends pas tout mais ça pourrait marcher »
- « Le motif dit X mais je vais l'adapter différemment »
- « Voici les principaux problèmes : [liste des correctifs sans enquête] »
- Proposer des solutions avant de tracer le flux de données
- **« Une dernière tentative de correctif » (alors que déjà 2+ tentées)**
- **Chaque correctif révèle un nouveau problème à un endroit différent**

**TOUT cela signifie : STOP. Retourne en Phase 1.**

**Si 3 correctifs ou plus ont échoué :** remets l'architecture en question (voir Phase 4.5).

## Signaux de ton partenaire humain que tu t'y prends mal

**Guette ces redirections :**
- « Ça n'arrive pas ? » — Tu as supposé sans vérifier
- « Est-ce que ça va nous montrer… ? » — Tu aurais dû ajouter de la collecte de preuves
- « Arrête de deviner » — Tu proposes des correctifs sans comprendre
- « Réfléchis à fond à ça » — Remets en cause les fondamentaux, pas seulement les symptômes
- « On est bloqués ? » (frustré) — Ton approche ne marche pas

**Quand tu vois ça :** STOP. Retourne en Phase 1.

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Le problème est simple, pas besoin de processus » | Les problèmes simples ont aussi une cause racine. Le processus est rapide pour eux. |
| « Urgence, pas le temps pour un processus » | Le débogage systématique est PLUS RAPIDE que le tâtonnement essai-erreur. |
| « Essaie juste ça d'abord, tu enquêteras ensuite » | Le premier correctif donne le ton. Fais-le bien dès le départ. |
| « J'écrirai le test après avoir confirmé que le correctif marche » | Les correctifs non testés ne tiennent pas. Le test d'abord le prouve. |
| « Plusieurs correctifs à la fois font gagner du temps » | Impossible d'isoler ce qui a marché. Ça crée de nouveaux bugs. |
| « La référence est trop longue, je vais adapter le motif » | Une compréhension partielle garantit des bugs. Lis-la en entier. |
| « Je vois le problème, laisse-moi le corriger » | Voir les symptômes ≠ comprendre la cause racine. |
| « Une tentative de plus » (après 2+ échecs) | 3+ échecs = problème d'architecture. Remets le motif en cause, ne recorrige pas. |

## Référence rapide

| Phase | Activités clés | Critère de réussite |
|-------|---------------|------------------|
| **1. Cause racine** | Lire erreurs, reproduire, vérifier changements, collecter preuves | Comprendre QUOI et POURQUOI |
| **2. Motif** | Trouver exemples fonctionnels, comparer | Identifier les différences |
| **3. Hypothèse** | Formuler une théorie, tester au minimum | Confirmée ou nouvelle hypothèse |
| **4. Implémentation** | Créer test, corriger, vérifier | Bug résolu, tests passent |

## Quand le processus révèle « pas de cause racine »

Si l'enquête systématique révèle que le problème est réellement environnemental, dépendant du timing, ou externe :

1. Tu as terminé le processus
2. Documente ce que tu as investigué
3. Implémente une gestion appropriée (retry, timeout, message d'erreur)
4. Ajoute du monitoring/logging pour investigation future

**Mais :** 95 % des cas « pas de cause racine » sont des enquêtes incomplètes.

## Techniques d'appui

Ces techniques font partie du débogage systématique et sont disponibles dans ce répertoire :

- **`root-cause-tracing.md`** — Tracer les bugs à rebours dans la pile d'appels jusqu'au déclencheur initial
- **`defense-in-depth.md`** — Ajouter de la validation à plusieurs couches après avoir trouvé la cause racine
- **`condition-based-waiting.md`** — Remplacer les timeouts arbitraires par du polling sur condition
