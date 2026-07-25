#!/usr/bin/env python3
"""
Liste les sessions Claude Code récentes pour choisir un transcript à analyser.

Affiche, par session (plus récentes d'abord) : date de modif, taille, id de session,
et le début du premier message utilisateur (pour identifier le scénario).

Usage :
    scripts/find-sessions.py [--limit 15] [--project <chemin>]

Par défaut, cherche sous ~/.claude/projects/. Le sous-dossier projet encode le cwd
(ex. /home/user/superpowers -> -home-user-superpowers).
"""

import json
import argparse
import time
from pathlib import Path


def first_user_prompt(path):
    try:
        with open(path, "r") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") == "user":
                    msg = d.get("message", {})
                    content = msg.get("content")
                    if isinstance(content, list):
                        for part in content:
                            if isinstance(part, dict) and part.get("type") == "text":
                                return part["text"]
                    elif isinstance(content, str):
                        return content
    except Exception:
        pass
    return ""


def main():
    ap = argparse.ArgumentParser(description="Lister les sessions Claude Code récentes")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--project", default=None, help="filtre sous-chaîne sur le dossier projet")
    args = ap.parse_args()

    root = Path.home() / ".claude" / "projects"
    if not root.is_dir():
        print(f"Aucun dossier de sessions : {root}")
        return

    files = [p for p in root.glob("*/*.jsonl")]  # transcripts principaux uniquement
    if args.project:
        files = [p for p in files if args.project in str(p.parent)]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    print(f"{'Modifié':<17}{'Taille':>10}  {'Projet / session'}")
    print("-" * 92)
    for p in files[: args.limit]:
        st = p.stat()
        mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
        size = f"{st.st_size:,}"
        prompt = " ".join(first_user_prompt(p).split())[:52]
        print(f"{mtime:<17}{size:>10}  {p.parent.name}/{p.stem}")
        if prompt:
            print(f"{'':<29}↳ {prompt}")


if __name__ == "__main__":
    main()
