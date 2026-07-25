---
name: test-driven-development
description: À utiliser pour implémenter toute fonctionnalité ou correction de bug, avant d'écrire le code d'implémentation
---

# Développement piloté par les tests (TDD)

## Vue d'ensemble

Écris le test d'abord. Regarde-le échouer. Écris le code minimal pour le faire passer.

**Principe central :** si tu n'as pas vu le test échouer, tu ne sais pas s'il teste la bonne chose.

**Violer la lettre des règles, c'est violer leur esprit.**

## Quand l'utiliser

**Toujours :** nouvelles fonctionnalités, corrections de bugs, refactorisation, changements de comportement.

**Exceptions (demande à ton partenaire humain) :** prototypes jetables, code généré, fichiers de configuration.

Tu penses « je saute le TDD juste cette fois » ? Stop. C'est une rationalisation.

## La loi d'airain

```
AUCUN CODE DE PRODUCTION SANS UN TEST QUI ÉCHOUE D'ABORD
```

Tu as écrit du code avant le test ? Supprime-le. Recommence.

**Aucune exception :**
- Ne le garde pas comme « référence »
- Ne l'« adapte » pas en écrivant les tests
- Ne le regarde pas
- Supprimer veut dire supprimer

Réimplémente à neuf à partir des tests. Point.

## Rouge-Vert-Refactor

Cycle : RED (test qui échoue) → vérifier qu'il échoue correctement → GREEN (code minimal) → vérifier qu'il passe, tout vert → REFACTOR (nettoyer en restant vert) → tâche suivante. Test qui échoue pour une mauvaise raison → retour à RED ; code qui ne passe pas → reste en GREEN.

### RED - Écrire un test qui échoue

Écris un test minimal montrant ce qui devrait se passer.

<Good>
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const op = () => { attempts++; if (attempts < 3) throw new Error('fail'); return 'success'; };
  const result = await retryOperation(op);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Nom clair, teste un comportement réel, une seule chose
</Good>

Mauvais : `test('retry works')` avec un `jest.fn()` mocké — nom vague, teste le mock et non le code.

**Exigences :** un comportement, nom clair, code réel (pas de mocks sauf inévitable).

### Vérifier RED - Regarde-le échouer

**OBLIGATOIRE. Ne saute jamais cette étape.**

```bash
npm test path/to/test.test.ts
```

