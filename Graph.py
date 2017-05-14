# -*-coding:utf8;-*-
import sqlite3
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from timeit import default_timer as timer


def create_stats_from_sql_with_pd():
    conn = sqlite3.connect('D:\data\data_merged.db')
    n = 0
    chunk_size = 10000000

    x_values = [0]
    y_values = [0]
    # http://code.activestate.com/recipes/137270-use-generators-for-fetching-large-db-record-sets/
    for chunk in pd.read_sql_query("""SELECT nb_trick FROM war""", conn, chunksize=chunk_size):
        print("Processing chunk: {}".format(n))
        n += 1

        list_nb_trick = list(chunk['nb_trick'])
        bins = list(set(list_nb_trick))
        bins.append(bins[-1] + 1)
        histogram = np.histogram(list_nb_trick, bins=bins)

        xs_new = list(histogram[1][:-1])
        ys_new = list(histogram[0])

        x_values_future = list(set(xs_new + x_values))
        ys_temporary = []

        for i in x_values_future:
            buffer = 0
            if i in xs_new:
                index = xs_new.index(i)
                buffer += ys_new[index]
            if i in x_values:
                index = x_values.index(i)
                buffer += y_values[index]
            ys_temporary.append(buffer)

        x_values = x_values_future
        y_values = ys_temporary

    nb_war_total = sum(y_values)

    print("\nNumber of wars used: {}".format(nb_war_total))

    conn.close()

    y_values = np.array(y_values) / nb_war_total * 100

    return x_values, y_values


# create stats from SQLite3 data base with pandas
start_time = timer()

stats = create_stats_from_sql_with_pd()

print("Runtime: {}s".format(round(timer() - start_time, 2)))

xs = stats[0]
ys = stats[1]

print("Sum frequency: {}".format(sum(ys)))  # should be near 100

# doesn't work if the data is too small, a better way to do it is coming
y0 = ys[0:len(ys):2]
y1 = ys[1:len(ys):2]
x0 = xs[0:len(xs):2]
x1 = xs[1:len(xs):2]

# display the graph
style.use('ggplot')

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))

ax1.plot(x0, y0, 'b', label='even')
ax1.plot(x1, y1, 'r', label='odd')

plt.rc('legend', fontsize=20)
plt.subplots_adjust(left=0.03, bottom=0.03, right=1.0, top=1.0, wspace=0.2, hspace=0)
ax1.legend()

plt.show()
