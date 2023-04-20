
import numpy as np

dico: dict[int, int] = {}

for i in range(100):
    val = int(np.random.normal(0.5) * 100)
    if val in dico:
        dico[val] += 1
    else:
        dico[val] = 1

print(dico)
