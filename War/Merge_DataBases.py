# merge the data bases created with a multi processes version into data\data_merged.db
import sqlite3


conn = sqlite3.connect('data\data_merged.db')
c = conn.cursor()
try:
    c.execute("""CREATE TABLE war
                 (base_deck_player1 list, base_deck_player2 list, victory int, nb_trick int)""")
    conn.commit()
except sqlite3.OperationalError:
    pass

try:
    nb_db = int(input("Number of data bases: "))
except ValueError:
    print("ValueError: you muss enter an integer!\nNumber of data bases set to 1.")
    nb_db = 1

for i in range(nb_db):
    c.execute("""ATTACH 'data\data0.db' AS db_to_merge{}""".format(i))
    c.execute("""INSERT INTO main.war SELECT * FROM db_to_merge{}.war""".format(i))
    conn.commit()
conn.close()
