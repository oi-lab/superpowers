#!/usr/bin/env python3
"""
Agrège et compare les résultats du benchmark de tokens.

Lit les JSON produits par run.sh dans benchmarks/token/results/ (sortie de
token-report.py --json).

Usage :
    summary.py --label baseline                     # moyenne/médiane d'un label
    summary.py --compare baseline candidate [--target 50]
"""

import json
import glob
import statistics
import argparse
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"


def total_tokens(t):
    return t["input_tokens"] + t["cache_creation"] + t["cache_read"] + t["output_tokens"]


def load(label):
    runs = []
    for p in sorted(glob.glob(str(RESULTS / f"{label}-*.json"))):
        try:
            with open(p) as f:
                d = json.load(f)
            runs.append({
                "file": Path(p).name,
                "cost": d["cost"],
                "tokens": total_tokens(d["totals"]),
                "output": d["totals"]["output_tokens"],
            })
        except Exception as e:
            print(f"  (ignoré {p}: {e})")
    return runs


def agg(runs, key):
    vals = [r[key] for r in runs]
    return {
        "mean": statistics.mean(vals),
        "median": statistics.median(vals),
        "n": len(vals),
    }


def show_label(label):
    runs = load(label)
    if not runs:
        print(f"Aucun résultat pour '{label}' dans {RESULTS}")
        return None
    print(f"== {label} ({len(runs)} run(s)) ==")
    print(f"{'fichier':<44}{'coût $':>10}{'tokens':>14}{'output':>12}")
    for r in runs:
        print(f"{r['file']:<44}{r['cost']:>10.2f}{r['tokens']:>14,}{r['output']:>12,}")
    c, t = agg(runs, "cost"), agg(runs, "tokens")
    print(f"{'MOYENNE':<44}{c['mean']:>10.2f}{t['mean']:>14,.0f}")
    print(f"{'MÉDIANE':<44}{c['median']:>10.2f}{t['median']:>14,.0f}")
    print()
    return runs


def compare(a, b, target):
    ra, rb = load(a), load(b)
    if not ra or not rb:
        print("Résultats manquants pour la comparaison.")
        return
    ca = statistics.mean([r["cost"] for r in ra])
    cb = statistics.mean([r["cost"] for r in rb])
    ta = statistics.mean([r["tokens"] for r in ra])
    tb = statistics.mean([r["tokens"] for r in rb])
    cost_red = (ca - cb) / ca * 100 if ca else 0
    tok_red = (ta - tb) / ta * 100 if ta else 0
    print("=" * 60)
    print(f"COMPARAISON  {a} (n={len(ra)})  vs  {b} (n={len(rb)})")
    print("=" * 60)
    print(f"{'Métrique':<22}{a:>16}{b:>16}{'réduc.':>8}")
    print(f"{'Coût pondéré $ (moy)':<22}{ca:>16.2f}{cb:>16.2f}{cost_red:>7.1f}%")
    print(f"{'Tokens bruts (moy)':<22}{ta:>16,.0f}{tb:>16,.0f}{tok_red:>7.1f}%")
    print("-" * 60)
    verdict = "ATTEINT ✅" if cost_red >= target else "NON ATTEINT ❌"
    print(f"Objectif /{100/target:.0f} (réduction ≥ {target:.0f}%) : {verdict}")
    print("=" * 60)
    return 0 if cost_red >= target else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label")
    ap.add_argument("--compare", nargs=2, metavar=("BASELINE", "CANDIDATE"))
    ap.add_argument("--target", type=float, default=50.0)
    args = ap.parse_args()
    if args.compare:
        import sys
        sys.exit(compare(args.compare[0], args.compare[1], args.target) or 0)
    elif args.label:
        show_label(args.label)
    else:
        ap.error("Fournis --label ou --compare")


if __name__ == "__main__":
    main()
