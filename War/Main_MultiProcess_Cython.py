# -*-coding:utf8;-*-
# war_pat_p
from timeit import default_timer as timer
import numpy as np
import os
import sqlite3
import pickle
from multiprocessing import Pool
import Cython_War
# import pandasDataAnalysis
# import cProfile


def run(x, nb):
    conn = sqlite3.connect('data\data{}.db'.format(nb))
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE war
                     (base_deck_player1 list, base_deck_player2 list, victory int, nb_trick int)""")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    np.random.seed()

    for i in range(x):
        b = Cython_War.Battle()
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

    try:
        nb_processes = int(input("Number of processes: "))
    except ValueError:
        print("ValueError: you muss enter an integer!\nNumber of processes set to 1.")
        nb_processes = 1
    # delete this security if you have more then 8 threads or set 8 to the number of threads you have
    if nb_processes > 8:
        nb_processes = 1

    pool = Pool(processes=nb_processes)

    nbBattleToSimulate_per_process = nbBattleToSimulate // nb_processes

    start = timer()

    # cProfile.run('run({})'.format(nbBattleToSimulate))
    pool.starmap(run, [(nbBattleToSimulate_per_process, 0), (nbBattleToSimulate_per_process, 1),
                       (nbBattleToSimulate_per_process, 2), (nbBattleToSimulate_per_process, 3),
                       (nbBattleToSimulate_per_process, 4), (nbBattleToSimulate_per_process, 5),
                       (nbBattleToSimulate_per_process, 6), (nbBattleToSimulate_per_process, 7)])
    # run(nbBattleToSimulate)

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
