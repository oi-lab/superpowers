Construisons un module de remises pour ce petit projet Python.

Objectif : une fonction qui calcule le prix total d'un panier après une remise par
paliers appliquée sur le montant.

Règles métier :
- montant < 50 € : 0 % de remise
- 50 € à < 100 € : 5 %
- 100 € à < 200 € : 10 %
- >= 200 € : 15 %
- Le montant est la somme de prix × quantité de chaque article du panier.
- La remise s'applique au montant total ; arrondir le prix final à 2 décimales.

Contraintes : Python pur, aucune dépendance externe, tests avec pytest. Ajoute le
module dans le package `shop` (dans `src/shop/`) et les tests dans `tests/`.
Quand c'est terminé, lance les tests et confirme qu'ils passent.
