from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
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

# def histogram_calc(cur, conn):
#     cur.execute('SELECT cleaner_than FROM Environment')
#     data_list = cur.fetchall()
#     l = []

#     for data in data_list:
#         l.append(data[0])

#     # Creating dataset
#     a = np.array(l)
    
#     # Creating histogram
#     fig, ax = plt.subplots(figsize =(10, 7))
#     ax.hist(a, bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    
#     # Show plot
#     plt.show()





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

    # #histogram
    # cur.execute('SELECT cleaner_than FROM Environment')
    # data_list = cur.fetchall()
    # l = []

    # for data in data_list:
    #     l.append(data[0])

    # # Creating dataset
    # a = np.array(l)
    
    # # Creating histogram
    # fig, ax = plt.subplots(figsize =(10, 7))
    # ax.hist(a, bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    
    # # Show plot
    # plt.show()




    pass

if __name__ == "__main__":
    main()

