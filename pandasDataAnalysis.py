import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
import sqlite3
import numpy as np


style.use('fivethirtyeight')


def read_data_nb_pli():
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT nb_pli FROM war", conn)
    conn.close()
    return df


def read_data_player1():
    conn = sqlite3.connect('data.db')
    data_frame = pd.read_sql_query("SELECT base_game_player1 FROM war", conn)
    conn.close()
    return data_frame

def read_data_player2():
    conn = sqlite3.connect('data.db')
    data_frame = pd.read_sql_query("SELECT base_game_player2 FROM war", conn)
    conn.close()
    return data_frame


# print(">>> reading...")
# df_nb_pli = read_data_nb_pli()
# print(">>> heading...")
# print(df_nb_pli.head())
# print(">>> describing...")
# print(df_nb_pli.describe())

print(">>> reading...")
df1 = read_data_player1()
df2 = read_data_player2()
print(">>> heading...")
print(df1.head(), df2.head())
print(">>> describing...")
print(df1.describe(), df2.describe())

# df.to_csv(r'C:\Users\admin\PycharmProjects\Bataille\data\data_global.csv', compression='bz2')
# df.to_csv(r'C:\Users\admin\PycharmProjects\Bataille\data\data_global.csv')
