import pprint
from datetime import datetime
from numpy.lib.type_check import _asfarray_dispatcher
import requests
import pandas as pd
from kiteconnect import KiteConnect
import json
from abc import abstractstaticmethod
import configparser
import concurrent
from requests.api import get
import os


pp = pprint.PrettyPrinter(indent=4)





config = configparser.ConfigParser()
file_path_for_credentials = os.getcwd() + '/data_files/' + 'credential.ini'
config.read(file_path_for_credentials)
api_key = config['kite']['api_key']

file_path_for_data = os.getcwd() + '/data_files/data.json'
with open(file_path_for_data, 'r') as fp:
    data = json.load(fp)
access_token = data["accesstoken"]








bullish_dic_r3 = {}
def find_highest_volume_strike_r3(name):
    file_path_for_df_calls = os.getcwd() + '/data_files/' + 'df_calls.csv'
    df = pd.read_csv(file_path_for_df_calls)

    df_calls = df.copy()
    df_calls = df_calls.loc[df_calls['name'] == name]
    sorted_df = df_calls.sort_values(by=['strike'])

    opt_symbol_list = sorted_df['tradingsymbol'].tolist()
    opt_symbol_list_new = []
    for symbol in opt_symbol_list:
        opt_symbol_list_new.append("NFO:" + symbol)

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token=access_token)
    dd = kite.quote(opt_symbol_list_new)

    li = list(dd.keys())
    max_vol = 0
    strike = ""
    instrument_token = ""
    for i in li:
        l = (dd[i]['volume'])
        if(l > max_vol):
            strike = i
            max_vol = l
            instrument_token = str(dd[i]['instrument_token'])

    sym = strike.replace("NFO:", "")
    strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
        sym + "/" + instrument_token

    bullish_dic_r3[name] = strike_url

def find_bullish_stocks_r3():
    global bullish_dic_r3
    bullish_dic_r3 = {}
    
    file_path_for_df_stock_fut_zerodha = os.getcwd() + '/data_files/' + \
        'df_stock_fut_zerodha.csv'
    df_stock_fut_zerodha = pd.read_csv(file_path_for_df_stock_fut_zerodha)
    
    
    file_path_for_df_joined = os.getcwd() + '/data_files/' + "joined.csv"
    df_joined = pd.read_csv(file_path_for_df_joined)

    '''
    part 1
    '''
    now = datetime.now()

    fut_symbol_list = df_stock_fut_zerodha['tradingsymbol'].tolist()
    future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
    for symbol in fut_symbol_list:
        temp = symbol.replace("&", "%26")
        symbol = temp
        future_string = future_string + "i=NFO:" + symbol + "&"
    future_string = future_string[:-1]

    r = requests.get(future_string, timeout=10)
    data = (r.json())
    dic = data['data']

    '''
    part 2
    '''
    temp = df_joined.copy()
    for i in dic.keys():
        d = list(dic[i].values())
        token = d[0]
        ltp = d[1]
        temp.loc[temp.instrument_token == token, 'last_price'] = ltp
    df_step_4 = temp.copy()

    df_step_4['checker'] = df_step_4.apply(lambda row: int(float(row.last_price)) > int(
        float(row.R3)), axis=1)

    df_step_5 = df_step_4.copy()
    df_step_5.drop(df_step_5[df_step_5['checker']
                   == False].index, inplace=True)

    stock_name_url_dic = pd.Series(
        df_step_5.url.values, index=df_step_5.name).to_dict()

    bullish_stocks = list(stock_name_url_dic.keys())
    # bullish_stocks =  df_stock_fut_zerodha['name'].tolist()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(find_highest_volume_strike_r3, bullish_stocks)

    then = datetime.now()
    timetaken = then - now
    print("time taken ", timetaken.total_seconds())

    return bullish_dic_r3




bullish_dic_r2 = {}
def find_highest_volume_strike_r2(name):
    
    file_path_for_df_calls = os.getcwd() + '/data_files/' + 'df_calls.csv'
    df = pd.read_csv(file_path_for_df_calls)

    df_calls = df.copy()
    df_calls = df_calls.loc[df_calls['name'] == name]
    sorted_df = df_calls.sort_values(by=['strike'])

    opt_symbol_list = sorted_df['tradingsymbol'].tolist()
    opt_symbol_list_new = []
    for symbol in opt_symbol_list:
        opt_symbol_list_new.append("NFO:" + symbol)

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token=access_token)
    dd = kite.quote(opt_symbol_list_new)

    li = list(dd.keys())
    max_vol = 0
    strike = ""
    instrument_token = ""
    for i in li:
        l = (dd[i]['volume'])
        if(l > max_vol):
            strike = i
            max_vol = l
            instrument_token = str(dd[i]['instrument_token'])

    sym = strike.replace("NFO:", "")
    strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
        sym + "/" + instrument_token

    # print(strike)
    bullish_dic_r2[name] = strike

