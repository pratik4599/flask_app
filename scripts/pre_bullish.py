import json
from ntpath import join
import requests
import pandas as pd
import datetime
import time
from pynse import *
from jugaad_data.nse import bhavcopy_fo_save
from datetime import date
import os


def create_url_for_futures(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-FUT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

def create_url_for_eq(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NSE/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

def create_url_for_options(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

def label_row(row,label_yr_month):
    final_url = row['SYMBOL'] + label_yr_month + \
        str(int(row['STRIKE_PR'])) + str(row['OPTION_TYP'])
    return final_url

def get_prev_day_data():
    
    file_path_for_predata = os.getcwd() + '/data_files/predata.json'
    with open(file_path_for_predata, 'r') as fp:
        predata = json.load(fp)

    prev_date = predata["prev_date"]
    prev_month = predata["prev_month"]
    prev_year = predata["prev_year"]
    
    return [prev_date,prev_month,prev_year]
    
def get_zerodha_instrument_csv():
    return pd.read_csv('https://api.kite.trade/instruments')

def get_expiry_date(df):
    df_exp_date = df.copy()
    df_exp_date = df_exp_date[(
        df_exp_date['segment'].str.contains("NFO-FUT") == True)]
    df_exp_date.drop(df_exp_date[df_exp_date['name']
                                 != 'NIFTY'].index, inplace=True)
    exp_date_zerodha = df_exp_date['expiry'].min()

    # adjustments for expiry week
    # LL = df_exp_date['expiry'].tolist()
    # exp_date_zerodha = LL[1]
    return exp_date_zerodha

def get_df_calls(df,exp_date_zerodha):
    df_calls = df.copy()
    df_calls = df_calls[(df_calls['segment'].str.contains("NFO-OPT") == True)]
    df_calls.drop(df_calls[df_calls['name'] == 'NIFTY'].index, inplace=True)
    df_calls.drop(df_calls[df_calls['name'] == 'BANKNIFTY'].index, inplace=True)
    df_calls.drop(df_calls[df_calls['name'] == 'FINNIFTY'].index, inplace=True)
    df_calls.drop(df_calls[df_calls['instrument_type'] != 'CE'].index, inplace=True)
    df_calls.drop(df_calls[df_calls['expiry'] !=
                exp_date_zerodha].index, inplace=True)
    df_calls['url'] = df_calls.apply(
        lambda row: create_url_for_options(row), axis=1)
    return df_calls

def get_df_puts(df,exp_date_zerodha):
    df_puts = df.copy()
    df_puts = df_puts[(df_puts['segment'].str.contains("NFO-OPT") == True)]
    df_puts.drop(df_puts[df_puts['name'] == 'NIFTY'].index, inplace=True)
    df_puts.drop(df_puts[df_puts['name'] == 'BANKNIFTY'].index, inplace=True)
    df_puts.drop(df_puts[df_puts['name'] == 'FINNIFTY'].index, inplace=True)
    df_puts.drop(df_puts[df_puts['instrument_type']
                 != 'PE'].index, inplace=True)
    df_puts.drop(df_puts[df_puts['expiry'] !=
                         exp_date_zerodha].index, inplace=True)
    df_puts['url'] = df_puts.apply(
        lambda row: create_url_for_options(row), axis=1)
    return df_puts

def get_bhavcopy(prev_year, prev_month, prev_date):
    temp_bc = bhavcopy_fo_save(date(prev_year, prev_month, prev_date), "")
    df_bc = pd.read_csv(temp_bc)
    os.remove(temp_bc)
    return df_bc

def get_stock_fut_zerodha(df,exp_date_zerodha):
    df_step_3 = df.copy()
    df_step_3 = df_step_3[(
        df_step_3['segment'].str.contains("NFO-FUT") == True)]
    df_step_3.drop(df_step_3[df_step_3['name'] == 'NIFTY'].index, inplace=True)
    df_step_3.drop(df_step_3[df_step_3['name'] =='BANKNIFTY'].index, inplace=True)
    df_step_3.drop(df_step_3[df_step_3['name'] =='FINNIFTY'].index, inplace=True)
    df_step_3.drop(df_step_3[df_step_3['expiry'] !=exp_date_zerodha].index, inplace=True)
    df_step_3.drop(df_step_3.columns[df_step_3.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    return df_step_3

def get_joined_df(df_bc,df_stock_fut_zerodha):    
    df_bc_stock_fut = df_bc.copy()
    df_bc_stock_fut.drop(df_bc_stock_fut[df_bc_stock_fut['INSTRUMENT'] != 'FUTSTK'].index, inplace=True) 
    # get element at index 1 for first day of new expiry
    # otherwise index 0
    dat = (list(df_bc_stock_fut.EXPIRY_DT.unique())[0])
    # print(dat)
    df_bc_stock_fut.drop(df_bc_stock_fut[df_bc_stock_fut['EXPIRY_DT'] != dat].index, inplace=True)
    df_bc_stock_fut.drop(['SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT',
                'CHG_IN_OI', 'TIMESTAMP'], axis=1, inplace=True)

    step_3_bearish = df_stock_fut_zerodha.copy()
    joined_bearish = pd.merge(df_bc_stock_fut, step_3_bearish,
                          left_on='SYMBOL', right_on='name')
    
    joined_bearish['P'] = joined_bearish.apply(lambda row: (
        row['HIGH'] + row['LOW'] + row['CLOSE']) / 3, axis=1)
    
    joined_bearish['R3'] = joined_bearish.apply(lambda row: (
        row['P'] + (1 * (row['HIGH'] - row['LOW']))), axis=1)
    
    joined_bearish['R2'] = joined_bearish.apply(lambda row: (
        row['P'] + (0.681 * (row['HIGH'] - row['LOW']))), axis=1)

    joined_bearish['R1'] = joined_bearish.apply(lambda row: (
        row['P'] + (0.381 * (row['HIGH'] - row['LOW']))), axis=1)
    
    joined_bearish['S2'] = joined_bearish.apply(lambda row: (
        row['P'] - (0.681 * (row['HIGH'] - row['LOW']))), axis=1)
    
    joined_bearish['S3'] = joined_bearish.apply(lambda row: (
        row['P'] - (1 * (row['HIGH'] - row['LOW']))), axis=1)
    
    joined_bearish.drop(joined_bearish.columns[joined_bearish.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    
    joined_bearish['url'] = joined_bearish.apply(
        lambda row: create_url_for_futures(row), axis=1)

    return joined_bearish

def create_eq_json(df,exp_date_zerodha):
    df_fut = df.copy()
    df_fut = df_fut[(
        df_fut['segment'].str.contains("NFO-FUT") == True)]
    df_fut.drop(df_fut[df_fut['name'] == 'NIFTY'].index, inplace=True)
    df_fut.drop(df_fut[df_fut['name'] ==
                       'BANKNIFTY'].index, inplace=True)
    df_fut.drop(df_fut[df_fut['name'] ==
                       'FINNIFTY'].index, inplace=True)
    df_fut.drop(df_fut[df_fut['expiry'] !=
                       exp_date_zerodha].index, inplace=True)
    df_fut.drop(df_fut.columns[df_fut.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    
    df_fut_for_join = df_fut.copy()
    df_fut_for_join = df_fut_for_join[['name']].copy()
    df_eq = df.copy()
    df_eq.drop(df_eq[df_eq['exchange'] != 'NSE'].index, inplace=True)
    df_eq.drop(df_eq[df_eq['segment'] != 'NSE'].index, inplace=True)
    df_eq.drop(df_eq[df_eq['instrument_type'] != 'EQ'].index, inplace=True)

    df_eq_for_join = df_eq.copy()

    joined_df_for_eq = pd.merge(df_fut_for_join, df_eq_for_join,
                                left_on='name', right_on='tradingsymbol')

    joined_df_for_eq.drop(['name_y', 'last_price', 'expiry', 'strike', 'tick_size', 'lot_size',
                          'instrument_type', 'segment', 'exchange', 'exchange_token'], axis=1, inplace=True)

    joined_df_for_eq.drop(joined_df_for_eq.columns[joined_df_for_eq.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)

    joined_df_for_eq['url'] = joined_df_for_eq.apply(
        lambda row: create_url_for_eq(row), axis=1)

    # joined_df_for_eq.to_csv("joined_df_for_eq.csv")

    stock_equity_name_url_dic = pd.Series(
        joined_df_for_eq.url.values, index=joined_df_for_eq.tradingsymbol).to_dict()


    file_path_for_eq = os.getcwd() + '/data_files/' + 'eq.json'
    with open(file_path_for_eq, 'w') as fp:
        json.dump(stock_equity_name_url_dic, fp)

    print('created eq.json')

def prepare_zerodha(df,exp_date_zerodha):
    df_opt = df.copy()
    df_opt = df_opt[(df_opt['segment'].str.contains("NFO-OPT") == True)]
    df_opt.drop(df_opt[df_opt['name'] == 'NIFTY'].index, inplace=True)
    df_opt.drop(df_opt[df_opt['name'] == 'BANKNIFTY'].index, inplace=True)
    df_opt.drop(df_opt[df_opt['name'] == 'FINNIFTY'].index, inplace=True)
    df_opt.drop(df_opt[df_opt['instrument_type'] != 'CE'].index, inplace=True)
    df_opt.drop(df_opt[df_opt['expiry'] !=
                exp_date_zerodha].index, inplace=True)
    df_opt['url'] = df_opt.apply(
        lambda row: create_url_for_options(row), axis=1)
    return df_opt

def prepare_bc(prev_year, prev_month, prev_date, exp_date_zerodha):
    # temp_bc = bhavcopy_fo_save(date(prev_year, prev_month, prev_date), "")
    # df_bc = pd.read_csv(temp_bc)
    # os.remove(temp_bc)
    # df_bc.drop(df_bc[df_bc['INSTRUMENT'] != 'OPTSTK'].index, inplace=True)
    # df_bc.drop(df_bc[df_bc['OPTION_TYP'] != 'CE'].index, inplace=True)
    # df_bc.drop(df_bc[df_bc['EXPIRY_DT'] !=exp_date_zerodha].index, inplace=True)
    # df_bc.drop(['SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT',
    #             'CHG_IN_OI', 'TIMESTAMP'], axis=1, inplace=True)
    # # hard coded for now
    # label_yr_month = "21NOV"
    # df_bc['CUSTOM_COL'] = df_bc.apply(lambda row: label_row(row,label_yr_month), axis=1)
    nse = Nse()
    dfbc = nse.bhavcopy_fno(dt.date(prev_year, prev_month, prev_date))
    dfbc.to_csv("local_file.csv")
    df_bc = pd.read_csv("local_file.csv")

    df_bc.drop(df_bc[df_bc['INSTRUMENT'] != 'OPTSTK'].index, inplace=True)
    df_bc.drop(df_bc[df_bc['OPTION_TYP'] != 'CE'].index, inplace=True)
    df_bc.drop(df_bc[df_bc['EXPIRY_DT'] !=exp_date_zerodha].index, inplace=True)
    df_bc.drop(['SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT',
                'CHG_IN_OI', 'TIMESTAMP'], axis=1, inplace=True)
    label_yr_month = "21NOV"
    df_bc['CUSTOM_COL'] = df_bc.apply(lambda row: label_row(row,label_yr_month), axis=1)
    return df_bc

def get_joined_df_for_calls(df_zerodha_for_calls,df_bc_for_calls):
    
    joined_df = pd.merge(df_zerodha_for_calls, df_bc_for_calls,
                            left_on='tradingsymbol', right_on='CUSTOM_COL')
    joined_df['P'] = joined_df.apply(lambda row: (
        row['HIGH'] + row['LOW'] + row['CLOSE']) / 3, axis=1)
    joined_df['R2'] = joined_df.apply(lambda row: (
        row['P'] + (0.618 * (row['HIGH'] - row['LOW']))), axis=1)
    joined_df['R3'] = joined_df.apply(lambda row: (
        row['P'] + (1 * (row['HIGH'] - row['LOW']))), axis=1)
    
    joined_df.drop(joined_df.columns[joined_df.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)

    # specific columns of joined df 
    df_step_2 = joined_df.copy()
    df_step_2 = df_step_2[['name', 'tradingsymbol','R2','R3',
                            'url', 'strike', 'instrument_token', 'instrument_type']].copy()
    df_step_2.drop(df_step_2.columns[df_step_2.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)

    return df_step_2
    
def fun():
    print("calling pre")
    
    # previous day data
    prev_day_list = get_prev_day_data()
    prev_date = prev_day_list[0]
    prev_month = prev_day_list[1]
    prev_year = prev_day_list[2]

    # zerodha instruemnt csv    
    df = get_zerodha_instrument_csv()
    print('downloaded zerodha instruemnt csv')


    # find expiry date 
    exp_date_zerodha = get_expiry_date(df)
    
    
    # df of calls
    df_calls = get_df_calls(df,exp_date_zerodha)   
    file_path_for_df_calls = os.getcwd() + '/data_files/' +  'df_calls.csv'
    df_calls.to_csv(file_path_for_df_calls)
    print('saved df_calls')
    
    
    # df of puts
    df_puts = get_df_puts(df,exp_date_zerodha)  
    file_path_for_df_puts = os.getcwd() + '/data_files/' +  'df_puts.csv'
    df_puts.to_csv(file_path_for_df_puts)
    print('saved df_puts')
    
    
    # stock futures from zerodha original
    df_stock_fut_zerodha = get_stock_fut_zerodha(df,exp_date_zerodha)
    file_path_for_df_stock_fut_zerodha = os.getcwd() + '/data_files/' + "df_stock_fut_zerodha.csv"
    df_stock_fut_zerodha.to_csv(file_path_for_df_stock_fut_zerodha)
    print('saved df_stock_fut_zerodha')
    
    
    # bhavcopy
    df_bc = get_bhavcopy(prev_year, prev_month, prev_date)
    
        
    # get joined df of stock futures
    joined =  get_joined_df(df_bc,df_stock_fut_zerodha)
    file_path_for_df_joined = os.getcwd() + '/data_files/' +  "joined.csv"
    joined.to_csv(file_path_for_df_joined)
    print('saved joined bearish')
    
    
    # equity
    create_eq_json(df,exp_date_zerodha)



    # stock options with fib levels 
    df_zerodha_for_calls = prepare_zerodha(df,exp_date_zerodha)
    print('saved df_zerodha_for_calls')
    df_bc_for_calls = prepare_bc(prev_year, prev_month, prev_date,exp_date_zerodha)
    file_path_for_joined_df_for_calls = os.getcwd() + '/data_files/' +  "joined_df_for_calls.csv"
    joined_df_for_calls = get_joined_df_for_calls(df_zerodha_for_calls,df_bc_for_calls)
    joined_df_for_calls.to_csv(file_path_for_joined_df_for_calls)
    print('saved joined_df_for_calls')

    
# fun()
