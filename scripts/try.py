# import concurrent
# from numpy.core.arrayprint import printoptions
# from requests.api import get
# import configparser
# from abc import abstractstaticmethod
# import json
# from kiteconnect import KiteConnect
# import pandas as pd
# import requests
# from datetime import datetime
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# import collections

# config = configparser.ConfigParser()
# config.read('credential.ini')
# api_key = config['kite']['api_key']

# with open('data.json', 'r') as fp:
#     data = json.load(fp)
# access_token = data["accesstoken"]

# output_dic = {}

# def find_highest_volume_strike(name):
#     df_step_2 = pd.read_csv("df_step_2.csv")
#     df2 = df_step_2.copy()
#     df2 = df2.loc[df2['name'] == name]
#     sorted_df = df2.sort_values(by=['strike'])

#     opt_symbol_list = sorted_df['tradingsymbol'].tolist()

#     # took 18 sec
#     opt_symbol_list_new = ['NFO:{}'.format(i) for i in opt_symbol_list]

#     # opt_symbol_list_new = []
#     # for symbol in opt_symbol_list:
#     #     opt_symbol_list_new.append("NFO:" + symbol)

#     kite = KiteConnect(api_key=api_key)
#     kite.set_access_token(access_token=access_token)
#     dd = kite.quote(opt_symbol_list_new)
#     li = list(dd.keys())
#     max_vol = 0
#     strike = ""
#     instrument_token = ""
#     for i in li:
#         l = (dd[i]['volume'])
#         if(l > max_vol):
#             max_vol = l
#             strike = i
#             instrument_token = str(dd[i]['instrument_token'])

#     l = (dd[strike]['last_price'])
#     p = (dd[strike]['ohlc']['close'])
#     net_change = round((float(((l-p)/p)*100)), 2)
#     strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
#         strike.replace("NFO:", "") + "/" + instrument_token

#     # if(net_change > 200):
#     #     print(strike_url)
    
#     output_dic[name] = [net_change,strike_url]

# def fun(option_strike):
#     df_step_3 = pd.read_csv("df_step_3.csv")
#     fut_symbol_list = df_step_3['name'].tolist()
#     now = datetime.now()

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(find_highest_volume_strike, fut_symbol_list)

#     then = datetime.now()
#     timetaken = then - now
#     print("time taken is ", timetaken.total_seconds())
#     return output_dic[option_strike]


# # fun()
# # pp.pprint(output_dic)
# # for k,v in output_dic.items():
# #     print(v[1])

# # pp.pprint(output_dic['IDFCFIRSTB'])
