from generation_instance import *
from resolution_instance import *
import time
import random
import matplotlib.pyplot as plt
generer = False
size=(20,20)
M,N=size
grille=np.zeros(size,dtype=np.int64)
if generer:
    # génération d'instances et ecriture dans le fichier d'intances
    liste_obstacle=[i for i in range(10,60,10)]
    liste_instances = []
    for obs_n in liste_obstacle:
        for _ in range(10):
            # N,M,d1,d2,f1,f2,o,nb_obstacles,nb_instances

            d1 = random.randint(0,M)
            d2 = random.randint(0,N)

            while True:
                f1 = random.randint(0,M)
                f2 = random.randint(0,N)

                if (f1, f2) != (d1,d2):
                    break

            o = random.choice(["nord","sud","est","ouest"])
            liste_instances.append(generation_instances(M,N,d1,d2,f1,f2,o,obs_n,1)[0])
            # print(f"{d1} {d2} {f1} {f2} {o}")

    ecriture_instances("instances_analyses_nb_obstacle.txt",liste_instances)




fichier = open("instances_analyses_nb_obstacle.txt","r")
liste_instances = lire_fichier(fichier)
nb_instances = len(liste_instances)
print(liste_instances[0])
print(nb_instances)

# résolution des instances

# résolution des instances
solutions = []
tableau_des_temps = []
liste_temps_tmp = []
for i in range(len(liste_instances)):
        ((M, N),matrice,(D1, D2, F1, F2, direction)) = liste_instances[i]
        graphe = generer_graphe(M,N,matrice)
        time_start = time.time()
        temps, commandes = plus_court_chemin(graphe,(D1, D2,direction),(F1, F2))
        time_end = time.time()
        liste_temps_tmp.append(time_end-time_start)
        if (i+1) % 10 == 0:
             tableau_des_temps.append(liste_temps_tmp)
             liste_temps_tmp = []
             
        # print(f"{temps} {" ".join(commandes)}")
        solutions.append((temps,commandes))


moyennes_ms = [np.mean(np.array(groupe) * 1000) for groupe in tableau_des_temps]

nb_obstacles = [10, 20, 30, 40, 50]

plt.figure(figsize=(8,5))
plt.plot(nb_obstacles, moyennes_ms, marker='o')

plt.title("Temps moyen de résolution sur 10 exemples en fonction du nombre d'obstacles")
plt.xlabel(r"nombre d'obstacles")
plt.ylabel("Temps moyen (ms)")
# plt.grid(True)
plt.tight_layout()
plt.show()


# ecriture des solution dans le fichier
autorisation_ecriture = True

if autorisation_ecriture:
    fichier_solutions = "solution_instances_analyse_obstacles.txt"
    ecrire_solutions(fichier_solutions,solutions)

