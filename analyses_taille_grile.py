from generation_instance import *
from resolution_instance import *
import random

generer = False


if generer:
    # génération d'instances et ecriture dans le fichier d'intances
    liste_tailles = [(i,i) for i in range(10,60,10)]

    liste_instances = []
    for (N,M) in liste_tailles:
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
            
            liste_instances.append(generation_instances(N,M,d1,d2,f1,f2,o,N,1)[0])
            # print(f"{d1} {d2} {f1} {f2} {o}")

    ecriture_instances("instances_analyses_grille.txt",liste_instances)



fichier = open("instances_analyses_grille.txt","r")
liste_instances = lire_fichier(fichier)
nb_instances = len(liste_instances)
print(liste_instances[0])
print(nb_instances)

# résolution des instances

for inst in liste_instances:
    ((N, M),matrice,(D1, D2, F1, F2, direction)) = inst
    graphe = generer_graphe(N,M,matrice)
    temps, commandes = plus_court_chemin(graphe,(D1, D2,direction),(F1, F2))
    print(f"{temps} {" ".join(commandes)}")

