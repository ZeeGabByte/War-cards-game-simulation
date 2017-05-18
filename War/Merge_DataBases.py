# merge the data bases created with a multi processes version
import sqlite3


path_list = [r'D:\data\data', r'D:\data\nb_trick\data_trick', r'D:\data\nb_trick2\data_trick']
path_attributes_list = ['(base_deck_player1 list, base_deck_player2 list, victory int, nb_trick int)',
                        '(nb_trick int)', '(nb_trick int)']

try:
    nb_db = int(input("Number of data bases: "))
except ValueError:
    print("ValueError: you muss enter an integer!\nNumber of data bases set to 1.")
    nb_db = 1

i = 0
for path in path_list:
    print('\t- ', i, path)
    i += 1

try:
    path_index = int(input("Enter the number of the path you want: "))
except ValueError:
    print("ValueError: you muss enter an integer!\nPath set to: {}".format(path_list[0]))
    path_index = 0
try:
    path = path_list[path_index]
except IndexError:
    print("Non valid index")
    path = 'D:\data\data'
    path_index = 0
    path_attributes_list = ['(base_deck_player1 list, base_deck_player2 list, victory int, nb_trick int)']

conn = sqlite3.connect('{}_merged.db'.format(path))
c = conn.cursor()

try:
    c.execute("""CREATE TABLE war {}""".format(path_attributes_list[path_index]))
    conn.commit()
except sqlite3.OperationalError:
    pass

for i in range(nb_db):
    print("Merging: {} / {}".format(i, nb_db - 1))
    c.execute("""ATTACH '{}{}.db' AS db_to_merge{}""".format(path, i, i))
    c.execute("""INSERT INTO main.war SELECT * FROM db_to_merge{}.war""".format(i))
    conn.commit()

conn.close()
