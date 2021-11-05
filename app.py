import pandas as pd
import time
import json
from flask import Flask, Response, flash, request, render_template, stream_with_context, send_file
from requests.api import get
from datetime import datetime
from flask_pymongo import PyMongo
import urllib
import os
from scripts import *

app = Flask(__name__)

# to clear list before starting server
visited_obj = []
with open('visited.json', 'w') as fp:
    json.dump(visited_obj, fp)


@app.route("/clear_visited", methods=["GET", "POST"])
def clear_visited():
    if request.method == "POST":
        visited_obj = []
        with open('visited.json', 'w') as fp:
            json.dump(visited_obj, fp)
        dd = {}
        dd = json.dumps(dd)
        return dd


@app.route("/prev_day", methods=["GET", "POST"])
def prev_day():
    if request.method == "POST":
        prev_date = request.form.get("prev_date")
        prev_date = int(prev_date)
        # print(prev_date)

        prev_month = request.form.get("prev_month")
        prev_month = int(prev_month)
        # print(prev_month)

        prev_year = request.form.get("prev_year")
        prev_year = int(prev_year)
        # print(prev_year)



        def fun0():
            file_path_for_predata = os.getcwd() + '/data_files/predata.json'
            with open(file_path_for_predata, 'r') as fp:
                predata_obj = json.load(fp)
            predata_obj["prev_date"] = prev_date
            predata_obj["prev_month"] = prev_month
            predata_obj["prev_year"] = prev_year


            with open(file_path_for_predata, 'w') as fp:
                json.dump(predata_obj, fp)
        fun0()

        return "done"

@app.route("/access_token", methods=["GET", "POST"])
def access_token():
    if request.method == "POST":
        def fun1():
            # from kite_autologin import autologin
            autologin()
        print('calling autologin function')
        fun1()
        return "done"

@app.route("/pre_bullish", methods=["GET", "POST"])
def pre_bullish():
    if request.method == "POST":
        def fun2():
            fun()
        fun2()
        return "done"


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def render_index():
    return render_template("home.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/vwap_r3_setup", methods=["GET", "POST"])
def vwap_r3_setup():
    if request.method == "POST":
        now = datetime.now()
        dd = find_vwap_r3_setup()
        dd = json.dumps(dd)
        then = datetime.now()
        timetaken = then - now
        print("time taken ", timetaken.total_seconds())
        return dd
    
@app.route("/bullish_stocks_r2", methods=["GET", "POST"])
def bullish_stocks_r2():
    if request.method == "POST":
        dd = find_bullish_stocks_r2()
        dd = json.dumps(dd)
        return dd
    
@app.route("/bullish_stocks_r3", methods=["GET", "POST"])
def bullish_stocks_r3():
    if request.method == "POST":
        dd = find_bullish_stocks_r3()
        dd = json.dumps(dd)
        return dd    

        
@app.route("/option_strike", methods=["GET", "POST"])
def option_strike():
    if request.method == "POST":
        option_strike = request.form.get("select_symbol")
        dd = find_option_strike(option_strike=option_strike)
        dd = json.dumps(dd)
        return dd
    

if __name__ == "__main__":
    app.debug= True
    app.run(threaded=True, port=5000)
