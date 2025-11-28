from generation_instance import *
from resolution_instance import *
import time as t
import random

generer = True
size=(20,20)
N,M=size
grille=np.zeros(size,dtype=np.int64)
if generer:
    # génération d'instances et ecriture dans le fichier d'intances
    liste_obstacle=[i for i in range(10,60,10)]
    liste_instances = []
    for obs_n in liste_obstacle:
        for _ in range(10):
            # N,M,d1,d2,f1,f2,o,nb_obstacles,nb_instances

            d1 = random.randint(0,N)
            d2 = random.randint(0,M)

            while True:
                f1 = random.randint(0,N)
                f2 = random.randint(0,M)

                if (f1, f2) != (d1,d2):
                    break

            o = random.choice(["nord","sud","est","ouest"])
            liste_instances.append(generation_instances(N,M,d1,d2,f1,f2,o,obs_n,1)[0])
            # print(f"{d1} {d2} {f1} {f2} {o}")

    ecriture_instances("instances_analyses_nb_obstacle.txt",liste_instances)




fichier = open("instances_analyses_nb_obstacle.txt","r")
liste_instances = lire_fichier(fichier)
nb_instances = len(liste_instances)
print(liste_instances[0])
print(nb_instances)

# résolution des instances

nb_obs_actuel=-1
for inst in liste_instances:
    start=t.perf_counter()
    ((N, M),matrice,(D1, D2, F1, F2, direction)) = inst
    if nb_obs_actuel<0:
        nb_obs_actuel=matrice.sum()
    graphe = generer_graphe(N,M,matrice)
    temps, commandes = plus_court_chemin(graphe,(D1, D2,direction),(F1, F2))
    end=t.perf_counter()
    print(f"{temps} {" ".join(commandes)}\ntemps algo  {nb_obs_actuel}")
