#!/usr/bin/env bash
# Crée un fixture Python DÉTERMINISTE pour le benchmark de tokens.
# Même état de départ à chaque run → comparaison équitable.
#
# Usage : setup-fixture.sh [dossier-cible]
# Sans argument, crée un dossier temporaire et imprime son chemin (dernière ligne).
set -euo pipefail

DEST="${1:-$(mktemp -d -t token-bench-XXXXXX)}"
mkdir -p "$DEST/src/shop" "$DEST/tests"

cat > "$DEST/pyproject.toml" <<'TOML'
[project]
name = "shop"
version = "0.0.0"
requires-python = ">=3.9"

[tool.pytest.ini_options]
pythonpath = ["src"]
TOML

cat > "$DEST/src/shop/__init__.py" <<'PY'
"""Petit paquet e-commerce d'exemple (fixture de benchmark)."""
PY

cat > "$DEST/src/shop/cart.py" <<'PY'
"""Panier : structures de base. Le module de remises reste à écrire."""

from dataclasses import dataclass


@dataclass
class Item:
    price: float
    quantity: int


def subtotal(items):
    """Somme prix × quantité des articles."""
    return sum(i.price * i.quantity for i in items)
PY

cat > "$DEST/tests/test_cart.py" <<'PY'
from shop.cart import Item, subtotal


def test_subtotal():
    assert subtotal([Item(10.0, 2), Item(5.0, 1)]) == 25.0
PY

cat > "$DEST/README.md" <<'MD'
# shop (fixture de benchmark)

Projet Python minimal servant de point de départ reproductible au benchmark de
tokens. `src/shop/cart.py` contient les structures de base ; le module de remises
est à ajouter selon le scénario.

Tests : `python -m pytest`
MD

# Baseline git propre (pour reset entre runs si le fixture est réutilisé)
if command -v git >/dev/null 2>&1; then
  git -C "$DEST" init -q
  git -C "$DEST" add -A
  git -C "$DEST" -c user.email=bench@example.com -c user.name=bench commit -qm "fixture initial" || true
fi

echo "$DEST"
