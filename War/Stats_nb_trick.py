# -*-coding:utf8;-*-
# war_pat_p
from timeit import default_timer as timer
import sqlite3
from multiprocessing import Pool
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd
import Cython_War_Trick


def run(x, string):
    print("Processing chunk: {}".format(string))
    conn = sqlite3.connect(':memory:')
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

    chunk = pd.read_sql_query("""SELECT nb_trick FROM war""", conn)
    f = chunk['nb_trick'].value_counts()
    return f


if __name__ == '__main__':
    try:
        nbWarToSimulate = int(input("Number of wars to simulate: "))
    except ValueError:
        print("ValueError: you muss enter an integer!\nNumber of wars set to 100000.")
        nbWarToSimulate = 1000000

    pool = Pool(processes=8)

    nbWarToSimulate_per_run = nbWarToSimulate

    while nbWarToSimulate_per_run > 1000000:
        nbWarToSimulate_per_run //= 8

    nb_run = nbWarToSimulate // nbWarToSimulate_per_run

    print("Number of wars per run: {}".format(nbWarToSimulate_per_run))
    print("Number of runs: {}".format(nb_run))
    print()

    start = timer()

    map_args = []
    for name in range(nb_run):
        map_args.append((nbWarToSimulate_per_run, str(name + 1) + ' / ' + str(nb_run)))

    res = pool.starmap(run, map_args)

    frequency = pd.Series([0], index=[100])
    for freq in res:
        frequency = frequency.add(freq, fill_value=0)

    nb_war_total = sum(frequency.values)
    print("\nNumber of wars used: {}".format(nb_war_total))
    frequency = frequency.divide(nb_war_total)
    frequency = frequency.multiply(100)

    runtime = timer() - start

    # Print stats de ce run
    print('\n' + '-' * 66 + '\n')
    print("\t{} wars have been simulated:\n".format(nb_war_total))
    print("\tOperation took {} seconds.".format(runtime))
    print("\tNumber of wars per seconds: {} wars/s".format(nb_war_total / runtime))
    print('\n' + '-' * 66 + '\n')

    xs, ys = frequency.index, frequency.values
    print("Sum frequency: {}".format(sum(ys)))  # should be near 100

    ys_even = []
    ys_odd = []
    xs_even = []
    xs_odd = []

    for ii in range(len(xs)):
        if xs[ii] % 2 == 0:
            ys_even.append(ys[ii])
            xs_even.append(xs[ii])
        else:
            ys_odd.append(ys[ii])
            xs_odd.append(xs[ii])

    # display the graph
    style.use('ggplot')

    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    ax1.plot(xs_even, ys_even, 'b', label='even')
    ax1.plot(xs_odd, ys_odd, 'r', label='odd')
    ax1.set_xticks(list(range(0, int(max(xs)), 150)))

    plt.rc('legend', fontsize=20)
    plt.subplots_adjust(left=0.03, bottom=0.03, right=1.0, top=1.0, wspace=0.2, hspace=0)
    ax1.legend()

    print("\nFrom: Zee_GabByte & Zee_ImperoTemp")

    plt.show()
