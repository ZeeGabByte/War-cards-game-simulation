def affichage(result_full, nombre_bataille, durée=1):
    """permet d'afficher les résultat et les statistiques

    result_full = [victoire 1, victoire 2, égalité], [nombre de plis de chaque parties], [jeux de base] """
    from numpy import mean, median
    if durée == 0:
        durée = 1
    nombre_pli_total = sum(result_full[1])
    large = 80
    print("=" * large + "\n")
    print("{nb_b} batailles simulées soit {nb_p} plis".format(nb_b=nombre_bataille, nb_p=nombre_pli_total))
    print("{v_b} bataille par seconde soit {v_p} plis par seconde".format(v_b=round(nombre_bataille / durée, 9),
                                                                          v_p=round(nombre_pli_total / durée, 9)))

    print("\n" + "-" * large + "\n")

    print("Pourcentage de résulats:\n    {v1} % de victoire de 1\n    {v2} % de victoire de 2\n     "
          "{eg} % d'égalité\n     {tl} % de bataille de plus de 1 000 000 plis"
          .format(v1=round(result_full[0][0] / nombre_bataille * 100, 3),
                  v2=round(result_full[0][1] / nombre_bataille * 100, 3),
                  eg=round(result_full[0][2] / nombre_bataille * 100, 3),
                  tl=round(result_full[0][3] / nombre_bataille * 100, 3)))

    print("\n" + "-" * large + "\n")

    print("Statistiques:")
    print("    Nombre de plis maximum: {max}\n    Nombre de plis minimum: {min}\n    "
          "Nombre de plis moyen: {moy}\n    Nombre de plis median: {med}"
          .format(max=max(result_full[1]), min=min(result_full[1]), moy=round(mean(result_full[1]), 9),
                  med=int(median(result_full[1]))))

    print("\n" + "-" * large + "\n")

    print("Répartition: ")
    result_full[1].sort()
    ecart_décile = nombre_bataille / 10
    for n_decile in range(1, 10):
        print("    {num} décile: {décile}".
              format(num=n_decile, décile=result_full[1][int(ecart_décile*n_decile)]))

    print("\n" + "=" * large)


def axage(list_nb_pli, nb_bataille):
    value_nb_pli = []
    frenquence_nb_pli = []
    list_nb_pli.sort()
    value_nb_pli.append(list_nb_pli[0])
    frenquence_nb_pli.append(1)
    del list_nb_pli[0]
    for el in list_nb_pli:
        if el == value_nb_pli[len(value_nb_pli)-1]:
            try:
                frenquence_nb_pli[len(value_nb_pli)-1] += 1
            except IndexError:
                frenquence_nb_pli.append(1)
        else:
            value_nb_pli.append(el)
            frenquence_nb_pli.append(1)
    frenquence_nb_pli = [el/nb_bataille for el in frenquence_nb_pli]
    return value_nb_pli, frenquence_nb_pli


def graph(x, y):
    from matplotlib import pyplot as plt
    from matplotlib import style
    style.use('ggplot')
    plt.plot(x, y, color='r')
    plt.show()
