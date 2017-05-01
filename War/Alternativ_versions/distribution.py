def distribution(paquet, n_p, cibles=42):
    """ distribue les elemet de la liste paquet dans la liste de liste
    cibles contenant n_p list (si cibles n'est pas specifie il est cree)"""
    if cibles == 42:
        cibles = [[]]
        for j in range(n_p - 1):
            cibles.append([])
    if type(paquet) is not list:
        raise TypeError("paquet doit être une liste")
    if type(cibles) is not list:
        raise TypeError("cibles doit être une liste")
    if type(n_p) is not int:
        raise TypeError("n_p doit être un entier")

    from random import randrange as rr
    x = 0
    for i in range(0, len(paquet)):
        r = rr(0, len(paquet))
        if x >= n_p:
            x = 0
        cibles[x].append(paquet[r])
        del paquet[r]
        x += 1
    return cibles