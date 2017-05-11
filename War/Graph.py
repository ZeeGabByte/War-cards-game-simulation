# -*-coding:utf8;-*-
import sqlite3
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd


def create_stats_from_sql_with_pd(low_born, up_born):
    """
    Create stats from SQLite3 data base with pandas
        if low_born == 'lower': take the min in data base
        if up_born == 'upper': take the max in data base
        if nb_trick_total == None: find it in data base
    Return a list of the frequency [plot] (in %) of a war of x trick (with x = range(low_born, up_born + 1))
    """

    conn = sqlite3.connect('data\data_merged.db')
    df0 = pd.read_sql_query("SELECT nb_trick FROM war", conn)
    conn.close()

    nb_trick_total = df0['nb_trick'].sum()

    plot = []
    for i in range(low_born, up_born + 1):
        temporary_df = df0[(df0['nb_trick'] == i)]
        plot.append(temporary_df['nb_trick'].count() / nb_trick_total * 100)
    return plot


create_stats = input("Generate stats ([y]/n): ")
if create_stats.upper()[0] == 'Y':
    create_stats = True

lower_born = 0
upper_born = 3000

if create_stats is True:
    # create stats from SQLite3 data base with pandas and export data to csv
    stats = create_stats_from_sql_with_pd(lower_born, upper_born)
    x = list(range(lower_born, upper_born + 1))

    df = pd.DataFrame({'nb_trick': x, 'probability': stats})

    df.set_index('nb_trick', inplace=True)

    df.to_csv(r'C:\Users\admin\PycharmProjects\Bataille\War\data\data {}.csv'
              .format((lower_born, upper_born + 1)), compression='bz2')

# import data from csv
df = pd.read_csv(r'C:\Users\admin\PycharmProjects\Bataille\War\data\data {}.csv'
                 .format((lower_born, upper_born + 1)), compression='bz2')

x = list(df['nb_trick'])
y = list(df['probability'])

# display the graph
style.use('ggplot')

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))

ax1.plot(x, y, 'b', linewidth=1.0)

ax1.set_xticks(range(lower_born, upper_born, (upper_born - lower_born) // 20))
plt.subplots_adjust(left=0.03, bottom=0.03, right=1.0, top=1.0, wspace=0.2, hspace=0)

plt.show()
