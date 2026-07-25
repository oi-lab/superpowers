#!/usr/bin/env python3
"""
Rapport de consommation de tokens pour une session Claude Code.

Somme la session principale ET les sous-agents, qu'ils soient :
  - inline dans le transcript principal (via toolUseResult, ancien format), OU
  - dans des fichiers séparés `<session>/subagents/agent-*.jsonl` (Claude Code web).

Usage :
    scripts/token-report.py <session.jsonl> [--json] [--no-subagents]
                            [--input-cost 15] [--output-cost 75]

Par défaut le coût est estimé aux tarifs Opus ($15 / $75 par M tokens). Ajuste
--input-cost / --output-cost pour ton modèle. Multiplicateurs cache appliqués :
cache_read = 0.1x input, cache_creation (write) = 1.25x input.
"""

import json
import sys
import argparse
from pathlib import Path

# Multiplicateurs de cache (relatifs au tarif input de base)
CACHE_READ_MULT = 0.1
CACHE_WRITE_MULT = 1.25


def empty():
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation": 0,
        "cache_read": 0,
        "messages": 0,
    }


def add(acc, usage):
    acc["input_tokens"] += usage.get("input_tokens", 0)
    acc["output_tokens"] += usage.get("output_tokens", 0)
    acc["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
    acc["cache_read"] += usage.get("cache_read_input_tokens", 0)


def scan_file(path):
    """Somme l'usage des messages assistant d'un fichier transcript."""
    acc = empty()
    inline_subagents = {}
    with open(path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
            except Exception:
                continue
            if data.get("type") == "assistant" and "message" in data:
                acc["messages"] += 1
                add(acc, data["message"].get("usage", {}))
            # Ancien format : sous-agents inline via toolUseResult
            if data.get("type") == "user" and "toolUseResult" in data:
                result = data["toolUseResult"]
                if isinstance(result, dict) and "usage" in result and "agentId" in result:
                    aid = result["agentId"]
                    sub = inline_subagents.setdefault(aid, empty())
                    sub["messages"] += 1
                    add(sub, result["usage"])
    return acc, inline_subagents


def subagent_dir_for(main_path):
    """<dir>/<stem>/subagents/ pour le format fichiers séparés."""
    p = Path(main_path)
    return p.parent / p.stem / "subagents"


def analyze_session(main_path, include_subagents=True):
    """Retourne (main, {label: usage}) en couvrant les deux formats."""
    main, inline = scan_file(main_path)
    subs = dict(inline)
    if include_subagents:
        sdir = subagent_dir_for(main_path)
        if sdir.is_dir():
            for f in sorted(sdir.glob("agent-*.jsonl")):
                acc, _ = scan_file(f)
                subs[f.stem] = acc
    return main, subs


def weighted_cost(u, input_cost, output_cost):
    base = input_cost / 1_000_000
    out = output_cost / 1_000_000
    return (
        u["input_tokens"] * base
        + u["cache_creation"] * base * CACHE_WRITE_MULT
        + u["cache_read"] * base * CACHE_READ_MULT
        + u["output_tokens"] * out
    )


def totals(main, subs):
    t = empty()
    for u in [main, *subs.values()]:
        for k in t:
            t[k] += u[k]
    return t


def fmt(n):
    return f"{n:,}"


def build_report(main_path, include_subagents, input_cost, output_cost):
    main, subs = analyze_session(main_path, include_subagents)
    t = totals(main, subs)
    return {
        "session": str(main_path),
        "main": main,
        "subagents": subs,
        "totals": t,
        "cost": weighted_cost(t, input_cost, output_cost),
        "input_cost_per_m": input_cost,
        "output_cost_per_m": output_cost,
    }


def print_report(rep):
    main, subs, t = rep["main"], rep["subagents"], rep["totals"]
    print("=" * 92)
    print(f"CONSOMMATION DE TOKENS — {rep['session']}")
    print("=" * 92)
    print(f"{'Agent':<28}{'Msgs':>6}{'Input':>12}{'Output':>12}{'CacheW':>12}{'CacheR':>12}")
    print("-" * 92)

    def row(label, u):
        print(f"{label[:28]:<28}{u['messages']:>6}{fmt(u['input_tokens']):>12}"
              f"{fmt(u['output_tokens']):>12}{fmt(u['cache_creation']):>12}{fmt(u['cache_read']):>12}")

    row("main (coordinateur)", main)
    for label in sorted(subs):
        row(label, subs[label])
    print("-" * 92)
    row("TOTAL", t)
    print()
    total_all = t["input_tokens"] + t["cache_creation"] + t["cache_read"] + t["output_tokens"]
    print(f"  Tokens output          : {fmt(t['output_tokens'])}")
    print(f"  Tokens input (net)     : {fmt(t['input_tokens'])}")
    print(f"  Cache write / read     : {fmt(t['cache_creation'])} / {fmt(t['cache_read'])}")
    print(f"  Total tokens (bruts)   : {fmt(total_all)}")
    print(f"  Coût pondéré estimé    : ${rep['cost']:.2f}  "
          f"(input ${rep['input_cost_per_m']}/M, output ${rep['output_cost_per_m']}/M,"
          f" cacheR x{CACHE_READ_MULT}, cacheW x{CACHE_WRITE_MULT})")
    print("=" * 92)


def main():
    ap = argparse.ArgumentParser(description="Rapport de tokens d'une session Claude Code")
    ap.add_argument("session", help="chemin du transcript principal .jsonl")
    ap.add_argument("--json", action="store_true", help="sortie JSON machine")
    ap.add_argument("--no-subagents", action="store_true", help="ignorer les sous-agents")
    ap.add_argument("--input-cost", type=float, default=15.0, help="$/M tokens input (défaut Opus 15)")
    ap.add_argument("--output-cost", type=float, default=75.0, help="$/M tokens output (défaut Opus 75)")
    args = ap.parse_args()

    if not Path(args.session).exists():
        print(f"Erreur : fichier introuvable : {args.session}", file=sys.stderr)
        sys.exit(1)

    rep = build_report(args.session, not args.no_subagents, args.input_cost, args.output_cost)
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print_report(rep)


if __name__ == "__main__":
    main()
