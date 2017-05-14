from time import time
from affichage_bataille import affichage
t = time()
from numpy import random


def distribute():
    """distribue les cartes"""
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
             0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    random.shuffle(cards)
    return cards[:26], cards[26:]


def redistribute(vainqueur, perdant, escarmouche_depth):
    """ remet dans les paquet les cartes ganées à l'escarmouche"""
    for i1 in range(0, escarmouche_depth + 1):  # toutes les cartes engagées dans l'escarmouche
        vainqueur.append(perdant[0])  # le vainqueur récupère la 1er carte du jeu du perdant
        vainqueur.append(vainqueur[0])  # le vainqueur récupère la 1er carte du jeu du gagnant
        del vainqueur[0]  # la 1ere carte du jeu du perdant est supprimé
        del perdant[0]  # la 1ere carte du jeu du perdant est supprimé
    return vainqueur, perdant


def escarmouche(player1, player2):
    """simule une escarmouche"""
    escarmouche_depth = 0
    try:
        while player1[escarmouche_depth] == player2[escarmouche_depth]:
            """tant que les cartes impaires sont égales on augmente l'escarmouche_depth"""
            escarmouche_depth += 2
        if player1[escarmouche_depth] > player2[escarmouche_depth]:  # 0 gagne l'escarmouche
            player1, player2 = redistribute(player1, player2, escarmouche_depth)
        elif player1[escarmouche_depth] < player2[escarmouche_depth]:  # 1 gagne l'escarmouche
            player2, player1 = redistribute(player2, player1, escarmouche_depth)
        return player1, player2, True
    except IndexError:
        return player1, player2, False  # bataille à sec donc pat et stop


def bataille_p():
    """simule une partie de bataille avec recuperation p"""


    nombre_plis = 0
    player1, player2 = distribute()
    jeu_p1_base = tuple(player1)  # on récupère le jeu de départ pr les statistiques
    jeu_p2_base = tuple(player2)
    go = True





    while go and len(player1) > 0 and len(player2) > 0:  # fait des plis tant qu'il y a pas de gagnant
        nombre_plis += 1
        if player1[0] > player2[0]:     # 0 gagne le plis
            player1.append(player2[0])     # le gagnant récupère la carte du perdant
            player1.append(player1[0])     # le gagnat récupère la carte du gagnant
            del player2[0]                 # puis on supprime la carte du perdant
            del player1[0]                 # puis on supprime la carte du gagnant
        elif player1[0] < player2[0]:   # 1 gagne le plis
            player2.append(player1[0])     # le gagnant récupère la carte du perdant
            player2.append(player2[0])     # le gagnat récupère la carte du gagnant
            del player1[0]                 # puis on supprime la carte du perdant
            del player2[0]                 # puis on supprime la carte du gagnant
        else:
            if nombre_plis < 1000000:
                player1, player2, go = escarmouche(player1, player2)
            else:  # la bataille est trop longue
                return 4, nombre_plis, (jeu_p1_base, jeu_p2_base)  # on renvoie 4
    if len(player1) > len(player2):    # 0 gagne la bataille
        return 1, nombre_plis, (jeu_p1_base, jeu_p2_base)   # on renvoie 1
    elif len(player1) < len(player2):  # 1 gagne la bataille
        return 2, nombre_plis, (jeu_p1_base, jeu_p2_base)  # on renvoie 2
    else:                              # égalité
        return 3, nombre_plis, (jeu_p1_base, jeu_p2_base)   # on renvoie 3

result_full = [[0, 0, 0, 0], [], []]
""""[victoire 1, victoire 2, égalité], [nombre de plis de chaque parties], [jeux de base]"""
exepetions = [[], []]  # [escarmouche ultime, bataille infinie ?]
# nombre_bataille = int(input("Nombre de bataille à simuler: "))
nombre_bataille = 1000000

for i in range(nombre_bataille):
    result_one = bataille_p()
    result_full[2].append(result_one[2])  # on récupère les jeux de départ de la bataille simulée
    result_full[1].append(result_one[1])  # on récupère le nombre de pli de la bataille simulée
    result_full[0][result_one[0] - 1] += 1  # on récupère lerésultat de la bataille simulée
    if result_one[0] == 3:
        exepetions[0].append(result_one[3])
    elif result_one[0] == 4:
        exepetions[1].append(result_one[3])
affichage(result_full, nombre_bataille, time() - t)
print(exepetions)
input()
