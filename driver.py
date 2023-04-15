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


def create_pie(filename):

    file = open(filename, "r")
    contents = file.read()
    dict = json.loads(contents)
    pie_chart = dict["green_count"]

    x = list(pie_chart.values())
    # plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()

    labels = 'Green', 'Not Green'

    ax.pie(x, radius= 3, center=(4,4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, labels=labels, autopct='%1.1f%%')
    ax.set_title("Proportion of Top 100 Company's Websites that are considered Green")


def create_histogram(cur, conn):
    cur.execute('SELECT cleaner_than FROM Environment')
    data_list = cur.fetchall()
    l = []

    for data in data_list:
        l.append(data[0])

    # Creating dataset
    a = np.array(l)
    
    # Creating histogram
    fig, ax = plt.subplots(figsize =(10, 7))
    ax.hist(a, bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    
    # Show plot
    # plt.show()


def bar_one_calc(cur, conn):
    tup_l = [] # (avg, name)
    d = {}
 
    cur.execute('SELECT Financial.low_price, Financial.high_price, Website.name FROM Financial JOIN Website ON Financial.id = Website.id')
    data_list = cur.fetchall()
    
    for data in data_list:
        avg = round((float(data[0]) + float(data[1])) / 2.0, 2)
        tup_l.append((avg, data[2]))

    sorted_list = list(sorted(tup_l, key = lambda t: t[0], reverse=True)) # sort by avg stock price in decending order

    for i in range(0,10):
        d[sorted_list[i][1]] = sorted_list[i][0]
    
    return d


def create_bar_one(filename):
    file = open(filename, "r")
    contents = file.read()
    dict = json.loads(contents)

    x = list(dict['top_avg_stock'].keys())
    y = list(dict['top_avg_stock'].values())

    fig, ax = plt.subplots(figsize =(20, 7))
    ax.barh(x,y)

    ax.set_xlabel('Average Stock Price ($)')
    ax.set_ylabel('Company Name')
    # plt.show()


def bar_two_calc(cur, conn):
    tup_l = [] # (CO2/bytes , name)
    d1 = {}
    d2 = {}
 
    cur.execute('SELECT Environment.CO2, Environment.bytes, Website.name, Website.ranking FROM Environment JOIN Website ON Environment.id = Website.id')
    data_list = cur.fetchall()
    
    for data in data_list:
        # cb = float('{:0.3e}'.format(float(data[0]) / float(data[1])))
        # cb = float(data[0]) / float(data[1])
        cb = float(data[0]) / (float(data[1]) * 0.00001)
        tup_l.append((cb, data[2], int(data[3])))

    ascend_list = list(sorted(tup_l, key = lambda t: t[2])) # sort by ranking in ascending order
    descend_list = list(sorted(tup_l, key = lambda t: t[2], reverse=True)) # sort by ranking in descending order


    for i in range(0,10):
        d1[ascend_list[i][1]] = ascend_list[i][0]
        d2[descend_list[i][1]] = descend_list[i][0]
    
    return d1, d2


def create_bar_two(filename):
    file = open(filename, "r")
    contents = file.read()
    dict = json.loads(contents)

    x1 = list(dict['top_carbon_per_byte'].keys())
    y1 = list(dict['top_carbon_per_byte'].values())
    x2 = list(dict['bottom_carbon_per_byte'].keys())
    y2 = list(dict['bottom_carbon_per_byte'].values())

    fig = plt.figure(figsize=(20,10))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.barh(x1, y1)
    ax2.barh(x2, y2)
    ax1.set_xlabel('CO2 per Byte')
    ax1.set_ylabel('Company Name')
    ax2.set_xlabel('CO2 per Byte')
    ax2.set_ylabel('Company Name')
    ax1.set_xlim([0.0333432108163833, 0.0333432108163834])
    ax2.set_xlim([0.0333432108163833, 0.0333432108163834])

    plt.show()


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
    filename = "calculations.json"

    green_dict = pie_calc(cur, conn)
    bar_one_dict = bar_one_calc(cur, conn)
    bar_two_dict1, bar_two_dict2 = bar_two_calc(cur, conn)


    main_dict["green_count"] = green_dict
    main_dict["top_avg_stock"] = bar_one_dict
    main_dict["top_carbon_per_byte"] = bar_two_dict1
    main_dict["bottom_carbon_per_byte"] = bar_two_dict2


    with open(filename, 'w') as f:
        f.write(json.dumps(main_dict, indent=4))


    create_pie(filename)
    create_histogram(cur, conn)
    create_bar_one(filename)
    create_bar_two(filename)
    # plt.show()

    

    pass

if __name__ == "__main__":
    main()

