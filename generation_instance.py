# fichier permettant de générer les instances pour les analyses 
# de temps de calcul de l'algorithme
import numpy as np
import random
import os
# fonction permettant de générer àléatoirement nb_instances
# instances en version naive
def generation_instances(M,N,d1,d2,f1,f2,o,nb_obstacles,nb_instances):

    instances = []
    for _ in range(nb_instances):
        matrice = np.zeros((M,N),dtype=int)
        cases_possibles = [(i,j) for i in range(M) for j in range(N) if (i,j) not in [(d1,d2),(f1,f2)]]
        nb_obstacles = min(nb_obstacles,len(cases_possibles))
        obstacles = random.sample(cases_possibles, nb_obstacles)

        for (i,j) in obstacles:
            matrice[i,j] = 1

        instances.append(((M,N),matrice,(d1,d2,f1,f2,o)))

    return instances

# fonction permettant d'écrire les différentes intances dans un fichier 
# soit qui existe deja, soit qu'il va creer
def ecriture_instances(fichier,liste_instances):
    with open(fichier,"w") as f:
        for ((M,N),matrice,(d1,d2,f1,f2,o)) in liste_instances:
            f.write(f"{M} {N}\n")

            for i in range(M):
                ligne_mat = " ".join(str(x) for x in matrice[i])
                f.write(ligne_mat + "\n")

            f.write(f"{d1} {d2} {f1} {f2} {o}\n")

        f.write("0 0")


# creation et génération instances
# liste_instances = generation_instances(9,10,7,2,2,7,"sud",10,5)
# ecriture_instances("instances_analyses_grille.txt",liste_instances)

# lecture des instances
def lire_fichier(file):
        
        liste_instances = []
        """Lit plusieurs instances, s'arrête à '0 0'"""
        lines = [l.strip() for l in file.readlines() if l.strip() != ""]
        i = 0
        n = len(lines)

        while i < n:

            # Lecture M N
            M, N = map(int, lines[i].split())

            # Condition de fin
            if M == 0 and N == 0:
                break

            i += 1

            # Lecture matrice
            matrice = []

            for _ in range(M):
                row = list(map(int, lines[i].split()))

                if len(row) != N:
                    raise ValueError(f"Ligne matrice incorrecte : {lines[i]}")
                matrice.append(row)
                i += 1

            matrice = np.array(matrice)

            # Lecture paramètres
            parts = lines[i].split()
            if len(parts) != 5:
                raise ValueError("Paramètres D1 D2 F1 F2 direction incorrects")

            D1, D2, F1, F2 = map(int, parts[:4])
            direction = parts[4]
            i += 1
            
            liste_instances.append(((M,N),matrice,(D1, D2, F1, F2, direction)))

        return liste_instances

def ecrire_solutions(fichier,liste_solutions):
    with open(fichier,"w") as f:
        for (temps,commandes) in liste_solutions:
            f.write(f"{temps} {" ".join(commandes)}\n")
            f.write("\n")
    