from urllib.request import urlopen
import sqlite3
import certifi
import json
import os


# financial modeling prep API Key: 7b82b2f514ddca127fb725b5c725eb67

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def make_db(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ db)
    cur = conn.cursor()
    return cur, conn
    

def main():
    url1 = 'https://financialmodelingprep.com/api/v3/profile/'
    ticker = 'AAPL'
    url2 = '?apikey=7b82b2f514ddca127fb725b5c725eb67'

    cur, conn = make_db('Companies.db')
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS Financial
        (ranking INTEGER PRIMARY KEY, stock_price FLOAT, website STRING)
        '''
    )

    cur.execute('SELECT * FROM ')

    data_dict = get_jsonparsed_data(url1 + ticker + url2)[0]

    


if __name__ == "__main__":
    main()