# -*-coding:utf8;-*-
import sqlite3
import pickle
import pandas as pd


def model(player_deck):
    ret = []
    for i in player_deck:
        ret.append(i ** 10)
    return sum(ret)


def import_data():
    conn = sqlite3.connect('data.db')
    data_frame = pd.read_sql_query(
        """SELECT base_deck_player1, base_deck_player2, victory FROM war LIMIT {}""".format(X), conn)
    conn.close()

    # visualise DataFrame
    print(data_frame.head())
    return data_frame


def check_model(data_frame, evaluation_model):
    total_tests = 0
    valid_test = 0
    non_valid_test = 0

    for qqc in data_frame.iterrows():
        total_tests += 1

        victory = qqc[1][2]

        sum_evaluated_base_deck_player1 = evaluation_model(pickle.loads(qqc[1][0]))
        sum_evaluated_base_deck_player2 = evaluation_model(pickle.loads(qqc[1][1]))

        if victory == 1:
            if sum_evaluated_base_deck_player1 > sum_evaluated_base_deck_player2:
                valid_test += 1
            else:
                non_valid_test += 1
        elif victory == 2:
            if sum_evaluated_base_deck_player1 < sum_evaluated_base_deck_player2:
                valid_test += 1
            else:
                non_valid_test += 1
        else:  # victory == 3
            pass
    return total_tests, valid_test, non_valid_test

try:
    X = int(input("Number of battles to analyse: "))
except ValueError:
    print("ValueError: you muss enter an integer!\nNumber of battles to analyse set to 100000.")
    X = 100000

if __name__ == '__main__':
    df = import_data()

    result = check_model(df, model)

    total = result[0]
    ok = result[1]
    non_ok = result[2]

    print('\n')
    print("Total: {}".format(total))
    print("Ok: {}".format(ok))
    print("Wrong: {}".format(non_ok))
    print("Percentage ok: {}%".format(round(ok / (ok + non_ok) * 100, 2)))
