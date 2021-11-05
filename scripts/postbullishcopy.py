
# def get_bullish_dic():
#     global bullish_dic
#     bullish_dic = {}
#     df_step_3 = pd.read_csv("df_step_3.csv")
#     df_joined_bearish = pd.read_csv("joined.csv")

#     '''
#     part 1
#     '''
#     now = datetime.now()

#     with open('data.json', 'r') as fp:
#         data = json.load(fp)
#     access_token = data["accesstoken"]

#     fut_symbol_list = df_step_3['tradingsymbol'].tolist()
#     future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
#     for symbol in fut_symbol_list:
#         temp = symbol.replace("&", "%26")
#         symbol = temp
#         future_string = future_string + "i=NFO:" + symbol + "&"
#     future_string = future_string[:-1]

#     r = requests.get(future_string, timeout=10)
#     data = (r.json())
#     dic = data['data']

#     '''
#     part 2
#     '''
#     # now = datetime.now()
#     temp = df_joined_bearish.copy()
#     for i in dic.keys():
#         d = list(dic[i].values())
#         token = d[0]
#         ltp = d[1]
#         temp.loc[temp.instrument_token == token, 'last_price'] = ltp
#     df_step_4 = temp.copy()

#     df_step_4['checker'] = df_step_4.apply(lambda row: int(float(row.last_price)) > int(
#         float(row.R1)), axis=1)

#     df_step_5 = df_step_4.copy()
#     df_step_5.drop(df_step_5[df_step_5['checker']
#                    == False].index, inplace=True)

#     stock_name_url_dic = pd.Series(
#         df_step_5.url.values, index=df_step_5.name).to_dict()

#     bullish_stocks = list(stock_name_url_dic.keys())

#     # bullish_dic = {}
#     # for i in bullish_stocks:
#     #     bullish_dic[i] = find_highest_volume_strike(i)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(find_highest_volume_strike, bullish_stocks)

#     then = datetime.now()
#     timetaken = then - now
#     print("time taken ", timetaken.total_seconds())
#     return bullish_dic

# def bullish_stocks_r3():
#     global bullish_dic2
#     bullish_dic2 = {}
#     df_step_3 = pd.read_csv("df_step_3.csv")
#     df_joined_bearish = pd.read_csv("joined.csv")

#     '''
#     part 1
#     '''
#     now = datetime.now()

#     with open('data.json', 'r') as fp:
#         data = json.load(fp)
#     access_token = data["accesstoken"]

#     fut_symbol_list = df_step_3['tradingsymbol'].tolist()
#     future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
#     for symbol in fut_symbol_list:
#         temp = symbol.replace("&", "%26")
#         symbol = temp
#         future_string = future_string + "i=NFO:" + symbol + "&"
#     future_string = future_string[:-1]

#     r = requests.get(future_string, timeout=10)
#     data = (r.json())
#     dic = data['data']

#     '''
#     part 2
#     '''
#     # now = datetime.now()
#     temp = df_joined_bearish.copy()
#     for i in dic.keys():
#         d = list(dic[i].values())
#         token = d[0]
#         ltp = d[1]
#         temp.loc[temp.instrument_token == token, 'last_price'] = ltp
#     df_step_4 = temp.copy()

#     df_step_4['checker'] = df_step_4.apply(lambda row: int(float(row.last_price)) > int(
#         float(row.R3)), axis=1)

#     df_step_5 = df_step_4.copy()
#     df_step_5.drop(df_step_5[df_step_5['checker']
#                    == False].index, inplace=True)

#     stock_name_url_dic = pd.Series(
#         df_step_5.url.values, index=df_step_5.name).to_dict()

#     bullish_stocks = list(stock_name_url_dic.keys())

#     # bullish_dic = {}
#     # for i in bullish_stocks:
#     #     bullish_dic[i] = find_highest_volume_strike(i)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(find_highest_volume_strike2, bullish_stocks)

#     then = datetime.now()
#     timetaken = then - now
#     print("time taken ", timetaken.total_seconds())

#     return bullish_dic2


# # bullish_stocks_r3()


# bullish_dic = {}
# bullish_dic2 = {}


# def find_highest_volume_strike(name):
#     df_step_2 = pd.read_csv("df_step_2.csv")
#     api_key = "a4wntz8ych7zc40h"

#     df2 = df_step_2.copy()
#     df2 = df2.loc[df2['name'] == name]
#     sorted_df = df2.sort_values(by=['strike'])

#     opt_symbol_list = sorted_df['tradingsymbol'].tolist()
#     opt_symbol_list_new = []
#     for symbol in opt_symbol_list:
#         opt_symbol_list_new.append("NFO:" + symbol)

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
#             strike = i
#             max_vol = l
#             instrument_token = str(dd[i]['instrument_token'])

