# Écrire de bons tests

**Charge cette référence quand :** tu écris ou modifies des tests, ajoutes des
mocks, ou ajoutes des méthodes de nettoyage/d'aide pour les tests.

## Vue d'ensemble

Un test existe pour attraper une casse précise. Deux principes gouvernent tout
ce qui suit :

```
1. Every test names the break it catches
2. Every test exercises the real thing
```

Le TDD strict produit les deux naturellement : un test écrit en premier et
observé en échec contre du vrai code a déjà prouvé qu'il peut échouer, et il ne
gagne un mock que lorsque la vraie dépendance se révèle lente ou externe.

## Principe 1 : nommer la casse

Avant d'écrire le corps du test, réponds : **quel changement de production
devrait faire échouer ce test — et ce changement est-il un bug ou une
décision ?** Un test gagne sa place en attrapant une mauvaise branche, un effet
de bord manquant, un mauvais argument, un cas limite ou un contrat rompu.

**Dérive les attentes indépendamment.** Utilise des littéraux et des fixtures
vérifiées à la main ; les tests pilotés par table avec des valeurs `want`
littérales sont la forme préférée. Une attente calculée par le code sous test —
ou par ses helpers — passe quoi que ce code fasse :

```typescript
// ❌ Mirror assertion: the same builder computes both sides — always true
const expected = buildSearchQuery({ tag: 'urgent' });
expect(buildSearchQuery({ tag: 'urgent' })).toBe(expected);

// ✅ Hand-derived literal
expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"');
```

**Pas de détecteurs de changement.** Si seules des décisions intentionnelles
peuvent faire échouer un test — la valeur d'une constante, le libellé exact d'un
message, une structure privée — il se déclenche à chaque refonte et dort pendant
les bugs. Teste le comportement qui dépend de la décision : pas
`expect(MAX_RETRIES).toBe(5)` mais « un appel qui échoue est retenté 5 fois et la
6e tentative n'a jamais lieu ».

**Le comportement, pas le texte.** Affirmer qu'un script, un skill ou une config
contient une ligne exacte prouve seulement que la source est la source. Exécute
les scripts sur des entrées contrôlées et affirme les sorties, les effets de bord
ou les codes de sortie. Les documents qui instruisent des agents se testent par
le comportement de l'agent consommateur (superpowers:writing-skills) ; la prose
destinée aux humains ne gagne aucun test.

**Ton code, pas le framework.** Teste le contrat que ton code établit à ses
frontières — la route que tu enregistres, la requête que tu émets, la charge utile
que tu produis. La mécanique amont revient à ses mainteneurs (le classique :
affirmer que ton routeur invoque un handler enregistré — c'est le test du
framework, pas le tien). Quand un comportement amont t'a réellement surpris,
écris un seul test de caractérisation étroit qui nomme l'hypothèse. La même
frontière s'applique à l'intérieur de ton code : constructeurs, getters,
constantes et simples relais ne gagnent des tests que lorsqu'ils valident,
normalisent, appliquent une valeur par défaut, dérivent, imposent ou provoquent
des effets de bord — sinon, affirme le premier résultat visible du consommateur
qui en dépend.

### Fonction de garde

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## Principe 2 : exercer la vraie chose

**Le mock ne gagne aucune assertion.** Une assertion sur un mock passe quand le
mock est présent et échoue quand il est absent — elle ne dit rien sur le
composant. Affirme le comportement du vrai composant ; si c'est le mock que tu
vérifies, dé-mocke-le ou supprime l'assertion.

```typescript
// ✅ Real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// ❌ Mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

**Correction de ton partenaire humain :** « Est-ce qu'on teste le comportement
d'un mock ? »

**Mocke au bon niveau.** Apprends chaque effet de bord de la vraie méthode avant
de la remplacer ; mocke l'opération lente ou externe et garde réel ce dont le
test dépend. En cas de doute, exécute d'abord le test contre l'implémentation
réelle et observe ce qui doit réellement se passer.

```typescript
// ❌ The mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
}));

// ✅ Mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

