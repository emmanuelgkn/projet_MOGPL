from collections import defaultdict

ORIENTATIONS = ["N","E","S","O"]

# dictionnaire des indentifiants lié aux orientations (0,1,2,4)
ID_ORIENTATIONS = {d: i for i,d in enumerate(ORIENTATIONS)}
# dictionnaire montrant les déplacements élémentaires 
# des différentes orientations 
DEPLAS = {
    "N": (-1,0),
    "S": (1,0),
    "E": (0,1),
    "O":(0,-1),
}

# fonction qui a partir d'une orientation "o"
# donne l'orientation quand on tourne à gauche
def tourne_gauche(o):
    ido = ID_ORIENTATIONS[o]
    return ORIENTATIONS[(ido - 1)%4]

# fonction qui a partir d'une orientation "o"
# donne l'orientation quand on tourne à droite
def tourne_droite(o):
    ido = ID_ORIENTATIONS[o]
    return ORIENTATIONS[(ido + 1)%4]

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
    di,dj = DEPLAS[o]
    i_act = i
    j_act = j

    for _ in range(n):
        i2 = i_act + di 
        j2 = i_act + dj 

        if not (0 <= i2 <= N) and (0 <= j2 <= M):
            return False, None
        
        if not valide[i2][j2]:
            return False, None
        
        i2, j2 = i_act, j_act 

    return True, (i2, j2)
    
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

                o_gauche = tourne_gauche(o)
                o_droite = tourne_droite(o)
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

# tests
M, N = 3, 3
obstacles = [[0,0,0],
             [0,0,0],
             [0,1,0]]
graph = generer_graphe(N,M,obstacles)

etat = (3,3,"E")

print(f"transitions depuis {etat} :")
for nxt, cmd in graph[etat]:
    print(f" {cmd} -> {nxt}")