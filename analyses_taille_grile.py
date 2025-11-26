from generation_instance import *
import random


# génération d'instances et ecriture dans le fichier d'intances
liste_tailles = [(i,i) for i in range(10,60,10)]

liste_instances = []
for (N,M) in liste_tailles:
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

# lecture et résolution des instances avec prélevement des temps de
# résolution