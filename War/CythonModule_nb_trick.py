# -*-coding:utf8;-*-
# war_pat_p
import numpy as np
cimport numpy as np
cimport cython


class Battle:
    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def __init__(self):
        cdef unsigned int nb_pli
        self.nb_trick = 0
        self.escarmoucheDepth = 0
        self.player1 = []
        self.player2 = []
        self.distribute()
        self.base_deck = (tuple(self.player1), tuple(self.player2))

    @cython.boundscheck(False)  # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    def distribute(self):
        deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4,
                5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        np.random.shuffle(deck)
        self.player1 = deck[:26]
        self.player2 = deck[26:]

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
    def trick(self):
        while self.player1 and self.player2 and self.nb_trick <= 10000:
            self.nb_trick += 1
            if self.player2[0] > self.player1[0]:
                self.player2.append(self.player1[0])
                self.player2.append(self.player2[0])
                del self.player1[0]
                del self.player2[0]
            elif self.player1[0] > self.player2[0]:
                self.player1.append(self.player2[0])
                self.player1.append(self.player1[0])
                del self.player1[0]
                del self.player2[0]
            else:
                self.escarmouche()
        if self.nb_trick > 10000:
            print("Infinite War?")
            print(self.base_deck)
            return -1
        elif len(self.player2) <= 0 < len(self.player1):
            return self.nb_trick
        elif len(self.player1) <= 0 < len(self.player2):
            return self.nb_trick
        elif len(self.player2) <= 0 and len(self.player1) <= 0:
            return self.nb_trick


@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def redistribute(winner, looser, depth):
    cdef unsigned int i
    for i in range(depth+1):
        winner.append(looser[0])
        winner.append(winner[0])
        del winner[0]
        del looser[0]
