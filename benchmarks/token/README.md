# Benchmark de tokens — scénario clé-en-main

Mesure, sur un scénario reproductible, l'écart de consommation de tokens entre le
plugin **d'origine** (baseline) et le **fork optimisé** (candidat). Objectif : /2.

Le scénario (`scenario.md`) est un petit module Python (remises par paliers, avec
tests). Il est volontairement modeste : il isole surtout le **surcoût de cérémonie**
(brainstorming/plan/review sur une tâche simple) — c'est là que le fork économise le
plus. Pour mesurer une grosse tâche, remplace `scenario.md` par la tienne.

## Contenu

| Fichier | Rôle |
|---------|------|
| `scenario.md` | Le prompt figé, identique aux deux runs |
| `setup-fixture.sh` | Crée un projet Python déterministe (même état de départ) |
| `run.sh` | Lance le scénario en headless (`claude -p`), capture le transcript, écrit un JSON |
| `summary.py` | Agrège les runs d'un label et compare baseline vs candidat (verdict /2) |
| `results/` | Rapports JSON produits (git-ignoré) |

## Prérequis

- CLI `claude` dans le PATH (le benchmark utilise le mode headless `claude -p`).
- `python3`. Les runs sont autonomes (`--dangerously-skip-permissions` par défaut,
  surchargeable via `CLAUDE_ARGS`) car le scénario édite des fichiers et lance pytest.

## Procédure A/B

> Règle d'or : **même modèle** et **même scénario** des deux côtés. Répète 3× et
> compare les moyennes (les sessions LLM varient de ±15-20 %).

1. **Baseline** — active le plugin **d'origine** (`obra/superpowers`) ou désactive le
   fork, puis :

   ```bash
   benchmarks/token/run.sh --label baseline --model <ton-modèle> --repeat 3
   ```

2. **Candidat** — active le **fork optimisé** (`oi-lab/superpowers`), puis :

   ```bash
   benchmarks/token/run.sh --label candidate --model <ton-modèle> --repeat 3
   ```

3. **Compare** :

   ```bash
   python3 benchmarks/token/summary.py --compare baseline candidate --target 50
   ```

   Sortie : coût pondéré moyen de chaque côté, réduction %, et verdict
   `Objectif /2 : ATTEINT/NON`.

### Basculer entre plugin d'origine et fork

Selon ton installation :
- **Marketplaces séparés** : garde deux entrées (`obra/...` et `oi-lab/...`) et
  active/désactive via `/plugin` entre les deux campagnes de runs.
- **Sur place** : `git checkout` du tag/commit d'origine pour la baseline, puis de la
  branche du fork pour le candidat, en réinstallant le plugin entre les deux.

Le runner ne fait que mesurer ce qui est **actif** au moment du run ; c'est toi qui
choisis quelle version est chargée.

## Tarifs

`run.sh` utilise les tarifs par défaut de `token-report.py` (Opus, $15/$75 par M).
Pour un autre modèle, exporte par exemple :

```bash
export TOKEN_COST_ARGS="--input-cost 3 --output-cost 15"   # Sonnet
```

## Lire le résultat

- **Coût pondéré** = meilleur proxy quota (output cher, cache_read ×0.1, write ×1.25).
- Regarde aussi, via `python3 scripts/token-report.py <transcript>`, la part
  **output** vs **cache_read** et le poids des **sous-agents** : beaucoup de sous-agents
  coûteux = workflows lourds déclenchés (ce que le fork rend opt-in).

## Limites

- Un scénario ne « prouve » pas le /2 dans l'absolu ; il chiffre l'écart sur CE
  scénario. Ajoute des scénarios plus gros pour couvrir tes vrais projets.
- Le mode headless peut se comporter légèrement différemment d'une session
  interactive ; l'important est qu'il soit **identique** pour baseline et candidat.
