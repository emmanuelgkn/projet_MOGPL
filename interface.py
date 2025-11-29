from generation_instance_pl import *
from resolution_instance import *

if __name__ == "__main__":

    M = int(input("Veuillez saisir le nombre de ligne: "))
    print(" ")
    N = int(input("Veuillez saisir le nombre de colonnes: "))
    print(" ")
    P = int(input("Veuillez le nombre d'obstacles: "))
    print(" ")
    
    print("generation du terrain ...")
    _, mat = generer_grille_lp(M, N, P, seed=None)

    print(" ")

    D1 = int(input("ligne d'origine: "))
    print(" ")

    D2 = int(input("colonne d'origine: "))
    print(" ")

    O = str(input("orientation d'origine: "))
    print(" ")

    F1 = int(input("ligne d'arrivee: "))
    print(" ")

    F2 = int(input("colonne d'arrivee: "))
    print(" ")



    graphe = generer_graphe(M,N,mat)

    etat_initial = (D1,D2,O)
    position_cible = (F1,F2)

    temps, commandes = plus_court_chemin(graphe,etat_initial,position_cible)

    print(" ")
    print("Voici le chemin optimal: ")
    print(f"{temps} {" ".join(commandes)}")