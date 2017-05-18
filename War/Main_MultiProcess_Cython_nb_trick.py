# -*-coding:utf8;-*-
# war_pat_p
from timeit import default_timer as timer
# import numpy as np
import os
import sqlite3
from multiprocessing import Pool
import Cython_War_Trick
# import pandasDataAnalysis
# import cProfile


def run(x, nb):
    conn = sqlite3.connect(r'D:\data\nb_trick\data_trick{}.db'.format(nb))
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE war (nb_trick int)""")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    for i in range(x):
        b = Cython_War_Trick.Battle()
        result = b.trick()
        c.execute("""INSERT INTO war VALUES (?)""", [result])
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
    # set this security to the number of threads of tour processor
    if nb_processes > 8:
        nb_processes = 1

    pool = Pool(processes=nb_processes)

    nbBattleToSimulate_per_process = nbBattleToSimulate // nb_processes

    start = timer()

    map_args = []
    for name in range(nb_processes):
        map_args.append((nbBattleToSimulate_per_process, name))

    pool.starmap(run, map_args)

    runtime = timer() - start

    # Print stats de ce run
    print('\n' + '-' * 66 + '\n')
    print("\t{} wars have been simulated:\n".format(nbBattleToSimulate // nb_processes * nb_processes))
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