#     sym = strike.replace("NFO:", "")
#     strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
#         sym + "/" + instrument_token
#     # return strike_url
#     bullish_dic[name] = strike_url


# def find_option_strike_helper(name):
#     df_step_2 = pd.read_csv("df_step_2.csv")
#     api_key = "a4wntz8ych7zc40h"

#     df2 = df_step_2.copy()
#     df2 = df2.loc[df2['name'] == name]
#     sorted_df = df2.sort_values(by=['strike'])

#     opt_symbol_list = sorted_df['tradingsymbol'].tolist()
#     opt_symbol_list_new = []
#     for symbol in opt_symbol_list:
#         opt_symbol_list_new.append("NFO:" + symbol)

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
#             strike = i
#             max_vol = l
#             instrument_token = str(dd[i]['instrument_token'])

#     sym = strike.replace("NFO:", "")
#     strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
#         sym + "/" + instrument_token
#     return strike_url
#     # bullish_dic[name] = strike_url


# def find_option_strike(option_strike):
#     output_dic = {}
#     output_dic[option_strike] = find_option_strike_helper(option_strike)
#     return output_dic


# def find_put_option_strike_helper(name):
#     df_step_2 = pd.read_csv("df_puts.csv")
#     api_key = "a4wntz8ych7zc40h"

#     df2 = df_step_2.copy()
#     df2 = df2.loc[df2['name'] == name]
#     sorted_df = df2.sort_values(by=['strike'])

#     opt_symbol_list = sorted_df['tradingsymbol'].tolist()
#     opt_symbol_list_new = []
#     for symbol in opt_symbol_list:
#         opt_symbol_list_new.append("NFO:" + symbol)

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
#             strike = i
#             max_vol = l
#             instrument_token = str(dd[i]['instrument_token'])

#     sym = strike.replace("NFO:", "")
#     strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
#         sym + "/" + instrument_token
#     return strike_url
#     # bullish_dic[name] = strike_url


# def find_put_option_strike(option_strike):
#     output_dic = {}
#     output_dic[option_strike] = find_put_option_strike_helper(option_strike)
#     return output_dic


# def find_highest_volume_strike2(name):
#     df_step_2 = pd.read_csv("df_step_2.csv")
#     api_key = "a4wntz8ych7zc40h"

#     df2 = df_step_2.copy()
#     df2 = df2.loc[df2['name'] == name]
#     sorted_df = df2.sort_values(by=['strike'])

#     opt_symbol_list = sorted_df['tradingsymbol'].tolist()
#     opt_symbol_list_new = []
#     for symbol in opt_symbol_list:
#         opt_symbol_list_new.append("NFO:" + symbol)

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
#             strike = i
#             max_vol = l
#             instrument_token = str(dd[i]['instrument_token'])

#     sym = strike.replace("NFO:", "")
#     strike_url = 'https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/' + \
#         sym + "/" + instrument_token
#     # return strike_url
#     bullish_dic2[name] = strike_url


# # r1
# # r2
# # r3

# def bullish_stocks_r1():
#     global bullish_dic2
#     bullish_dic2 = {}

#     df_step_3 = pd.read_csv("df_step_3.csv")
#     df_joined_bearish = pd.read_csv("joined.csv")

#     '''
#     part 1
#     '''
#     now = datetime.now()

#     with open('data.json', 'r') as fp:
#         data = json.load(fp)
#     access_token = data["accesstoken"]

#     fut_symbol_list = df_step_3['tradingsymbol'].tolist()
#     future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
#     for symbol in fut_symbol_list:
#         temp = symbol.replace("&", "%26")
#         symbol = temp
#         future_string = future_string + "i=NFO:" + symbol + "&"
#     future_string = future_string[:-1]

#     r = requests.get(future_string, timeout=10)
#     data = (r.json())
#     dic = data['data']

#     '''
#     part 2
#     '''
#     # now = datetime.now()
#     temp = df_joined_bearish.copy()
#     for i in dic.keys():
#         d = list(dic[i].values())
#         token = d[0]
#         ltp = d[1]
#         temp.loc[temp.instrument_token == token, 'last_price'] = ltp
#     df_step_4 = temp.copy()

#     df_step_4['checker'] = df_step_4.apply(
#         lambda row:
#             int(float(row.last_price)) > int(float(row.R1))
#             and
#             int(float(row.last_price)) < int(float(row.R2)), axis=1)

#     df_step_5 = df_step_4.copy()
#     df_step_5.drop(df_step_5[df_step_5['checker']
#                    == False].index, inplace=True)

#     stock_name_url_dic = pd.Series(
#         df_step_5.url.values, index=df_step_5.name).to_dict()

