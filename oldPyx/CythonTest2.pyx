#-*-coding:utf8;-*-
from timeit import default_timer as timer
import os
import numpy as np
cimport numpy as np
cimport cython


class Battle:
    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def __init__(self):
        cdef unsigned int nb_pli
        self.nb_pli = 0
        self.distribute()
        self.base_game = (list(self.player1), list(self.player2))

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def distribute(self):
        cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4,
                 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        np.random.shuffle(cards)
        self.player1 = cards[:26]
        self.player2 = cards[26:]

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def escarmouche(self):
        cdef unsigned int escarmoucheDepth
        self.escarmoucheDepth = 0
        try:
            while self.player1[self.escarmoucheDepth] == self.player2[self.escarmoucheDepth]:
                self.escarmoucheDepth += 2
            if self.player1[self.escarmoucheDepth] > self.player2[self.escarmoucheDepth]:
                redistribute(self.player1, self.player2, self.escarmoucheDepth)
            elif self.player2[self.escarmoucheDepth] > self.player1[self.escarmoucheDepth]:
                redistribute(self.player2, self.player1, self.escarmoucheDepth)
        except IndexError:
            self.player1 = []
            self.player2 = []

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def pli(self):
        while len(self.player1) != 0 and len(self.player2) != 0:
            self.nb_pli += 1
            if self.player2[0] > self.player1[0]:
                self.player2.append(self.player1[0])
                self.player2.append(self.player2[0])
                del(self.player1[0])
                del(self.player2[0])
            elif self.player1[0] > self.player2[0]:
                self.player1.append(self.player2[0])
                self.player1.append(self.player1[0])
                del(self.player1[0])
                del(self.player2[0])
            else:
                self.escarmouche()
        if len(self.player2) <= 0 < len(self.player1):
            return 1, self.nb_pli, self.base_game
        elif len(self.player1) <= 0 < len(self.player2):
            return 2, self.nb_pli, self.base_game
        elif len(self.player2) <= 0 and len(self.player1) <= 0:
            return 3, self.nb_pli, self.base_game


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def run(unsigned int x):
    np.random.seed()
    result = []
    for i in range(x):
        b = Battle()
        result.append(b.pli())
    return result


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def redistribute2(winner, looser, depth):
    winner += looser[:depth + 1] + winner[:depth + 1]
    del (winner[:depth + 1])
    del (looser[:depth + 1])


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def redistribute(winner, looser, depth):
    cdef unsigned int i
    for i in range(depth+1):
        winner.append(looser[0])
        winner.append(winner[0])
        del(winner[0])
        del(looser[0])


# @profile
# def redistribute2(winner, looser, depth):
#     winner.append(looser[:depth+1])
#     winner.append(winner[:depth+1])
#     del(winner[:depth+1])
#     del(looser[:depth+1])


def run_main():
    cdef unsigned int nbBattleToSimulate
    cdef unsigned int nb_victory_player1
    cdef unsigned int nb_victory_player2
    cdef unsigned int nb_equality

    try:
        nbBattleToSimulate = int(input("Number of battles to simulate: "))
    except ValueError:
        print("ValueError: you muss enter an integer!\nNumber of battles set to 100000.")
        nbBattleToSimulate = 100000

    start = timer()
    result = [run(nbBattleToSimulate)]
    runtime = timer() - start

    # Analyse des stats
    nb_pli = []
    victory = []
    for process in result:
        for war in process:
            nb_pli.append(war[1])
            victory.append(war[0])
    nb_victory_player1 = 0
    nb_victory_player2 = 0
    nb_equality = 0
    for final_result in victory:
        if final_result == 1:
            nb_victory_player1 += 1
        elif final_result == 2:
            nb_victory_player2 += 1
        elif final_result == 3:
            nb_equality += 1
    nb_pli_total = sum(nb_pli)
    min_pli = min(nb_pli)
    max_pli = max(nb_pli)
    average_pli = np.mean(nb_pli)
    median_pli = np.median(nb_pli)
    nb_battle = len(result) * len(result[0])

    # Affichage des stats
    print('\n' + '-' * 66 + '\n')
    print("\t{} battles have been simulated:\n".format(nb_battle))
    print("\tNumber of victory:")
    print("\t\t- Player 1: {}".format(nb_victory_player1))
    print("\t\t- Player 2: {}".format(nb_victory_player2))
    print("\tNumber of equality: {}\n".format(nb_equality))
    print("\tVictory rate player 1: {} %".format((nb_victory_player1 / nb_battle) * 100))
    print("\tVictory rate player 2: {} %".format((nb_victory_player2 / nb_battle) * 100))
    print("\tEquality rate: {} %\n".format((nb_equality / nb_battle) * 100))
    print("\tNumber of pli (Average): {}".format(average_pli))
    print("\tNumber of pli (Median): {}".format(median_pli))
    print("\tNumber of pli max: {}".format(max_pli))
    print("\tNumber of pli min: {}\n".format(min_pli))
    print("\tOperation took {} seconds.".format(runtime))
    print("\tNumber of battle per seconds: {} battles/s".format(nb_battle / runtime))
    print("\tNumber of pli per seconds: {} pli/s\n".format(nb_pli_total / runtime))
    print('-' * 66)
    print("\nFrom: Zee_GabByte & Zee_ImperoTemp")
    os.system("pause")


if __name__ == '__main__':
    run_main()
