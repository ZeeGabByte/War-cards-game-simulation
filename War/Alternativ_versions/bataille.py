from numpy import random
from random import randrange


def distribute_13():
    """distribue les cartes"""
    cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
             0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    random.shuffle(cards)
    return cards[:26], cards[26:]


def distribute_n(n):
    """distribue les cartes avec n"""
    cards = list(range(0, n)) * 4
    random.shuffle(cards)
    return cards[:2 * n], cards[2 * n:]


def redistribute_v(vainqueur, perdant, escarmouche_depth):
    """ remet dans les paquet les cartes ganées à l'escarmouche"""
    for i1 in range(0, escarmouche_depth+1):  # toutes les cartes engagées dans l'escarmouche
        vainqueur.append(vainqueur[0])        # le vainqueur récupère la 1er carte du jeu du gagnant
        vainqueur.append(perdant[0])          # le vainqueur récupère la 1er carte du jeu du perdant
        del vainqueur[0]                      # la 1ere carte du jeu du perdant est supprimé
        del perdant[0]                        # la 1ere carte du jeu du perdant est supprimé
    return vainqueur, perdant


def redistribute_p(vainqueur, perdant, escarmouche_depth):
    """ remet dans les paquet les cartes ganées à l'escarmouche"""
    for i1 in range(0, escarmouche_depth+1):  # toutes les cartes engagées dans l'escarmouche
        vainqueur.append(perdant[0])          # le vainqueur récupère la 1er carte du jeu du perdant
        vainqueur.append(vainqueur[0])  # le vainqueur récupère la 1er carte du jeu du gagnant
        del vainqueur[0]                      # la 1ere carte du jeu du perdant est supprimé
        del perdant[0]                        # la 1ere carte du jeu du perdant est supprimé
    return vainqueur, perdant


def escarmouche_pat(player1, player2, redistribute):
    """simule une escarmouche"""
    escarmouche_depth = 0
    try:
        while player1[escarmouche_depth] == player2[escarmouche_depth]:
            """tant que les cartes impaires sont égales on augmente l'escarmouche_depth"""
            escarmouche_depth += 2
        if player1[escarmouche_depth] > player2[escarmouche_depth]:    # 0 gagne l'escarmouche
            player1, player2 = redistribute(player1, player2, escarmouche_depth)
        elif player1[escarmouche_depth] < player2[escarmouche_depth]:  # 1 gagne l'escarmouche
            player2, player1 = redistribute(player2, player1, escarmouche_depth)
        return player1, player2, True
    except IndexError:
        return player1, player2, False  # bataille à sec donc pat et stop


def escarmouche_tirage(player1, player2, redistribute):
    """simule une escarmouche"""
    escarmouche_depth = 0
    try:
        while player1[escarmouche_depth] == player2[escarmouche_depth]:
            """tant que les cartes impaires sont égales  on augmente l'escarmouche_depth"""
            escarmouche_depth += 2
        if player1[escarmouche_depth] > player2[escarmouche_depth]:    # 0 gagne l'escarmouche
            player1, player2 = redistribute(player1, player2, escarmouche_depth)
        elif player1[escarmouche_depth] < player2[escarmouche_depth]:  # 1 gagne l'escarmouche
            player2, player1 = redistribute(player1, player2, escarmouche_depth)
        return player1, player2, True
    except IndexError:
        return tirage(player1, player2, redistribute)  # bataille à sec donc tirage pour pouvoir continuer