**Rends les doubles spécifiques.** Quand les arguments, le nombre d'appels ou
l'ordre font partie du contrat, affirme-les — un faux qui accepte n'importe quoi
ne vérifie rien. Donne à chaque branche (succès, erreur, malformé) sa propre
fixture ou son propre spy, pour que la mauvaise branche ne puisse pas satisfaire
l'attente.

**Reflète complètement les vraies données.** Mocke la structure complète telle
qu'elle existe en réalité — tous les champs documentés — pas seulement ceux que
ton test lit. Les mocks partiels échouent silencieusement quand du code aval lit
un champ omis : le test passe pendant que l'intégration casse.

**Les classes de production ne portent que des méthodes de production.** Le
nettoyage dont seuls les tests ont besoin vit dans les utilitaires de test,
jamais comme un `destroy()` sur la classe de production. Demande-toi : cette
méthode n'est-elle appelée que depuis les tests ? Cette classe possède-t-elle le
cycle de vie de cette ressource ? Mauvaises réponses → utilitaire de test.

**Préfère les vrais composants aux mocks complexes.** Quand la mise en place du
mock dépasse la logique du test, quand les mocks ratent des méthodes que les vrais
composants possèdent, ou quand les tests cassent quand le mock change, bascule
vers un test d'intégration avec de vrais composants. **Question de ton partenaire
humain :** « A-t-on besoin d'utiliser un mock ici ? »

### Fonction de garde

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test
  depends on real — mock the slow/external level below them.

  Mock responses mirror the complete real structure.

  A method only tests call lives in test utilities, not production.

  About to assert on the mock itself?
    Unmock it or delete the assertion.
```

## Les tests sont livrés avec l'implémentation

Le cycle TDD — test qui échoue, implémentation minimale, refactor — c'est ce que
« terminé » veut dire. Livre les tests dont le comportement a besoin et rien de
plus : le code trivial et la prose humaine n'en gagnent aucun, et un test écrit
pour satisfaire un processus coûte de la maintenance pour toujours.

## Le contrôle par mutation

Avant de terminer, mute mentalement le code de production ; au moins un test
devrait échouer pour chaque mutation réaliste :

- Mauvaise constante ou mauvais argument
- Mauvais handler de branche
- Changement d'état ou effet de bord manquant
- Retour vide ou par défaut
- Validation manquante pour une entrée à zéro, vide, nulle, non autorisée ou malformée

Une mutation que rien n'attrape signale que le comportement n'est pas protégé —
ou que le test est tautologique.

## Référence rapide

| Quand tu… | Fais |
|-----------|------|
| Écris un test | Nomme la casse qu'il attrape — un bug, pas une décision |
| Construis une valeur attendue | Dérive-la à la main ; jamais avec le code sous test |
| Testes un script ou un document | Exécute-le / pressure-teste son consommateur ; ne grep jamais son texte |
| Es tenté de tester une dépendance | Teste le contrat de ta frontière, pas leur mécanique documentée |
| Veux affirmer sur un élément mocké | Teste le vrai composant, ou dé-mocke-le |
| Es sur le point de mocker une méthode | Apprends ses effets de bord ; mocke le niveau lent/externe |
| Construis une réponse mockée | Reflète complètement la vraie structure |
| As besoin d'un nettoyage utilisé par les seuls tests | Mets-le dans les utilitaires de test |
| Vois la mise en place du mock enfler | Bascule vers un test d'intégration avec de vrais composants |
| Termines un fichier de test | Lance le contrôle par mutation |

## Signaux d'alerte

- Mise en place et assertion partagent le même objet, garantissant l'égalité
- Le test ne peut échouer que par un panic, un crash ou un sélecteur manquant
- Le test échoue à chaque changement intentionnel, jamais à une casse accidentelle
- Les valeurs attendues sont cachées derrière des boucles, des builders ou des helpers
- Le test grep le texte source, ou affirme qu'un symbole supprimé reste supprimé
- Le test importerait encore si seul le framework restait
- Le test existe pour la couverture, ne vérifiant aucun effet de bord ni résultat
- Une assertion vérifie un test ID `*-mock`, ou échoue si tu retires le mock
- Une méthode n'est appelée que depuis des fichiers de test
- La mise en place du mock fait plus de la moitié du test, ou tu ne peux pas expliquer pourquoi le mock est nécessaire
- Mocker « juste au cas où »
