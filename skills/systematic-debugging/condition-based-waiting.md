# Attente basée sur une condition

## Vue d'ensemble

Les tests instables devinent souvent le timing avec des délais arbitraires. Cela crée des conditions de course où les tests passent sur des machines rapides mais échouent sous charge ou en CI.

**Principe central :** attends la condition réelle qui t'intéresse, pas une supposition sur le temps qu'elle prend.

## Quand l'utiliser

Si un test utilise `setTimeout`/`sleep` : quand il teste réellement un comportement de timing, documente POURQUOI le timeout est nécessaire ; sinon, passe à une attente basée sur une condition.

**Utilise quand :**
- Les tests ont des délais arbitraires (`setTimeout`, `sleep`, `time.sleep()`)
- Les tests sont instables (passent parfois, échouent sous charge)
- Les tests dépassent le délai quand ils tournent en parallèle
- Tu attends la fin d'opérations asynchrones

**N'utilise pas quand :**
- Tu testes un vrai comportement de timing (intervalles de debounce, throttle)
- Documente toujours POURQUOI si tu utilises un timeout arbitraire

## Pattern principal

```typescript
// ❌ BEFORE: Guessing at timing
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ AFTER: Waiting for condition
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

## Patterns rapides

| Scénario | Pattern |
|----------|---------|
| Attendre un événement | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Attendre un état | `waitFor(() => machine.state === 'ready')` |
| Attendre un décompte | `waitFor(() => items.length >= 5)` |
| Attendre un fichier | `waitFor(() => fs.existsSync(path))` |
| Condition complexe | `waitFor(() => obj.ready && obj.value > 10)` |

## Implémentation

Fonction de polling générique :
```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise(r => setTimeout(r, 10)); // Poll every 10ms
  }
}
```

Voir `condition-based-waiting-example.ts` dans ce répertoire pour une implémentation complète avec des helpers spécifiques au domaine (`waitForEvent`, `waitForEventCount`, `waitForEventMatch`) issus d'une vraie session de débogage.

## Erreurs courantes

**❌ Polling trop rapide :** `setTimeout(check, 1)` — gaspille le CPU
**✅ Correction :** poll toutes les 10ms

**❌ Pas de timeout :** boucle infinie si la condition n'est jamais remplie
**✅ Correction :** inclus toujours un timeout avec une erreur claire

**❌ Données périmées :** état mis en cache avant la boucle
**✅ Correction :** appelle le getter dans la boucle pour des données fraîches

## Quand un timeout arbitraire EST correct

```typescript
// Tool ticks every 100ms - need 2 ticks to verify partial output
await waitForEvent(manager, 'TOOL_STARTED'); // First: wait for condition
await new Promise(r => setTimeout(r, 200));   // Then: wait for timed behavior
// 200ms = 2 ticks at 100ms intervals - documented and justified
```

**Exigences :**
1. Attends d'abord la condition déclencheuse
2. Base-toi sur un timing connu (pas une supposition)
3. Un commentaire expliquant POURQUOI

## Impact concret

D'une session de débogage (2025-10-03) :
- 15 tests instables corrigés dans 3 fichiers
- Taux de réussite : 60% → 100%
- Temps d'exécution : 40% plus rapide
- Plus de conditions de course