def tirage(player1, player2, redistribute):
    """tire du plus long vers le plus court 1 fois"""
    if len(player1) > len(player2):  # on doit tirer du jeu du 0 vers le 1
        aleatoir = randrange(len(player2)-1, len(player1))
        """choisi un nombre aleatoire corespondant à l'indice d'une carte
                qui ne soit pas engager dans l'escarmouche donc un indice supérieur à la longueur du jeu de 1 """
        player2.append(player1[aleatoir])  # le joeur 1 récupère la carte d'incide aleatoir du joueur 0
        del player1[aleatoir]  # la carte d'indice aleatoir est supprimé du jeu du joueur 0
        return escarmouche_tirage(player1, player2, redistribute)
        # semi recursivité : rappelle la f° escarmouche avec le nv jeux
    elif len(player1) < len(player2):  # on doit tirer du jeu du 1 vers le 0
        aleatoir = randrange(len(player1)-1, len(player2))
        """choisi un nombre aleatoire corespondant à l'indice d'une carte
                qui ne soit pas engager dans l'escarmouche donc un indice supérieur à la longueur du jeu de 0 """
        player1.append(player2[aleatoir])  # le joeur 0 récupère la carte d'incide aleatoir du joueur 1
        del player2[aleatoir]  # la carte d'indice aleatoir est supprimé du jeu du joueur 1
        return escarmouche_tirage(player1, player2, redistribute)
        # semi recursivité : rappelle la f° escarmouche avec le nv jeux
    else:  # si ils font la même taille alors bataille ultime
        return player1, player2, False  # arrête la boucle principale while


def bataille_v(player1, player2, escarmouche):
    """simule une partie de bataille avec recuperation v"""
    nombre_plis = 0
    go = True
    while go and player1 and player2 and nombre_plis < 1000000:  # fait des plis tant qu'il y a pas de gagnant
        nombre_plis += 1
        if player1[0] > player2[0]:    # 0 gagne le plis
            player1.append(player1[0])     # le gagnat récupère la carte du gagnant
            player1.append(player2[0])     # le gagnant récupère la carte du perdant
            del player2[0]                 # puis on supprime la carte du perdant
            del player1[0]                 # puis on supprime la carte du gagnant
        elif player1[0] < player2[0]:  # 1 gagne le plis
            player2.append(player2[0])     # le gagnat récupère la carte du gagnant
            player2.append(player1[0])     # le gagnant récupère la carte du perdant
            del player1[0]                 # puis on supprime la carte du perdant
            del player2[0]                 # puis on supprime la carte du gagnant
        else:
            player1, player2, go = escarmouche(player1, player2, redistribute_v)
    if nombre_plis > 1000000:  # la bataille est trop longue
        return 4, nombre_plis  # on renvoie 4
    elif len(player1) > len(player2):        # 0 gagne la bataille
        return 1, nombre_plis    # on renvoie 1
    elif len(player1) < len(player2):      # 1 gagne la bataille
        return 2, nombre_plis    # on renvoie 2
    else:                                  # égalité
        return 3, nombre_plis    # on renvoie 3


def bataille_p(player1, player2, escarmouche):
    """simule une partie de bataille avec recuperation p"""
    nombre_plis = 0
    go = True
    while go and player1 and player2 and nombre_plis < 1000000:  # fait des plis tant qu'il y a pas de gagnant
        nombre_plis += 1
        if player1[0] > player2[0]:     # 0 gagne le plis
            player1.append(player2[0])     # le gagnant récupère la carte du perdant
            player1.append(player1[0])  # le gagnat récupère la carte du gagnant
            del player2[0]                 # puis on supprime la carte du perdant
            del player1[0]                 # puis on supprime la carte du gagnant
        elif player1[0] < player2[0]:   # 1 gagne le plis
            player2.append(player1[0])     # le gagnant récupère la carte du perdant
            player2.append(player2[0])  # le gagnat récupère la carte du gagnant
            del player1[0]                 # puis on supprime la carte du perdant
            del player2[0]                 # puis on supprime la carte du gagnant
        else:
                player1, player2, go = escarmouche(player1, player2, redistribute_p)
    if nombre_plis > 1000000:  # la bataille est trop longue
        return 4, nombre_plis  # on renvoie 4
    elif len(player1) > len(player2):    # 0 gagne la bataille
        return 1, nombre_plis    # on renvoie 1
    elif len(player1) < len(player2):  # 1 gagne la bataille
        return 2, nombre_plis    # on renvoie 2
    else:                              # égalité
        return 3, nombre_plis    # on renvoie 3


