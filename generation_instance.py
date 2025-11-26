# fichier permettant de générer les instances pour les analyses 
# de temps de calcul de l'algorithme
import numpy as np
import random

# fonction permettant de générer àléatoirement nb_instances
# instances en version naive
def generation_instances(N,M,d1,d2,f1,f2,o,nb_obstacles,nb_instances):

    instances = []
    for _ in range(nb_instances):
        matrice = np.zeros((N,M),dtype=int)
        cases_possibles = [(i,j) for i in range(N) for j in range(M) if (i,j) not in [(d1,d2),(f1,f2)]]
        nb_obstacles = min(nb_obstacles,len(cases_possibles))
        obstacles = random.sample(cases_possibles, nb_obstacles)

        for (i,j) in obstacles:
            matrice[i,j] = 1

        instances.append(((N,M),matrice,(d1,d2,f1,f2,o)))

    return instances

# fonction permettant d'écrire les différentes intances dans un fichier 
# soit qui existe deja, soit qu'il va creer
def ecriture_instances(fichier,liste_instances):
    with open(fichier,"w") as f:
        for ((N,M),matrice,(d1,d2,f1,f2,o)) in liste_instances:
            f.write(f"{N} {M}\n")

            for i in range(N):
                ligne_mat = " ".join(str(x) for x in matrice[i])
                f.write(ligne_mat + "\n")

            f.write(f"{d1} {d2} {f1} {f2} {o}\n")

        f.write("0 0")


# creation et génération instances
# liste_instances = generation_instances(9,10,7,2,2,7,"sud",10,5)
# ecriture_instances("instances_analyses_grille.txt",liste_instances)