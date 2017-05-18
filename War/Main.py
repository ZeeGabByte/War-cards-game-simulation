# -*-coding:utf8;-*-
# war_pat_p
from timeit import default_timer as timer
import numpy as np
import os
import sqlite3
import pickle
# import pandasDataAnalysis
# import cProfile


class Battle:
    def __init__(self):
        self.nb_trick = 0
        self.escarmoucheDepth = 0
        self.player1 = []
        self.player2 = []
        self.distribute()
        self.base_deck = (tuple(self.player1), tuple(self.player2))

    def distribute(self):
        deck = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4,
                5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        np.random.shuffle(deck)
        self.player1 = deck[:26]
        self.player2 = deck[26:]

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
        while self.player1 and self.player2:
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
            return 4, self.nb_trick, tuple(self.base_deck)
        elif len(self.player2) <= 0 < len(self.player1):
            return 1, self.nb_trick, tuple(self.base_deck)
        elif len(self.player1) <= 0 < len(self.player2):
            return 2, self.nb_trick, tuple(self.base_deck)
        elif len(self.player2) <= 0 and len(self.player1) <= 0:
            return 3, self.nb_trick, tuple(self.base_deck)


def redistribute(winner, looser, depth):
    for i in range(depth+1):
        winner.append(looser[0])
        winner.append(winner[0])
        del winner[0]
        del looser[0]


def run(x):
    conn = sqlite3.connect('D:\data\data0.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE war
                     (base_deck_player1 list, base_deck_player2 list, victory int, nb_trick int)""")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    for i in range(x):
        b = Battle()
        result = b.trick()
        c.execute("""INSERT INTO war VALUES (?, ?, ?, ?)""", (pickle.dumps(result[2][0]),
                                                              pickle.dumps(result[2][1]), result[0], result[1]))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    try:
        nbBattleToSimulate = int(input("Number of wars to simulate: "))
    except ValueError:
        print("ValueError: you muss enter an integer!\nNumber of wars set to 100000.")
        nbBattleToSimulate = 100000

    start = timer()

    # cProfile.run('run({})'.format(nbBattleToSimulate))
    run(nbBattleToSimulate)

    runtime = timer() - start

    # Print stats de ce run
    print('\n' + '-' * 66 + '\n')
    print("\t{} wars have been simulated:\n".format(nbBattleToSimulate // 8 * 8))
    print("\tOperation took {} seconds.".format(runtime))
    print("\tNumber of battle per seconds: {} wars/s".format(nbBattleToSimulate / runtime))
    print('\n' + '-' * 66 + '\n')

    # # display global stats
    # print(">>> reading...")
    # df1 = pandasDataAnalysis.read_data_player1()
    # df2 = pandasDataAnalysis.read_data_player2()
    # print(df1.head(), df2.head())
    # print(">>> describing...")
    # print(df1.describe(), df2.describe())

    print("\nFrom: Zee_GabByte & Zee_ImperoTemp")
    os.system("pause")
