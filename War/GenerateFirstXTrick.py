# -*-coding:utf8;-*-
# war_pat_p


class Battle:
    def __init__(self, player1, player2, limit_trick):
        self.nb_trick = 0
        self.limit_trick = limit_trick
        self.escarmoucheDepth = 0
        self.player1 = list(player1)
        self.player2 = list(player2)

    def escarmouche(self):
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

    def trick(self):
        while len(self.player1) != 0 and len(self.player2) != 0 and self.nb_trick < self.limit_trick:
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
        if self.nb_trick == self.limit_trick:
            if model1(self.player2) < model1(self.player1):
                return 1
            elif model1(self.player1) < model1(self.player2):
                return 2
            elif model1(self.player1) == model1(self.player2):
                return 3
        elif len(self.player2) <= 0 < len(self.player1):
            return 1
        elif len(self.player1) <= 0 < len(self.player2):
            return 2
        else:
            print("equality2")
            return 3


def redistribute(winner, looser, depth):
    for i in range(depth+1):
        winner.append(looser[0])
        winner.append(winner[0])
        del winner[0]
        del looser[0]


def model1(player_deck):
    ret = []
    for i in player_deck:
        ret.append(i ** i)
    return sum(ret)
