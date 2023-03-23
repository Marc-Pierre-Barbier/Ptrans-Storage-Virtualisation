
# Nos données a évaluer

Chaque stockage posséde 5 variables (dans l'état actuel de nos modification): capacity, nRops, nRband, nWops, nWband

## Moyene et écart type

...

## Temps d'execution

...

## Calcule de l'entropie

### Pourquoi l'entropie

L'entropie permet de mesurer le bruit sur un signal plus notre signal est uniforme moin il y aura d'entropie.
C'est pour cette propriéte que c'est interessent dans notre cas, ca cela permet de comparer 2 solution pour savoir la quel a donnée le resultat avec le taux d'usage le plus uniforme, donc quel approche nous amene a la solution la plus équilibré.

### la methode

plutot que mélanger ces 5 variables, j'ai décité de calculé séparément l'entropie de ces variable.

Ce qui revien a prendre la liste des stockage d'en extraire la liste de notre variable. cette liste est normalisé pour représenter le % d'utilisation de la variable.

Maintenant qu'on a une liste numerique on peut simplement appliquer la formule pour calculer l'entropie.
