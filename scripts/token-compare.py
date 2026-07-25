#!/usr/bin/env python3
"""
Compare la consommation de tokens de deux sessions Claude Code (avant/après)
et rend un verdict par rapport à un objectif de réduction (défaut : 50 %, le /2).

Usage :
    scripts/token-compare.py <baseline.jsonl> <candidat.jsonl>
                             [--target 50] [--input-cost 15] [--output-cost 75]

- baseline  = session de référence (ex. plugin d'origine, ou plugin désactivé)
- candidat  = session à évaluer (ex. plugin optimisé)

Lance le MÊME scénario dans les deux sessions (voir docs/mesure-tokens.md).
"""

import sys
import argparse
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "token_report", Path(__file__).resolve().parent / "token-report.py"
)
_tr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tr)
build_report, fmt = _tr.build_report, _tr.fmt


def pct_reduction(base, cand):
    if base == 0:
        return 0.0
    return (base - cand) / base * 100.0


def line(label, base, cand):
    red = pct_reduction(base, cand)
    arrow = "↓" if cand < base else ("↑" if cand > base else "=")
    print(f"{label:<26}{fmt(int(base)):>14}{fmt(int(cand)):>14}{arrow:>3}{red:>8.1f}%")


def total_tokens(t):
    return t["input_tokens"] + t["cache_creation"] + t["cache_read"] + t["output_tokens"]


def main():
    ap = argparse.ArgumentParser(description="Comparateur de tokens avant/après")
    ap.add_argument("baseline")
    ap.add_argument("candidate")
    ap.add_argument("--target", type=float, default=50.0, help="réduction cible en %% (défaut 50)")
    ap.add_argument("--input-cost", type=float, default=15.0)
    ap.add_argument("--output-cost", type=float, default=75.0)
    args = ap.parse_args()

    for p in (args.baseline, args.candidate):
        if not Path(p).exists():
            print(f"Erreur : fichier introuvable : {p}", file=sys.stderr)
            sys.exit(1)

    b = build_report(args.baseline, True, args.input_cost, args.output_cost)
    c = build_report(args.candidate, True, args.input_cost, args.output_cost)
    bt, ct = b["totals"], c["totals"]

    print("=" * 65)
    print("COMPARAISON DE CONSOMMATION — baseline vs candidat")
    print("=" * 65)
    print(f"baseline : {args.baseline}")
    print(f"candidat : {args.candidate}")
    print("-" * 65)
    print(f"{'Métrique':<26}{'baseline':>14}{'candidat':>14}{'':>3}{'réduc.':>8}")
    print("-" * 65)
    line("Tokens output", bt["output_tokens"], ct["output_tokens"])
    line("Tokens input (net)", bt["input_tokens"], ct["input_tokens"])
    line("Cache read", bt["cache_read"], ct["cache_read"])
    line("Cache write", bt["cache_creation"], ct["cache_creation"])
    line("Total tokens (bruts)", total_tokens(bt), total_tokens(ct))
    line("Coût pondéré ($)", b["cost"], c["cost"])
    print("-" * 65)

    cost_red = pct_reduction(b["cost"], c["cost"])
    tok_red = pct_reduction(total_tokens(bt), total_tokens(ct))
    print()
    print(f"  Réduction coût pondéré : {cost_red:.1f} %  (cible : {args.target:.0f} %)")
    print(f"  Réduction tokens bruts : {tok_red:.1f} %")
    verdict = "ATTEINT ✅" if cost_red >= args.target else "NON ATTEINT ❌"
    print(f"  Objectif /{100/args.target:.0f} : {verdict}")
    print("=" * 65)
    sys.exit(0 if cost_red >= args.target else 2)


if __name__ == "__main__":
    main()
