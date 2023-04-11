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

    data = requests.get(url)
    return data.json()


def make_db(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ db)
    cur = conn.cursor()
    return cur, conn
    

def main():
    url1 = 'https://financialmodelingprep.com/api/v3/profile/'
    ticker = None
    url2 = '?apikey=7b82b2f514ddca127fb725b5c725eb67'

    cur, conn = make_db('Companies.db')

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS Financial
        (id INTEGER PRIMARY KEY, stock_price FLOAT, website TEXT)
        '''
    )

    cur.execute('SELECT max(id) FROM Financial')
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

    cur.execute('SELECT id, ticker FROM Website')
    webs = cur.fetchall()

    for i in range(start, end): # INSERT max 25 items :), not take
        ticker = webs[i][1]
        data_dict = get_jsonparsed_data(url1 + ticker + url2)[0]

        price = data_dict['price']
        website = data_dict['website']

        # print((w[0], price, website))

        cur.execute('INSERT OR IGNORE INTO Financial (id, stock_price, website) VALUES (?,?,?)', (int(webs[i][0]), float(price), website))

    conn.commit()

    # if cur.fetchone() == None:

    


if __name__ == "__main__":
    main()