Confirme : le test échoue (n'erre pas) ; le message d'échec est celui attendu ; il échoue parce que la fonctionnalité manque (pas à cause d'une faute de frappe).

**Le test passe ?** Tu testes un comportement existant. Corrige le test. **Le test erre ?** Corrige l'erreur, relance jusqu'à ce qu'il échoue correctement.

### GREEN - Code minimal

Écris le code le plus simple qui fait passer le test — bon : une boucle `for (i<3)` avec `try/return await fn()` et `throw` au dernier essai, juste assez pour passer. Mauvais : une signature avec `options?: { maxRetries, backoff, onRetry }` — sur-conçu, YAGNI.

N'ajoute pas de fonctionnalités, ne refactorise pas d'autre code, n'« améliore » rien au-delà du test.

### Vérifier GREEN - Regarde-le passer

**OBLIGATOIRE.**

```bash
npm test path/to/test.test.ts
```

Confirme : le test passe ; les autres tests passent toujours ; sortie impeccable (aucune erreur, aucun avertissement).

**Le test échoue ?** Corrige le code, pas le test. **D'autres tests échouent ?** Corrige maintenant.

### REFACTOR - Nettoyer

Uniquement après le vert : supprimer la duplication, améliorer les noms, extraire des helpers. Garde les tests verts. N'ajoute pas de comportement.

### Répéter

Prochain test qui échoue pour la prochaine fonctionnalité.

## Bons tests

| Qualité | Bon | Mauvais |
|---------|------|-----|
| **Minimal** | Une seule chose. Un « et » dans le nom ? Sépare-le. | `test('validates email and domain and whitespace')` |
| **Clair** | Le nom décrit le comportement | `test('test1')` |
| **Montre l'intention** | Démontre l'API souhaitée | Masque ce que le code devrait faire |

Quand tu écris ou modifies un test, lis [writing-good-tests.md](writing-good-tests.md) pour les règles qui gardent les tests honnêtes :
- Nomme le changement de production qui ferait échouer le test — avant de l'écrire
- Assertion sur un comportement réel, jamais sur le comportement d'un mock
- Garde le code réservé aux tests dans les utilitaires de test, hors des classes de production
- Comprends les effets de bord d'une dépendance avant de la mocker

## Rationalisations courantes

| Excuse | Réalité |
|--------|---------|
| « Trop simple à tester » | Le code simple casse. Le test prend 30 secondes. |
| « Je testerai après » | Les tests écrits après passent immédiatement — ce qui ne prouve rien. Ils peuvent tester la mauvaise chose, tester l'implémentation au lieu du comportement, ou rater le cas limite que tu as oublié. Tu ne l'as jamais vu échouer, donc tu n'as jamais prouvé qu'il peut attraper le bug. Écrire le test d'abord force cet échec. |
| « Tester après atteint les mêmes objectifs (l'esprit, pas le rituel) » | Les tests-après répondent « que fait ce code ? » ; les tests-d'abord répondent « que devrait faire ce code ? ». Les tests écrits après sont biaisés par le code déjà écrit — tu vérifies les cas dont tu te souviens, pas ceux que tu aurais découverts. De la couverture sans preuve que les tests fonctionnent. |
| « Déjà testé manuellement » | Le test manuel est ad hoc : aucune trace de ce que tu as couvert, aucun moyen de le rejouer quand le code change, cas faciles à oublier sous pression. « Ça marchait quand j'ai essayé » ≠ exhaustif. Les tests automatisés s'exécutent de la même façon à chaque fois. |
| « Supprimer X heures est du gâchis » | Sophisme des coûts irrécupérables — ce temps est déjà dépensé de toute façon. Le vrai choix : réécrire avec le TDD (haute confiance) vs. le garder et bricoler des tests après (faible confiance, bugs probables). Garder du code auquel tu ne peux pas te fier, voilà le gâchis. |
| « Garder comme référence, écrire les tests d'abord » | Tu vas l'adapter. C'est tester après. Supprimer veut dire supprimer. |
| « Besoin d'explorer d'abord » | D'accord. Jette l'exploration, recommence avec le TDD. |
| « Test difficile = conception peu claire » | Écoute le test. Difficile à tester = difficile à utiliser. |
| « Le TDD va me ralentir » | Le TDD EST la voie pragmatique : attrape les bugs avant le commit, prévient les régressions, te laisse refactoriser sans peur. Les raccourcis « pragmatiques » mènent au débogage en production — plus lent, pas plus rapide. |
| « Le test manuel est plus rapide » | Le manuel ne prouve pas les cas limites. Tu re-testeras à chaque changement. |
| « Le code existant n'a pas de tests » | Tu l'améliores. Ajoute des tests pour le code existant. |

## Signaux d'alarme - STOP et recommence

- Code avant le test
- Test après l'implémentation
- Le test passe immédiatement
- Impossible d'expliquer pourquoi le test a échoué
- Tests ajoutés « plus tard »
- Rationaliser « juste cette fois »
- « Je l'ai déjà testé manuellement »
- « Tester après atteint le même but »
- « C'est l'esprit, pas le rituel »
- « Garder comme référence » ou « adapter le code existant »
- « Déjà passé X heures, supprimer est du gâchis »
- « Le TDD est dogmatique, je suis pragmatique »
- « C'est différent parce que… »

**Tout cela signifie : supprime le code. Recommence avec le TDD.**

## Checklist de vérification

Avant de marquer le travail comme terminé :

- [ ] Chaque nouvelle fonction/méthode a un test
- [ ] Regardé chaque test échouer avant d'implémenter
- [ ] Chaque test a échoué pour la raison attendue (fonctionnalité manquante, pas faute de frappe)
- [ ] Écrit le code minimal pour faire passer chaque test
- [ ] Tous les tests passent
- [ ] Sortie impeccable (aucune erreur, aucun avertissement)
- [ ] Les tests utilisent du code réel (mocks uniquement si inévitable)
- [ ] Cas limites et erreurs couverts

Impossible de cocher toutes les cases ? Tu as sauté le TDD. Recommence.

## En cas de blocage

| Problème | Solution |
|---------|----------|
| Ne sais pas comment tester | Écris l'API souhaitée. Écris l'assertion d'abord. Demande à ton partenaire humain. |
| Test trop compliqué | Conception trop compliquée. Simplifie l'interface. |
| Dois tout mocker | Code trop couplé. Utilise l'injection de dépendances. |
| Setup de test énorme | Extrais des helpers. Toujours complexe ? Simplifie la conception. |

## Intégration du débogage

Un bug trouvé ? Écris un test qui échoue et le reproduit. Suis le cycle TDD. Le test prouve la correction et prévient la régression. Ne corrige jamais un bug sans test.

## Règle finale

```
Code de production → un test existe et a échoué d'abord
Sinon → ce n'est pas du TDD
```

Aucune exception sans la permission de ton partenaire humain.
