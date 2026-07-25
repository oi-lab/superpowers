---
name: verification-before-completion
description: À utiliser au moment de déclarer un travail terminé, corrigé ou passant, avant de committer ou créer des PR - exige de lancer les commandes de vérification et de confirmer la sortie avant toute affirmation de succès ; des preuves avant les affirmations, toujours
---

# Vérification avant de conclure

**Principe fondamental :** des preuves avant les affirmations, toujours.

## La loi d'airain

```
AUCUNE AFFIRMATION DE COMPLÉTION SANS PREUVE DE VÉRIFICATION FRAÎCHE
```

Si tu n'as pas lancé la commande de vérification dans ce message, tu ne peux pas affirmer que ça passe.

## La fonction de contrôle

```
AVANT d'affirmer un statut ou d'exprimer une satisfaction :

1. IDENTIFIE : quelle commande prouve cette affirmation ?
2. LANCE : exécute la commande COMPLÈTE (fraîche, entière)
3. LIS : la sortie complète, vérifie le code de sortie, compte les échecs
4. VÉRIFIE : la sortie confirme-t-elle l'affirmation ?
   - Si NON : énonce le statut réel avec preuves
   - Si OUI : énonce l'affirmation AVEC preuves
5. SEULEMENT ALORS : formule l'affirmation

Sauter une étape = mentir, pas vérifier
```

## Échecs courants

| Affirmation | Exige | Insuffisant |
|-------|----------|----------------|
| Les tests passent | Sortie de la commande de test : 0 échec | Lancement précédent, « devrait passer » |
| Linter propre | Sortie du linter : 0 erreur | Vérification partielle, extrapolation |
| Le build réussit | Commande de build : exit 0 | Linter qui passe, logs qui semblent bons |
| Bug corrigé | Test du symptôme initial : passe | Code modifié, corrigé supposé |
| Test de régression fonctionne | Cycle rouge-vert vérifié | Le test passe une fois |
| Agent a terminé | Le diff VCS montre les changements | L'agent rapporte « succès » |
| Exigences satisfaites | Checklist ligne par ligne | Tests qui passent |

## Signaux d'alarme — STOP

- Utiliser « devrait », « probablement », « semble »
- Exprimer une satisfaction avant vérification (« Super ! », « Parfait ! », « Fini ! »…)
- Sur le point de committer/pusher/faire une PR sans vérification
- Faire confiance aux rapports de succès d'un agent
- S'appuyer sur une vérification partielle
- Penser « juste cette fois »
- Fatigué et vouloir en finir
- **TOUTE formulation impliquant un succès sans avoir lancé la vérification**

## Prévention des rationalisations

| Excuse | Réalité |
|--------|---------|
| « Ça devrait marcher maintenant » | LANCE la vérification |
| « Je suis confiant » | Confiance ≠ preuve |
| « Juste cette fois » | Aucune exception |
| « Le linter est passé » | Linter ≠ compilateur |
| « L'agent a dit succès » | Vérifie indépendamment |
| « Je suis fatigué » | Épuisement ≠ excuse |
| « Une vérification partielle suffit » | Le partiel ne prouve rien |
| « Mots différents donc la règle ne s'applique pas » | L'esprit prime sur la lettre |

## Motif clé — test de régression (TDD Rouge-Vert)

```
✅ Écris → Lance (pass) → Annule le correctif → Lance (DOIT ÉCHOUER) → Restaure → Lance (pass)
❌ « J'ai écrit un test de régression » (sans vérification rouge-vert)
```

## Quand l'appliquer

**TOUJOURS avant :** toute affirmation de succès/complétion, expression de satisfaction, déclaration positive sur l'état du travail ; commit, PR, complétion de tâche ; passage à la tâche suivante ; délégation à des agents.

**S'applique aux :** phrases exactes, paraphrases et synonymes, implications de succès, TOUTE communication suggérant complétion/exactitude.
