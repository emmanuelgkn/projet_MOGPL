from generation_instance import *
from resolution_instance import *
import random
import time
import matplotlib.pyplot as plt

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
solutions = []
tableau_des_temps = []
liste_temps_tmp = []
for i in range(len(liste_instances)):
        ((N, M),matrice,(D1, D2, F1, F2, direction)) = liste_instances[i]
        graphe = generer_graphe(N,M,matrice)
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

tailles_instances = [10, 20, 30, 40, 50]

plt.figure(figsize=(8,5))
plt.plot(tailles_instances, moyennes_ms, marker='o')

plt.title("Temps moyen de résolution sur 10 exemples en fonction de la taille des instances")
plt.xlabel(r"Taille d'instance $N \times N$")
plt.ylabel("Temps moyen (ms)")
# plt.grid(True)
plt.tight_layout()
plt.show()


# ecriture des solution dans le fichier
autorisation_ecriture = False

if autorisation_ecriture:
    fichier_solutions = "solution_instances_analyse_grille.txt"
    ecrire_solutions(fichier_solutions,solutions)


