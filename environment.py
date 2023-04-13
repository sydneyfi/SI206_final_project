from urllib.request import urlopen
import sqlite3
import certifi
import json
import os
import requests


# financial modeling prep API Key: 7b82b2f514ddca127fb725b5c725eb67

def get_jsonparsed_data(url):
    # response = urlopen(url, cafile=certifi.where())
    # data = response.read().decode("utf-8")
    # return json.loads(data)
    try:
        data = requests.get(url)
        return data.json()
    except:
        return None


def make_db(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ db)
    cur = conn.cursor()
    return cur, conn
    

def main():
    url1 = 'https://api.websitecarbon.com/site?url='
    website = None

    cur, conn = make_db('Companies.db')

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS Environment
        (id INTEGER PRIMARY KEY, green_id INTEGER, cleaner_than FLOAT, bytes FLOAT, CO2 FLOAT)
        '''
    )

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Green 
        (id INTEGER PRIMARY KEY, label TEXT)
        '''
    )

    cur.execute('SELECT max(id) FROM Green')
    start = None
    try:
        row = cur.fetchone()
        if row is None:
            start = 0
        else:
            start = row[0] + 1
    except:
        start = 0
    
    if start is None: start = 0
    end = start + 25
    if end > 100: end = 100

    cur.execute('SELECT id, website FROM Financial')
    finance = cur.fetchall()

    cur.execute('INSERT OR IGNORE INTO Green (id, label) VALUES (?,?)', (0, "unknown"))
    cur.execute('INSERT OR IGNORE INTO Green (id, label) VALUES (?,?)', (1, "True"))
    cur.execute('INSERT OR IGNORE INTO Green (id, label) VALUES (?,?)', (2, "null"))

    for i in range(start, end): # INSERT max 25 items :), not take
        website = finance[i][1]
        data_dict = get_jsonparsed_data(url1 + website)
        if data_dict is None:
            label = "null"
        else:
            #how do i deal with the label?? like how do i manually check? this will go into green_id
            label = str(data_dict.get('green', "unknown"))
            clean = data_dict["cleanerThan"]
            bit = data_dict["statistics"]["adjustedBytes"]
            carbon = data_dict["statistics"]["co2"]["grid"]["grams"]

        cur.execute('INSERT OR IGNORE INTO Environment (id, green_id, cleaner_than, bytes, CO2) VALUES (?,?,?,?,?)', (int(finance[i][0]), label, clean, bit, carbon))

    conn.commit()

    # if cur.fetchone() == None:

    


if __name__ == "__main__":
    main()