def bataille_mix(player1, player2):
    """simule une partie de bataille avec recuperation p"""
    if not isinstance(player1, list):
        raise TypeError("player1 muss be a list ")
    if not isinstance(player2, list):
        raise TypeError("player2 muss be a list ")
    nombre_plis = 0
    go = True
    while go and player1 and player2 and nombre_plis < 1000000:  # fait des plis tant qu'il y a pas de gagnant
        nombre_plis += 1
        if player1[0] > player2[0]:     # 0 gagne le plis
            player1.append(player1[0])     # le gagnant récupère la carte du gagnant
            player1.append(player2[0])     # le gagnant récupère la carte du perdant
            del player2[0]                 # puis on supprime la carte du perdant
            del player1[0]                 # puis on supprime la carte du gagnant
        elif player1[0] < player2[0]:   # 1 gagne le plis
            player2.append(player1[0])     # le gagnant récupère la carte du perdant
            player2.append(player2[0])     # le gagnat récupère la carte du gagnant
            del player1[0]                 # puis on supprime la carte du perdant
            del player2[0]                 # puis on supprime la carte du gagnant
        else:
            player1, player2, go = escarmouche_pat_mix(player1, player2)
    if nombre_plis > 1000000:  # la bataille est trop longue
        return 4, nombre_plis  # on renvoie 4
    elif len(player1) > len(player2):    # 0 gagne la bataille
        return 1, nombre_plis    # on renvoie 1
    elif len(player1) < len(player2):  # 1 gagne la bataille
        return 2, nombre_plis    # on renvoie 2
    else:                              # égalité
        return 3, nombre_plis    # on renvoie 3


def escarmouche_pat_mix(player1, player2):
    """simule une escarmouche"""
    escarmouche_depth = 0
    try:
        while player1[escarmouche_depth] == player2[escarmouche_depth]:
            """tant que les cartes d'indexs impairs sont égales on augmente l'escarmouche_depth"""
            escarmouche_depth += 2
        if player1[escarmouche_depth] > player2[escarmouche_depth]:    # 0 gagne l'escarmouche
            player1, player2 = redistribute_v(player1, player2, escarmouche_depth)
        elif player1[escarmouche_depth] < player2[escarmouche_depth]:  # 1 gagne l'escarmouche
            player2, player1 = redistribute_p(player2, player1, escarmouche_depth)
        return player1, player2, True
    except IndexError:
        return player1, player2, False  # bataille à sec donc pat et stop


def bataille_mix_period(player1, player2):
    """simule une partie de bataille avec recuperation p"""
    if not isinstance(player1, list):
        raise TypeError("player1 muss be a list ")
    if not isinstance(player2, list):
        raise TypeError("player2 muss be a list ")
    x = []
    y1 = []
    y2 = []
    nombre_plis = 0
    go = True
    while go and player1 and player2 and nombre_plis < 1000000:  # fait des plis tant qu'il y a pas de gagnant
        y1.append(len(player1))
        y2.append(len(player2))
        x.append(nombre_plis)
        if player1[0] > player2[0]:     # 0 gagne le plis
            player1.append(player1[0])    # le gagnant récupère la carte du gagnant
            player1.append(player2[0])     # le gagnant récupère la carte du perdant
            del player2[0]                 # puis on supprime la carte du perdant
            del player1[0]                 # puis on supprime la carte du gagnant
        elif player1[0] < player2[0]:   # 1 gagne le plis
            player2.append(player1[0])     # le gagnant récupère la carte du perdant
            player2.append(player2[0])     # le gagnat récupère la carte du gagnant
            del player1[0]                 # puis on supprime la carte du perdant
            del player2[0]                 # puis on supprime la carte du gagnant
        else:
            player1, player2, go = escarmouche_pat_mix(player1, player2)
        nombre_plis += 1
    return x, y1, y2
