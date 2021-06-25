import pandas as pd
import sys
import cymysql
import csv
import codecs


def insert(cursor, sql, args):
    cursor.execute(sql, args)

def read_csv_to_gamedata(filename):
    connection = cymysql.connect(host='econcamp02.chnnzivddubs.ap-southeast-1.rds.amazonaws.com', port=3306, user='admin', passwd='root1234', db='db', charset='utf8mb4')
    cursor = connection.cursor()
    clearAll = "DELETE FROM gamedata"
    cursor.execute(clearAll)
    with codecs.open(filename=filename, mode="r", encoding="utf_8_sig") as f:
        reader = csv.reader(f)
        next(reader)
        sql = "insert into gamedata values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for item in reader:
            if item[1] is None or item[1] == "": # item[1]作為key，不能為null
                continue
            args = tuple(item)
            print(args)
            insert(cursor, sql, args)
        connection.commit()
        cursor.close()
        connection.close()

def read_csv_to_historydata(filename):
    connection = cymysql.connect(host='econcamp02.chnnzivddubs.ap-southeast-1.rds.amazonaws.com', port=3306, user='admin', passwd='root1234', db='db', charset='utf8mb4')
    cursor = connection.cursor()
    clearAll = "DELETE FROM historydata"
    cursor.execute(clearAll)
    with codecs.open(filename=filename, mode="r", encoding="utf_8_sig") as f:
        reader = csv.reader(f)
        next(reader)
        sql = "insert into historydata values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for item in reader:
            if item[1] is None or item[1] == "": # item[1]作為key，不能為null
                continue
            args = tuple(item)
            print(args)
            insert(cursor, sql, args)
        connection.commit()
        cursor.close()
        connection.close()


def createNew():
    """
    create a new universe \n
    then return a pandas.DataFrame
    """
    new_data = {'ID': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}, 'name': {0: 'TreasureIsland', 1: 'Narnia', 2: 'Dracula', 3: 'Hogwarts', 4: 'Robinson', 5: 'DonQuixote', 6: 'Gulliver', 7: 'Peter', 8: 'Alice', 9: 'Troy'}, 'money': {0: 1000, 1: 1000, 2: 1000, 3: 1000, 4: 1000, 5: 1000, 6: 1000, 7: 1000, 8: 1000, 9: 1000}, 'food': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'max_popu': {0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100}, 'available_popu': {0: 100, 1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100}, 'Si': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'Ni': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'Ra': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'Co': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'Cr': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'cumSi': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'cumNi': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'cumRa': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'cumCo': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'cumCr': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'hurt': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'tech': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product1': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product2': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product3': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product4': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product5': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product6': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product7': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product8': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product9': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'product10': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'score': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'Round': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}
    df = pd.DataFrame(new_data)
    return df

def read(CSVfilename):
    df = pd.read_csv(CSVfilename)
    return df

def write(df, filename):
    df.to_csv(filename, sep= ",", index = False, encoding="utf_8_sig")
    print(f"{filename} is written.")

