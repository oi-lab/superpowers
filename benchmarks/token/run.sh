#!/usr/bin/env bash
# Runner clé-en-main du benchmark de tokens.
#
# Pour chaque exécution : crée un fixture neuf, lance le scénario en mode headless
# (claude -p), capture le transcript de session, et enregistre un rapport JSON.
#
# Usage :
#   benchmarks/token/run.sh --label baseline  [--model <id>] [--repeat 3]
#   benchmarks/token/run.sh --label candidate [--model <id>] [--repeat 3]
#
# A/B : lance --label baseline avec le plugin D'ORIGINE (ou désactivé), puis
# --label candidate avec le FORK optimisé. MÊME --model des deux côtés. Voir README.md.
#
# Réglages :
#   --model <id>     modèle passé à claude (fortement recommandé pour l'équité A/B)
#   --repeat N       nombre d'exécutions (défaut 1 ; 3+ recommandé pour la variance)
#   --keep-fixture   ne pas supprimer les fixtures créés
#   CLAUDE_ARGS=...  args supplémentaires passés à `claude` (ex. permissions)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
SCENARIO="$HERE/scenario.md"
RESULTS="$HERE/results"
REPORT="$REPO_ROOT/scripts/token-report.py"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
PROJECTS="$CLAUDE_HOME/projects"

LABEL=""
MODEL=""
REPEAT=1
KEEP=0
# Par défaut, headless autonome : le scénario doit pouvoir éditer des fichiers et lancer les tests.
DEFAULT_CLAUDE_ARGS="--dangerously-skip-permissions"

while [ $# -gt 0 ]; do
  case "$1" in
    --label) LABEL="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --repeat) REPEAT="$2"; shift 2;;
    --keep-fixture) KEEP=1; shift;;
    *) echo "Argument inconnu : $1" >&2; exit 1;;
  esac
done

[ -n "$LABEL" ] || { echo "Erreur : --label requis (baseline | candidate)" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "Erreur : 'claude' introuvable dans le PATH." >&2; exit 1; }
mkdir -p "$RESULTS"

extra_args="${CLAUDE_ARGS:-$DEFAULT_CLAUDE_ARGS}"
model_args=""; [ -n "$MODEL" ] && model_args="--model $MODEL"

for i in $(seq 1 "$REPEAT"); do
  echo "=========================================================="
  echo "[$LABEL] run $i/$REPEAT"
  FIXTURE="$(bash "$HERE/setup-fixture.sh" | tail -1)"
  echo "fixture : $FIXTURE"

  START=$(date +%s)
  echo "→ lancement de claude -p (headless)…"
  # shellcheck disable=SC2086
  ( cd "$FIXTURE" && claude -p "$(cat "$SCENARIO")" $model_args $extra_args ) \
    > "$FIXTURE/.claude-stdout.log" 2>&1 || echo "  (claude a retourné un code non nul — on capture quand même le transcript)"

  # Transcript principal le plus récent modifié depuis START (hors sous-agents)
  TRANSCRIPT="$(find "$PROJECTS" -mindepth 2 -maxdepth 2 -name '*.jsonl' -newermt "@$START" \
                 -not -path '*/subagents/*' -printf '%T@\t%p\n' 2>/dev/null \
                 | sort -rn | head -1 | cut -f2-)"

  if [ -z "$TRANSCRIPT" ]; then
    echo "  ⚠ aucun transcript trouvé sous $PROJECTS depuis le début du run." >&2
    echo "    Vérifie que 'claude -p' écrit bien une session, et CLAUDE_CONFIG_DIR." >&2
  else
    OUT="$RESULTS/${LABEL}-$(date +%Y%m%d-%H%M%S)-run${i}.json"
    model_cost_args=""
    # Tarifs : Opus par défaut dans token-report ; ajustables via TOKEN_COST_ARGS
    python3 "$REPORT" "$TRANSCRIPT" --json ${TOKEN_COST_ARGS:-} > "$OUT"
    echo "  transcript : $TRANSCRIPT"
    echo "  résultat   : $OUT"
    python3 "$REPORT" "$TRANSCRIPT" ${TOKEN_COST_ARGS:-} | tail -8
  fi

  [ "$KEEP" -eq 1 ] || rm -rf "$FIXTURE"
done

echo "=========================================================="
echo "Terminé. Agrège avec :  python3 $HERE/summary.py --label $LABEL"
echo "Compare avec        :  python3 $HERE/summary.py --compare baseline candidate --target 50"
