# -*-coding:utf8;-*-
import sqlite3
import pickle
from timeit import default_timer as timer
import pandas as pd
import GenerateFirstXTrick as first


def model(players_deck):
    res = []
    for player_deck in players_deck:
        ret = []
        for i in player_deck:
            ret.append(i ** 10)
        res.append(sum(ret))
    return res


def model1(players_deck):
    res = []
    for player_deck in players_deck:
        ret = []
        for i in player_deck:
            ret.append(i ** i)
        res.append(sum(ret))
    return res


def model2(players_deck):
    b = first.Battle(players_deck[0], players_deck[1], 52)
    res = b.trick()
    if res == 1:
        final_result = (1, 0)
    elif res == 2:
        final_result = (0, 1)
    else:
        final_result = (0, 0)
    return final_result


def import_data():
    conn = sqlite3.connect('D:\data\data_merged.db')
    data_frame = pd.read_sql_query(
        """SELECT base_deck_player1, base_deck_player2, victory FROM war WHERE victory!=3 LIMIT {}""".format(X), conn)
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

        sum_evaluated_base_deck = evaluation_model((pickle.loads(qqc[1][0]), pickle.loads(qqc[1][1])))
        sum_evaluated_base_deck_player1 = sum_evaluated_base_deck[0]
        sum_evaluated_base_deck_player2 = sum_evaluated_base_deck[1]

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
        else:
            print('WTF')
    return total_tests, valid_test, non_valid_test

try:
    X = int(input("Number of battles to analyse: "))
except ValueError:
    print("ValueError: you muss enter an integer!\nNumber of battles to analyse set to 10000.")
    X = 10000

if __name__ == '__main__':
    df = import_data()

    models_dic = {'reference_model': model, 'tested_model': model1, 'second_tested_model': model2}
    models = list(models_dic.values())
    models_names = list(models_dic.keys())

    for model, model_name in zip(models, models_names):
        start_time = timer()
        result = check_model(df, model)
        runtime = round(timer() - start_time, 2)

        total = result[0]
        ok = result[1]
        non_ok = result[2]

        print('\n{}:'.format(model_name))
        print("\t- took: {}s".format(runtime))
        print("\t- Total: {}".format(total))
        print("\t- Ok: {}".format(ok))
        print("\t- Wrong: {}".format(non_ok))
        print("\t- Percentage ok: {}%".format(round(ok / total * 100, 2)))
