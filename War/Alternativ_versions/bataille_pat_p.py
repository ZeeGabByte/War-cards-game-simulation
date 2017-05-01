from time import time as ti
from distribution import distribution as distribute
from numpy import mean, median


def bataille():
    paquet_base = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13,
                   1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    numbers_player = 2
    nombre_plis = 0
    jeux = distribute(paquet_base, numbers_player, [[], []])
    jeu_base = tuple(jeux)  # on récupère le jeu de départ pr les statistiques

    def redistribute(jeux, vainqueur, perdant, escarmoucheDepth):
        """ remet dans les paquet les cartes ganées à l'escarmouche"""
        for i1 in range(0, escarmoucheDepth+1):
            jeux[vainqueur].append(jeux[perdant][0])
            jeux[vainqueur].append(jeux[vainqueur][0])
            del jeux[vainqueur][0]
            del jeux[perdant][0]
        return jeux

    def escarmouche(jeux):
        """simule une escarmouche"""
        escarmoucheDepth = 0
        try:
            while jeux[0][escarmoucheDepth] == jeux[1][escarmoucheDepth]:
                escarmoucheDepth += 2
            if jeux[0][escarmoucheDepth] > jeux[1][escarmoucheDepth]:  # 0 gagne l'escarmouche
                jeux = redistribute(jeux, 0, 1, escarmoucheDepth)
            elif jeux[0][escarmoucheDepth] < jeux[1][escarmoucheDepth]:  # 1 gagne l'escarmouche
                jeux = redistribute(jeux, 1, 0, escarmoucheDepth)
        except IndexError:
            jeux = 0  # bataille à sec donc pat et stop
        return jeux

    while jeux != 0 and len(jeux[0]) > 0 and len(jeux[1]) > 0:  # fait des pli tant qu'il y a pas de gagnant
        nombre_plis += 1
        if jeux[0][0] > jeux[1][0]:    # 0 gagne le plis
            jeux[0].append(jeux[1][0])     # le gagnant récupère la carte du perdant
            jeux[0].append(jeux[0][0])     # le gagnat récupère la carte du gagnant
            del jeux[1][0]                 # puis on supprime la carte du perdant
            del jeux[0][0]                 # puis on supprime la carte du gagnant
        elif jeux[0][0] < jeux[1][0]:  # 1 gagne le plis
            jeux[1].append(jeux[0][0])     # le gagnant récupère la carte du perdant
            jeux[1].append(jeux[1][0])     # le gagnat récupère la carte du gagnant
            del jeux[0][0]                 # puis on supprime la carte du perdant
            del jeux[1][0]                 # puis on supprime la carte du gagnant
        else:
            jeux = escarmouche(jeux)
    if jeux != 0 and len(jeux[0]) > len(jeux[1]):  # 0 gagne la bataille
        return 1, nombre_plis, jeu_base
    elif jeux != 0 and len(jeux[0]) < len(jeux[1]):  # 1 gagne la bataille
        return 2, nombre_plis, jeu_base
    else:  # égalité
        return 3, nombre_plis, jeu_base


def affichage(result_full, nombre_bataille, t):
    """permet d'afficher les résultat et les statistiques"""
    nombre_pli_total = sum(result_full[1])
    print("=" * 60 + "\n")
    print("{nb_b} batailles simulées soit {nb_p} plis".format(nb_b=nombre_bataille, nb_p=nombre_pli_total))
    print("{v_b} bataille par seconde soit {v_p} plis par seconde".format(v_b=nombre_bataille / t,
                                                                          v_p=nombre_pli_total / t))

    print("\n" + "-" * 60 + "\n")

    print("Porcentage de résulats:\n    {v1} % de victoire de 1\n    {v2} % de victoire de 2\n     {eg} % d'égalité"
          .format(v1=result_full[0][0] / nombre_bataille * 100, v2=result_full[0][1] / nombre_bataille * 100,
                  eg=result_full[0][2] / nombre_bataille * 100))

    print("\n" + "-" * 60 + "\n")

    print("Statistiques:")
    print("    Nombre de plis maximum: {max}\n    Nombre de plis minimum: {min}\n    "
          "Nombre de plis moyen: {moy}\n    Nombre de plis median: {med}"
          .format(max=max(result_full[1]), min=min(result_full[1]), moy=mean(result_full[1]),
                  med=median(result_full[1])))

    print("\n" + "=" * 60)

result_full = [[0, 0, 0], [], []]
""""[victoire 1, victoire 2, égalité], [nombre de plis de chaque parties], [jeux de base]"""
nombre_bataille = int(input("Nombre de bataille à simuler: "))

t1 = ti()
for i in range(0, nombre_bataille):
    result_one = bataille()
    result_full[1].append(result_one[1])  # on récupère le nombre de pli de la bataille simulée
    result_full[2].append(result_one[2])  # on récupère les jeux de départ de la bataille simulée
    result_full[0][result_one[0]-1] += 1  # on récupère lerésultat de la bataille simulée
t = ti() - t1

affichage(result_full, nombre_bataille, t)