#     bullish_stocks = list(stock_name_url_dic.keys())

#     # bullish_dic = {}
#     # for i in bullish_stocks:
#     #     bullish_dic[i] = find_highest_volume_strike(i)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(find_highest_volume_strike2, bullish_stocks)

#     then = datetime.now()
#     timetaken = then - now
#     print("time taken ", timetaken.total_seconds())
#     return bullish_dic2


# def bullish_stocks_r2():
#     global bullish_dic2
#     bullish_dic2 = {}
#     df_step_3 = pd.read_csv("df_step_3.csv")
#     df_joined_bearish = pd.read_csv("joined.csv")

#     '''
#     part 1
#     '''
#     now = datetime.now()

#     with open('data.json', 'r') as fp:
#         data = json.load(fp)
#     access_token = data["accesstoken"]

#     fut_symbol_list = df_step_3['tradingsymbol'].tolist()
#     future_string = f"https://api.kite.trade/quote/ltp?api_key={api_key}&access_token={access_token}&"
#     for symbol in fut_symbol_list:
#         temp = symbol.replace("&", "%26")
#         symbol = temp
#         future_string = future_string + "i=NFO:" + symbol + "&"
#     future_string = future_string[:-1]

#     r = requests.get(future_string, timeout=10)
#     data = (r.json())
#     dic = data['data']

#     '''
#     part 2
#     '''
#     # now = datetime.now()
#     temp = df_joined_bearish.copy()
#     for i in dic.keys():
#         d = list(dic[i].values())
#         token = d[0]
#         ltp = d[1]
#         temp.loc[temp.instrument_token == token, 'last_price'] = ltp
#     df_step_4 = temp.copy()

#     df_step_4['checker'] = df_step_4.apply(
#         lambda row:
#             int(float(row.last_price)) > int(float(row.R2))
#             and
#             int(float(row.last_price)) < int(float(row.R3)), axis=1)

#     df_step_5 = df_step_4.copy()
#     df_step_5.drop(df_step_5[df_step_5['checker']
#                    == False].index, inplace=True)

#     stock_name_url_dic = pd.Series(
#         df_step_5.url.values, index=df_step_5.name).to_dict()

#     bullish_stocks = list(stock_name_url_dic.keys())

#     # bullish_dic = {}
#     # for i in bullish_stocks:
#     #     bullish_dic[i] = find_highest_volume_strike(i)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(find_highest_volume_strike2, bullish_stocks)

#     then = datetime.now()
#     timetaken = then - now
#     print("time taken ", timetaken.total_seconds())
#     return bullish_dic2


# def quote_dic():

#     # api key
#     config = configparser.ConfigParser()
#     config.read('credential.ini')
#     api_key = config['kite']['api_key']

#     # access token
#     with open('data.json', 'r') as fp:
#         data = json.load(fp)
#     access_token = data["accesstoken"]

#     # kite object
#     kite = KiteConnect(api_key=api_key)
#     kite.set_access_token(access_token=access_token)

#     # equity list
#     with open('eq.json', 'r') as fp:
#         eq_url_dic = json.load(fp)
#     equity_list = list(eq_url_dic.keys())
#     equity_list_quote_format_list = ['NSE:{}'.format(i) for i in equity_list]

#     # api call for quote
#     qd = kite.quote(equity_list_quote_format_list)
#     return qd


# def open_high_low():
#     # get quote
#     dd = quote_dic()

#     # stock:url dictionary
#     with open('eq.json', 'r') as fp:
#         eq_url_dic = json.load(fp)

#     # open == high
#     name_open_equal_high = {}
#     li = list(dd.keys())
#     for i in li:
#         o = (dd[i]['ohlc']['open'])
#         h = (dd[i]['ohlc']['high'])
#         i = i.replace("NSE:", "")
#         if o == h:
#             name_open_equal_high[i] = [round((float(((o-h)/h)*100)), 2)]

#     # open == low
#     name_open_equal_low = {}
#     li = list(dd.keys())
#     for i in li:
#         o = (dd[i]['ohlc']['open'])
#         l = (dd[i]['ohlc']['low'])
#         i = i.replace("NSE:", "")
#         if o == l:
#             name_open_equal_low[i] = [round((float(((o-l)/l)*100)), 2)]

#     name_url_dic_open_equal_high = {}
#     for i in name_open_equal_high.keys():
#         name_url_dic_open_equal_high[i] = eq_url_dic[i]

#     name_url_dic_open_equal_low = {}
#     for i in name_open_equal_low.keys():
#         name_url_dic_open_equal_low[i] = eq_url_dic[i]

#     lis_open_high_low = [name_url_dic_open_equal_high,
#                          name_url_dic_open_equal_low]

#     return lis_open_high_low
