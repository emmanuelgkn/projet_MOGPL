from collections import defaultdict, deque

ORIENTATIONS = ["nord","est","sud","ouest"]

# dictionnaire des indentifiants lié aux orientations (0,1,2,4)
ID_ORIENTATIONS = {d: i for i,d in enumerate(ORIENTATIONS)}

# dictionnaire montrant les déplacements élémentaires 
# des différentes orientations 
DEPLA = {
    "nord": (-1,0),
    "sud": (1,0),
    "est": (0,1),
    "ouest":(0,-1),
}

# fonction qui a partir d'une orientation "o"
# donne l'orientation quand on tourne à dir = (gauche | droite)
def tourne(o,dir):
    ido = ID_ORIENTATIONS[o]
    if dir == "gauche":
        return ORIENTATIONS[(ido - 1)%4]
    elif dir == "droite":
        return ORIENTATIONS[(ido + 1)%4]
    else:
        print("direction incorrecte")

# fonction qui retourne les croisements 
# accecible par le robot dans la grille
# avec la matrice obtacles correspondant
# aux cases de la grille 
def croisements_valides(N, M, obstacles):
    valide = [[True for _ in range(M+1)] for _ in range(N+1)]

    for i in range(N+1):
        for j in range(M+1):
            for r in (i-1,i):
                for c in (j-1,j):
                    if (0 <= r < N) and (0 <= c < M):
                        if obstacles[r][c] == 1:
                            valide[i][j] = False
    return valide

# fonction qui test si un robot en "i,j" 
# peut bouger d'une distance "n" dans une 
# grille de dimention "N, M" avec une orientation "o"
# tout en tenant compte de la matrice des croisements
# valides "valide"
def peut_bouger(i,j,o,n,N,M,valide):
    di,dj = DEPLA[o]
    i_act = i
    j_act = j

    for _ in range(n):
        i2 = i_act + di 
        j2 = j_act + dj 

        if not ((0 <= i2 <= N) and (0 <= j2 <= M)):
            return False, None
        
        if not valide[i2][j2]:
            return False, None
        
        i_act, j_act = i2, j2 

    return True, (i_act, j_act)
    
# fonction permettant de générer un graphe
# représentant la grille de taille N * M
# avec la matrice obstacles correspondant
# aux cases de la grille 
def generer_graphe(N,M,obstacles):
    graphe = defaultdict(list)

    valide = croisements_valides(N,M,obstacles)

    for i in range(N+1):
        for j in range(M+1):

            if not valide[i][j]:
                continue

            for o in ORIENTATIONS:
                etat = (i,j,o)

                o_gauche = tourne(o,"gauche")
                o_droite = tourne(o,"droite")
                graphe[etat].append(((i,j,o_gauche), "G"))
                graphe[etat].append(((i,j,o_droite), "D"))

                for n in [1,2,3]:
                    ok, coord = peut_bouger(i,j,o,n,N,M,valide)
                    if ok:
                        (i2,j2) = coord
                        prochain_etat = (i2,j2,o)
                        commande = f"a{n}"
                        graphe[etat].append((prochain_etat,commande))

    return graphe

# Tests 1
# M, N = 3, 3
# obstacles = [[0,0,0],
#              [0,0,0],
#              [0,1,0]]
# graph = generer_graphe(N,M,obstacles)

# etat = (0,0,"est")

# print(f"transitions depuis {etat} :")
# for nxt, cmd in graph[etat]:
#     print(f" {cmd} -> {nxt}")

# fonction permettant d'effectuer un parcours en largeur de 
# notre graphe pour trouver le plus court chemin
def plus_court_chemin(graphe,etat_initial,cible_position):

    file = deque()
    file.append(etat_initial)

    parents = {etat_initial: (None,None)}

    etat_final = None

    i0, j0, _ = etat_initial

    if (i0,j0) == cible_position:
        return 0, []
    
    while file != deque():
        etat = file.popleft()
        i, j, _ = etat

        if (i, j) == cible_position:
            etat_final = etat
            break

        for etat_suiv, cmd in graphe[etat]:
            if etat_suiv not in parents:
                parents[etat_suiv] = (etat,cmd)
                file.append(etat_suiv)        
    
    if etat_final is None:
        return -1, []
    
    commandes = []
    actuel = etat_final

    while True: 

        prev,cmd = parents[actuel]

        if prev is None:
            break

        actuel = prev

        commandes.append(cmd)
    
    commandes.reverse()
    temps = len(commandes)

    return temps, commandes


# tests 2
# N, M = 9, 10
# obstacles = [[0,0,0,0,0,0,1,0,0,0],
#              [0,0,0,0,0,0,0,0,1,0],
#              [0,0,0,1,0,0,0,0,0,0],
#              [0,0,1,0,0,0,0,0,0,0],
#              [0,0,0,0,0,0,1,0,0,0],
#              [0,0,0,0,0,1,0,0,0,0],
#              [0,0,0,1,1,0,0,0,0,0],
#              [0,0,0,0,0,0,0,0,0,0],
#              [1,0,0,0,0,0,0,0,1,0]]



# graphe = generer_graphe(N,M,obstacles)

# etat_initial = (7,2,"sud")

# position_cible = (2,7)

# temps, commandes = plus_court_chemin(graphe,etat_initial,position_cible)

# if temps == -1:
#     print("Aucun chemin")
#     print(f"temps : {temps}")
#     print(f"commandes: {commandes}")
# else:
#     print(f"temps: {temps}")
#     print(f"commandes: {" ".join(commandes)}")