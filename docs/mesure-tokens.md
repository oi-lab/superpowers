# Protocole de mesure de la consommation de tokens

But : vérifier empiriquement l'effet des optimisations du plugin sur la
consommation de tokens (objectif : la diviser par 2), et voir où partent les tokens.

## Outils (`scripts/`)

| Script | Rôle |
|--------|------|
| `find-sessions.py` | Liste les sessions Claude Code récentes (date, taille, id, 1er prompt) |
| `token-report.py` | Rapport détaillé d'UNE session : main + sous-agents, input/output/cache, coût pondéré |
| `token-compare.py` | Compare DEUX sessions (baseline vs candidat) et rend un verdict vs objectif |

`token-report.py` couvre les deux formats de sous-agents (inline `toolUseResult`
et fichiers séparés `<session>/subagents/agent-*.jsonl`).

## Où sont les transcripts

`~/.claude/projects/<cwd-encodé>/<session-id>.jsonl` (ex. `/home/user/superpowers`
devient `-home-user-superpowers`). Les sous-agents sont dans
`<session-id>/subagents/agent-*.jsonl`.

```bash
python3 scripts/find-sessions.py --limit 15 --project superpowers
```

## Métrique retenue

Le **coût pondéré** (`token-compare.py` → « Coût pondéré ($) ») est le meilleur proxy
de la consommation, car il applique des poids réalistes :

- output = cher (par défaut $75/M, tarif Opus)
- input net = $15/M
- **cache_read = 0.1×** input, **cache_write = 1.25×** input

Ajuste au modèle réellement utilisé :
`--input-cost 3 --output-cost 15` pour Sonnet, `15 / 75` pour Opus (défaut).

> Observation utile : sur les longues sessions, le **cache_read** domine largement le
> total brut (contexte relu à chaque tour). C'est pourquoi réduire la longueur des
> échanges (mode compact, Phase 2) et le nombre de sous-agents (opt-in, Phase 3) pèse
> plus que la taille des skills.

## Méthode A/B (recommandée pour l'objectif /2)

Compare le fork optimisé à une **référence**, sur un scénario identique.

1. **Choisis un scénario reproductible** : un même prompt de départ menant à un
   travail de dev représentatif de ton usage (ex. « ajoute un CRUD Produit à ce
   projet Laravel + une page React de liste »). Fige-le dans un fichier.

2. **Session BASELINE** : dans un dépôt de test propre, avec le **plugin d'origine**
   (upstream `obra/superpowers`) OU le plugin désactivé. Nouvelle session, colle le
   scénario, laisse-la se dérouler jusqu'au bout. Note l'id de session.

3. **Session CANDIDAT** : même dépôt remis à l'état initial (`git reset --hard`,
   `git clean -fd`), avec le **fork optimisé** installé. Nouvelle session, même
   scénario, même modèle.

4. **Compare** :

   ```bash
   python3 scripts/token-compare.py \
     ~/.claude/projects/<projet>/<baseline-id>.jsonl \
     ~/.claude/projects/<projet>/<candidat-id>.jsonl \
     --target 50 --input-cost 15 --output-cost 75
   ```

   Le script imprime la réduction par métrique et un verdict `Objectif /2 : ATTEINT/NON`.
   Code de sortie 0 si l'objectif est atteint, 2 sinon (utilisable en CI/script).

## Contre la variance (important)

Les sessions LLM sont non déterministes. Pour une mesure fiable :

- Même **modèle** et même **scénario** exact des deux côtés.
- Même **état de dépôt** de départ (reset entre les runs).
- Répète chaque côté **2-3 fois** et compare les **moyennes** (ou les médianes), pas un
  run isolé. Un écart de ±15-20 % entre runs identiques est normal.
- Évite les interruptions manuelles qui changent la trajectoire.

## Auto-diagnostic rapide (sans baseline)

Pour juste voir où partent tes tokens sur une vraie session :

```bash
python3 scripts/token-report.py ~/.claude/projects/<projet>/<session-id>.jsonl
```

Regarde : part de l'**output** vs **cache_read** ; poids des **sous-agents** vs le
**main**. Beaucoup de sous-agents très coûteux = signe que des workflows lourds se
déclenchent trop (levier Phase 3).

## Limites

- Le comparatif suppose des scénarios équivalents ; il ne « prouve » pas le /2 dans
  l'absolu, il chiffre l'écart sur un scénario donné.
- Les changements de comportement (Phase 3) relèvent aussi des evals `drill`
  (`evals/`), qui jugent la conformité, pas seulement les tokens.
