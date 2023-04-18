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
        leb = gl[0]
        cur.execute(f"SELECT COUNT(Green.label) FROM Environment JOIN Green ON Environment.green_id = Green.id WHERE Green.label = '{leb}'")
        result = cur.fetchone()
        d[gl[0]] = result[0]
    
    return d


def create_pie(filename):
    file = open(filename, "r")
    contents = file.read()
    dict = json.loads(contents)
    pie_chart = dict["green_count"]

    x = list(pie_chart.values())
    fig, ax = plt.subplots()
    ax.axis('off')

    labels = 'Green', 'Not Green'

    ax.pie(x, radius= 8, center=(4,4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, labels=labels, autopct='%1.1f%%', colors=[(0.24, 0.69, 0.1, 0.8),(0.924, 0.69, 0.1, 0.8)])
    ax.set_title("Proportion of Top 100 Companies' Websites That Are Considered Green")

    fig.savefig('Pie.png')


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
    N, bins, patches = ax.hist(a, bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], edgecolor='white', linewidth=1)

    ax.set_title("Histogram of How Green the Top 100 Companies' Websites Are")
    ax.set_xlabel('Decimal Representing the Percentage of Tested Resources the Website is Cleaner Than')
    ax.set_ylabel('Number of Companies')
    ax.set_ybound(0,25)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

    patches[9].set_facecolor((0.24, 0.69, 0.1, 0.8)) # set the colors of the bins
    patches[8].set_facecolor((0.316, 0.69, 0.1, 0.8))
    patches[7].set_facecolor((0.392, 0.69, 0.1, 0.8))
    patches[6].set_facecolor((0.468, 0.69, 0.1, 0.8))
    patches[5].set_facecolor((0.544, 0.69, 0.1, 0.8))
    patches[4].set_facecolor((0.62, 0.69, 0.1, 0.8))
    patches[3].set_facecolor((0.696, 0.69, 0.1, 0.8))
    patches[2].set_facecolor((0.772, 0.69, 0.1, 0.8))
    patches[1].set_facecolor((0.848, 0.69, 0.1, 0.8))
    patches[0].set_facecolor((0.924, 0.69, 0.1, 0.8))

    fig.savefig('Histo.png')


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

    fig, ax = plt.subplots(figsize =(15, 7))
    ax.barh(x,y, color = (0.24, 0.69, 0.1, 0.8))

    ax.set_xlabel('Average Stock Price ($)')
    ax.set_ylabel('Company Name')
    ax.set_title('Top 10 Companies with the Highest Average Stock Price')

    for i in range(10):
        ax.text(float(y[i]) + 100, i, '$' + str(y[i]), ha = 'center')

    plt.subplots_adjust(left=.25)

    fig.savefig('Bar_1.png')


def bar_two_calc(cur, conn):
    tup_l = [] # (CO2/bytes , name)
    d1 = {}
    d2 = {}
 
    cur.execute('SELECT Environment.CO2, Environment.bytes, Website.name, Website.ranking FROM Environment JOIN Website ON Environment.id = Website.id')
    data_list = cur.fetchall()
    
    for data in data_list:
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

    fig = plt.figure(figsize=(15,15))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.barh(x1, y1, color= (0.24, 0.69, 0.1, 0.8))
    ax2.barh(x2, y2, color= (0.924, 0.69, 0.1, 0.8))
    ax1.set_xlabel('CO2 per MegaByte')
    ax1.set_ylabel('Company Name (+ Ranking)')
    ax2.set_xlabel('CO2 per MegaByte')
    ax2.set_ylabel('Company Name (+ Ranking)')
    ax1.set_title('CO2 per MegaByte of the Top 10 Ranked Companies')
    ax2.set_title('CO2 per MegaByte of the Lower 10 Ranked Companies')

    rank_high = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th']
    rank_low = ['100th','99th','98th','97th','96th','95th','94th','93rd','92nd','91st','90th']

    for i in range(10):
        ax1.text(float(y1[i]) + 0.0007, i, rank_high[i], ha = 'center')
        ax2.text(float(y2[i]) + 0.0007, i, rank_low[i], ha = 'center')

    plt.subplots_adjust(left=.25)

    fig.savefig('Bar_2.png')


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
    plt.show()

    

    pass

if __name__ == "__main__":
    main()

