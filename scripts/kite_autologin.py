from selenium import webdriver
from kiteconnect import KiteConnect
import time
import os
import urllib.parse as urlparse
import json

import configparser
config = configparser.ConfigParser()

file_path_for_credentials = os.getcwd() + '/data_files/' + 'credential.ini'
config.read(file_path_for_credentials)

api_key = config['kite']['api_key']
api_secret = config['kite']['api_secret']
user = config['kite']['username']
passw = config['kite']['password']
two_fa = int(config['kite']['two_fa'])

path = r'C:\Users\91956\AppData\Local\Programs\Python\Python39\chromedriver'

def autologin():
    kite = KiteConnect(api_key=api_key)
    '''


    '''
    service = webdriver.chrome.service.Service(path)
    service.start()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')

    options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url, options)

    '''


    '''
    driver.get(kite.login_url())
    driver.implicitly_wait(10)
    username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    time.sleep(1)
    password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
    username.send_keys(user)
    password.send_keys(passw)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
    time.sleep(1)
    pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
    pin.send_keys(two_fa)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(3)
    current_url = driver.current_url
    parsed = urlparse.urlparse(current_url)
    '''


    '''
    request_token = urlparse.parse_qs(parsed.query)['request_token'][0]
    data = kite.generate_session(request_token=request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    ac = data["access_token"]
    di = dict()
    di['accesstoken'] = ac
    
    file_path_for_data = os.getcwd() + '/data_files/data.json'
    with open(file_path_for_data, 'w') as fp:
        json.dump(di, fp)
    driver.quit()
    print('access token generated')

# autologin()
























# def autologin():
#     from selenium import webdriver
#     from kiteconnect import KiteConnect
#     import time
#     import os
#     import urllib.parse as urlparse
#     import json


#     import configparser
#     config = configparser.ConfigParser()
#     config.read('credential.ini')
#     api_key = config['kite']['api_key']
#     api_secret = config['kite']['api_secret']
#     user = config['kite']['username']
#     passw = config['kite']['password']
#     two_fa = int(config['kite']['two_fa'])


#     '''
#     options = webdriver.ChromeOptions()
#     options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-sh-usage')
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options = options.to_capabilities()

#     driver = webdriver.Chrome(executable_path=os.environ.get(
#         "CHROMEDRIVER_PATH"), options=options)
#     '''

#     path = os.environ.get("CHROMEDRIVER_PATH")
#     service = webdriver.chrome.service.Service(path)
#     service.start()
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_argument('--headless')
#     options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-sh-usage')
#     options = options.to_capabilities()
#     driver = webdriver.Remote(service.service_url, options)


#     # driver.get("https://www.youtube.com/")
#     # print(driver.page_source)


#     kite = KiteConnect(api_key=api_key)
#     driver.get(kite.login_url())
#     driver.implicitly_wait(10)
#     username = driver.find_element_by_xpath(
#         '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
#     time.sleep(3)
#     password = driver.find_element_by_xpath(
#         '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
#     username.send_keys(user)
#     password.send_keys(passw)
#     driver.find_element_by_xpath(
#         '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
#     time.sleep(3)
#     pin = driver.find_element_by_xpath(
#         '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
#     pin.send_keys(two_fa)
#     driver.find_element_by_xpath(
#         '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
#     time.sleep(3)
#     current_url = driver.current_url
#     parsed = urlparse.urlparse(current_url)
#     '''
#     '''
#     request_token = urlparse.parse_qs(parsed.query)['request_token'][0]
#     # print(request_token)
#     data = kite.generate_session(
#         request_token=request_token, api_secret=api_secret)
#     kite.set_access_token(data["access_token"])
#     ac = data["access_token"]
#     di = dict()
#     di['accesstoken'] = ac
#     print(di)
#     with open('data.json', 'w') as fp:
#         json.dump(di, fp)
#     driver.quit()
#     print('access token generated')
















# from kiteconnect import KiteConnect
# from selenium import webdriver
# import time
# import os
# import urllib.parse as urlparse
# import json

# import configparser
# config = configparser.ConfigParser()
# config.read('credential.ini')

# api_key = config['kite']['api_key']
# api_secret = config['kite']['api_secret']
# user = config['kite']['username']
# passw = config['kite']['password']
# two_fa = int(config['kite']['two_fa'])

# path = r'C:\Users\91956\AppData\Local\Programs\Python\Python39\chromedriver'

# def autologin():
#     kite = KiteConnect(api_key=api_key)
#     '''
    
    
    
#     '''
#     service = webdriver.chrome.service.Service(path)
#     service.start()
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_argument('--headless')
#     options = options.to_capabilities()
#     driver = webdriver.Remote(service.service_url, options)
    
#     '''
    
    
#     '''
#     driver.get(kite.login_url())
#     driver.implicitly_wait(10)
#     username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
#     time.sleep(3)
#     password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
#     username.send_keys(user)
#     password.send_keys(passw)
#     driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
#     time.sleep(3)
#     pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
#     pin.send_keys(two_fa)
#     driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
#     time.sleep(3)
#     current_url = driver.current_url
#     parsed = urlparse.urlparse(current_url)
#     '''
    
    
    
#     '''
#     request_token = urlparse.parse_qs(parsed.query)['request_token'][0]
#     # print(request_token)
#     data = kite.generate_session(request_token=request_token, api_secret=api_secret)
#     kite.set_access_token(data["access_token"])
#     ac = data["access_token"]
#     di = dict()
#     di['accesstoken'] = ac
#     # print(di)
#     with open('data.json', 'w') as fp:
#         json.dump(di, fp)
#     driver.quit()
#     print('access token generated')
    
# # autologin()


