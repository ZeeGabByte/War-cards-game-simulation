# -*-coding:utf8;-*-
from timeit import default_timer as timer
import numpy as np
from multiprocessing import Pool
import os
import sqlite3
import pandasDataAnalysis
# import cProfile


class Battle:
    def __init__(self):
        self.nb_pli = 0
        self.distribute()
        self.base_game = (list(self.player1), list(self.player2))

    def distribute(self):
        cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4,
                 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        np.random.shuffle(cards)
        self.player1 = cards[:26]
        self.player2 = cards[26:]

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
            return 1, self.nb_pli, list(self.base_game)
        elif len(self.player1) <= 0 < len(self.player2):
            return 2, self.nb_pli, list(self.base_game)
        elif len(self.player2) <= 0 and len(self.player1) <= 0:
            return 3, self.nb_pli, list(self.base_game)


def run(x):
    conn = sqlite3.connect('data.db', timeout=1000)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE war
                     (base_game_player1 list, base_game_player2 list, victory int, nb_pli int)''')
        conn.commit()
    except sqlite3.OperationalError:
        pass

    for i in range(x):
        b = Battle()
        result = b.pli()
        c.execute("INSERT INTO war VALUES (?, ?, ?, ?)", (np.array(result[2][0]), np.array(result[2][1]), result[0],
                                                          result[1]))
    conn.commit()
    conn.close()


def redistribute(winner, looser, depth):
    for i in range(depth+1):
        winner.append(looser[0])
        winner.append(winner[0])
        del(winner[0])
        del(looser[0])


if __name__ == '__main__':
    # try:
    #     nbBattleToSimulate = int(input("Number of battles to simulate: "))
    # except ValueError:
    #     print("ValueError: you muss enter an integer!\nNumber of battles set to 100000.")
    #     nbBattleToSimulate = 100000

    nbBattleToSimulate = 100000

    pool = Pool(8)
    start = timer()

    # cProfile.run('run({})'.format(nbBattleToSimulate))
    # run(nbBattleToSimulate)
    pool.map(run, [nbBattleToSimulate // 8] * 8)

    runtime = timer() - start

    # Print stats de ce run
    print('\n' + '-' * 66 + '\n')
    print("\t{} battles have been simulated:\n".format(nbBattleToSimulate // 8 * 8))
    print("\tOperation took {} seconds.".format(runtime))
    print("\tNumber of battle per seconds: {} battles/s".format(nbBattleToSimulate / runtime))
    print('\n' + '-' * 66 + '\n')

    # Analyse stats globales
    # conn = sqlite3.connect('data.db')
    # c = conn.cursor()
    #
    # try:
    #     c.execute('''CREATE TABLE war
    #                  (base_game_player1 list, base_game_player2 list, victory int, nb_pli int)''')
    #     conn.commit()
    # except sqlite3.OperationalError:
    #     pass
    #
    # c.execute("SELECT COUNT(victory) FROM war")
    # nb_battle = c.fetchone()[0]
    # c.execute("SELECT COUNT(victory) FROM war WHERE victory = 1")
    # nb_victory_player1 = c.fetchone()[0]
    # c.execute("SELECT COUNT(victory) FROM war WHERE victory = 2")
    # nb_victory_player2 = c.fetchone()[0]
    # c.execute("SELECT COUNT(victory) FROM war WHERE victory = 3")
    # nb_equality = c.fetchone()[0]
    # c.execute("SELECT SUM(nb_pli) FROM war")
    # nb_pli_total = c.fetchone()[0]
    # c.execute("SELECT AVG(nb_pli) FROM war")
    # average_pli = c.fetchone()[0]
    # c.execute("SELECT MAX(nb_pli) FROM war")
    # max_pli = c.fetchone()[0]
    # c.execute("SELECT MIN(nb_pli) FROM war")
    # min_pli = c.fetchone()[0]
    #
    # conn.close()
    #
    # # Print stats globales
    # print("\t{} battles in data:".format(nb_battle))
    # print("\t{} plis\n".format(nb_pli_total))
    # print("\tNumber of victory:")
    # print("\t\t- Player 1: {}".format(nb_victory_player1))
    # print("\t\t- Player 2: {}".format(nb_victory_player2))
    # print("\tNumber of equality: {}\n".format(nb_equality))
    # print("\tVictory rate player 1: {} %".format((nb_victory_player1 / nb_battle) * 100))
    # print("\tVictory rate player 2: {} %".format((nb_victory_player2 / nb_battle) * 100))
    # print("\tEquality rate: {} %\n".format((nb_equality / nb_battle) * 100))
    # print("\tNumber of pli (Average): {}".format(average_pli))
    # print("\tNumber of pli max: {}".format(max_pli))
    # print("\tNumber of pli min: {}\n".format(min_pli))
    # print('-' * 66)

    print(">>> reading...")
    df1 = pandasDataAnalysis.read_data_player1()
    df2 = pandasDataAnalysis.read_data_player2()
    print(df1.head(), df2.head())
    print(">>> describing...")
    print(df1.describe(), df2.describe())

    print("\nFrom: Zee_GabByte & Zee_ImperoTemp")
    os.system("pause")
