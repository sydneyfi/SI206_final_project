# Team name: The Pie Chart Pastries
# Team Members: Selena Wang, Sydney Finkelstein, Katherine Zhao 

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests
import sqlite3

#returns the company name, ticker name, and ranking of each company
def get_top_companies():
    url = f"https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    name_list = [x.text for x in soup.find_all("div", class_ = "company-name")]
    ticker_list = [x.text for x in soup.find_all("div", class_ = "company-code")]

    companies = []
    for i in range(len(name_list)):
        tup = (name_list[i], ticker_list[i], (i+1))
        companies.append(tup)

    return companies

def createTable():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Companies.db")
    cur = conn.cursor()

    conn.commit()

    return cur, conn

def make_top_companies_table(cur, conn, list_of_tups):
    cur.execute('''CREATE TABLE IF NOT EXISTS Website (id INTEGER PRIMARY KEY, ranking INTEGER UNIQUE,
                    name TEXT, ticker TEXT)''')
    cur.execute("SELECT MAX(id) FROM Website")
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
    if end > 100:
        end = 100
    
    for i in range(start, end):
        cur.execute("INSERT OR IGNORE INTO Website (id, ranking, name, ticker) VALUES (?,?,?,?)",(i, list_of_tups[i][2], list_of_tups[i][0], list_of_tups[i][1]))

    conn.commit()



def topCompanies():
    companies = get_top_companies()
    cur, conn = createTable()
    make_top_companies_table(cur, conn, companies)

    conn.close()


if __name__ == "__main__":
    topCompanies()