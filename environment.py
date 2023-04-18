from urllib.request import urlopen
import sqlite3
import certifi
import json
import os
import requests


# financial modeling prep API Key: 7b82b2f514ddca127fb725b5c725eb67

def get_jsonparsed_data(url):
    try:
        data = requests.get(url, timeout=None)
        return data.json()
    except:
        return None


def make_db(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ db)
    cur = conn.cursor()
    return cur, conn
    

def environment():
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

    cur.execute('SELECT max(id) FROM Environment')
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
    if end > 100: end = 100 # account for index out of range

    cur.execute('SELECT id, website FROM Financial')
    finance = cur.fetchall()

    for i in range(start, end): # INSERT max 25 items :), not take
        website = finance[i][1]
        if website == "https://www.stock.walmart.com": # clean data for websites that don't work
            website = "https://www.walmart.com"
        elif website == "https://corporate.mcdonalds.com":
            website = "https://www.mcdonalds.com"
        elif website == "https://www.amd.com":
            website = "https://ir.amd.com/"
        elif website == "https://www.lowes.com":
            website = "https://corporate.lowes.com/"
        elif website == "https://www.spglobal.com":
            website = "https://investor.spglobal.com/"

        print("i:", i, ", Website:", website)

        data_dict = get_jsonparsed_data(url1 + website)
        
        if data_dict is None:
            print("None dict:", website)
            return
        elif data_dict == {}:
            print("Empty dict:",website) # cahnge so that it uhhh re-requests
            data_dict = get_jsonparsed_data(url1 + website)
            while data_dict == {}:
                print("rerunning: ", website)
                data_dict = get_jsonparsed_data(url1 + website)
        
        green_label = str(data_dict.get('green', "no data"))
        cur.execute("SELECT id FROM Green WHERE label = ?", (green_label, ))

        green_tup = cur.fetchone()

        if green_tup is None or green_tup[0] is None:
            cur.execute('SELECT MAX(id) FROM Green')
            max_tuple = cur.fetchone()

            if max_tuple is None or max_tuple[0] is None:
                max_id = 0
            else:
                max_id = int(max_tuple[0]) + 1
                
            cur.execute("INSERT OR IGNORE INTO Green (id, label) VALUES (?,?)", (max_id, green_label))
            green_id = max_id
        else:
            green_id = int(green_tup[0])


        clean = data_dict.get("cleanerThan", -1)
        bit = data_dict["statistics"]["adjustedBytes"]
        carbon = data_dict["statistics"]["co2"]["grid"]["grams"]

        cur.execute('INSERT OR IGNORE INTO Environment (id, green_id, cleaner_than, bytes, CO2) VALUES (?,?,?,?,?)', (int(finance[i][0]), green_id, clean, bit, carbon))
        conn.commit()


    


if __name__ == "__main__":
    environment()