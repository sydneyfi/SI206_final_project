from urllib.request import urlopen
import matplotlib.pyplot as plt
import sqlite3
import certifi
import json
import os
import requests

import stockInfo
import environment
import topCompanies

def pie_calc(cur, conn):
    d = {}

    cur.execute('SELECT label FROM Green')
    green_labels = cur.fetchall()

    for gl in green_labels:
        cur.execute(f"SELECT COUNT(Green.label) FROM Environment JOIN Green ON Environment.green_id = Green.id WHERE Green.label = '{gl[0]}'")
        result = cur.fetchone()
        d[gl[0]] = result[0]
        # print("label:", gl, "result:", result[0])
        # print(d)
    
    return d
    

def main():
    #put other file functions here in following order: topCompanies, stockInfo, environment
    # for i in range(0,4):
    #     topCompanies.topCompanies()
    # for i in range(0,4):
    #     stockInfo.stockInfo()
    # for i in range(0,4):
    #     environment.environment()

    main_dict = {}

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/'+ "Companies.db")
    cur = conn.cursor()

    green_dict = pie_calc(cur, conn)

    main_dict["pie_chart"] = green_dict

    with open("calculations.json", 'w') as f:
        f.write(json.dumps(main_dict, indent=4))

    file = open("calculations.json", "r")
    contents = file.read()
    dict = json.loads(contents)
    pie_chart = dict["pie_chart"]

    x = list(pie_chart.values())
    plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()

    ax.pie(x, radius= 3, center=(4,4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
    plt.show()




    pass

if __name__ == "__main__":
    main()