def find_bullish_stocks_r2():
    global bullish_dic_r2
    bullish_dic_r2 = {}
    
    file_path_for_df_stock_fut_zerodha = os.getcwd() + '/data_files/' + \
        'df_stock_fut_zerodha.csv'
    df_stock_fut_zerodha = pd.read_csv(file_path_for_df_stock_fut_zerodha)
    
    
    file_path_for_df_joined = os.getcwd() + '/data_files/' + "joined.csv"
    df_joined = pd.read_csv(file_path_for_df_joined)

    '''
    part 1
    '''
    now = datetime.now()

    fut_symbol_list = df_stock_fut_zerodha['tradingsymbol'].tolist()
    future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
    for symbol in fut_symbol_list:
        temp = symbol.replace("&", "%26")
        symbol = temp
        future_string = future_string + "i=NFO:" + symbol + "&"
    future_string = future_string[:-1]

    r = requests.get(future_string, timeout=10)
    data = (r.json())
    dic = data['data']
    
    # print(data)

    '''
    part 2
    '''
    temp = df_joined.copy()
    for i in dic.keys():
        d = list(dic[i].values())
        token = d[0]
        ltp = d[1]
        temp.loc[temp.instrument_token == token, 'last_price'] = ltp
    df_step_4 = temp.copy()

    # df_step_4['checker'] = df_step_4.apply(
    #     lambda row:
    #         int(float(row.last_price)) > int(float(row.R2))
    #         and
    #         int(float(row.last_price)) < int(float(row.R3)), axis=1)

    df_step_4['checker'] = df_step_4.apply(
        lambda row:
            int(float(row.last_price)) > int(float(row.R2)), axis=1)

    df_step_5 = df_step_4.copy()
    df_step_5.drop(df_step_5[df_step_5['checker']
                   == False].index, inplace=True)

    stock_name_url_dic = pd.Series(
        df_step_5.url.values, index=df_step_5.name).to_dict()

    bullish_stocks = list(stock_name_url_dic.keys())
    print(len(bullish_stocks))
    # bullish_stocks =  df_stock_fut_zerodha['name'].tolist()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(find_highest_volume_strike_r2, bullish_stocks)

    then = datetime.now()
    timetaken = then - now
    # print("time taken ", timetaken.total_seconds())

    return bullish_dic_r2




def find_option_strike_helper(name):
    file_path_for_df_calls = os.getcwd() + '/data_files/' + 'df_calls.csv'
    df = pd.read_csv(file_path_for_df_calls)

    df2 = df.copy()
    df2 = df2.loc[df2['name'] == name]
    sorted_df = df2.sort_values(by=['strike'])

    opt_symbol_list = sorted_df['tradingsymbol'].tolist()
    opt_symbol_list_new = []
    for symbol in opt_symbol_list:
        opt_symbol_list_new.append("NFO:" + symbol)

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token=access_token)
    dd = kite.quote(opt_symbol_list_new)

    li = list(dd.keys())
    max_vol = 0
    strike = ""
    instrument_token = ""
    for i in li:
        l = (dd[i]['volume'])
        if(l > max_vol):
            strike = i
            max_vol = l
            instrument_token = str(dd[i]['instrument_token'])

    sym = strike.replace("NFO:", "")
    strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
        sym + "/" + instrument_token
    return strike_url

def find_option_strike(option_strike):
    output_dic = {}
    output_dic[option_strike] = find_option_strike_helper(option_strike)
    return output_dic




output_dic_for_vwap_r3 = {}
def find_vwap_r3_setup_helper(bullish_stocks):
    file_path_for_joined_df_for_calls = os.getcwd() + '/data_files/' +  "joined_df_for_calls.csv"
    df = pd.read_csv(file_path_for_joined_df_for_calls)
    temp = df.copy()
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token=access_token)

    # print(bullish_stocks)
    for k,v in bullish_stocks.items():
        # print(k)
        temp2 = temp.copy()
        trading_symbol = v.replace("NFO:", "")
        temp2 = temp2.loc[temp2['tradingsymbol'] == trading_symbol]
        # r3_price = temp2['R3'].values[0]
        r2_price = temp2['R2'].values[0]
        dd = kite.quote(v)
        # print(dd)
        # print('hiii')
        li = list(dd.keys())
        instrument_token = ""
        for i in li:
            last_price = (dd[i]['last_price'])
            average_price = (dd[i]['average_price'])
            # print(average_price, last_price)
            instrument_token = str(dd[i]['instrument_token'])
            
            if(average_price >= r2_price and last_price > r2_price):
                strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
                    trading_symbol + "/" + instrument_token
                output_dic_for_vwap_r3[k] = strike_url

def find_vwap_r3_setup():
    global output_dic_for_vwap_r3 
    output_dic_for_vwap_r3 = {}
    bullish_stocks = find_bullish_stocks_r2()
    # print(bullish_stocks)
    temp_lis = []
    
    for k,v in bullish_stocks.items():
        temp_dic = {}
        temp_dic[k] = v
        temp_lis.append(temp_dic)
        
    # print(temp_lis)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(find_vwap_r3_setup_helper, temp_lis)

    return output_dic_for_vwap_r3

# print(find_vwap_r3_setup())


