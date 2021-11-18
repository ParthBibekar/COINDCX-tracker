import pandas as pd
from matplotlib import pyplot as plt
import hmac
import hashlib
import base64
import json
import time
import requests
from datetime import datetime
from tabulate import tabulate
import csv

investment = 00.00
coindcx = json.load(open('./api.json'))
key = coindcx['apikey']
secret = coindcx['secretkey']
common_url = "https://api.coindcx.com/exchange"

secret_bytes = bytes(secret, encoding='utf-8')
timeStamp = int(round(time.time() * 1000))
body = {
    "timestamp": timeStamp
}
json_body = json.dumps(body, separators = (',', ':'))
signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
url = common_url + "/v1/users/balances"
ret = {}
headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

def getbalance():
    global df
    global myINR
    global myUSDT
    df = pd.DataFrame()
    
    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()

    for i in data:
        if i['balance'] != '0.0':
            #print(i)
            df = df.append(i,ignore_index=True)
        if i['currency'] == 'INR':
            myINR = i['balance']
        if i['currency'] == 'USDT':
            myUSDT = i['balance']

    return(df)

getbalance()
searchfor = ['INR', 'USDT']
df = df[~df.currency.str.contains('|'.join(searchfor))]
df = df.reset_index()
del df['index']
df['currency'] = df['currency'].astype(str) + 'USDT'        
coins = df['currency'].values.tolist()

last_price = []
market_coin = []

def currentPrice():
    global usdtToinr
    global df2
    df2 = pd.DataFrame()
    url = common_url + "/ticker"
    response = requests.get(url)
    data = response.json()
                 
    for i in data:
        for j in coins:
            if j == i['market']:
                last_price.append(i['last_price'])
                market_coin.append(i['market'])
                #print(i["market"],i["last_price"])
    df2['currency'] = market_coin
    df2['Current price(USDT)'] = last_price           

    for i in data:
        if 'USDTINR' == i['market']:
            usdtToinr = i['last_price']

currentPrice()  
df = df.sort_values(by='currency')
df = df.reset_index()
df2 = df2.sort_values('currency')   
df2 = df2.reset_index()      
del df['index']
del df2['index']
df['Current price(USDT)'] = df2['Current price(USDT)']
df['balance'] = df['balance'].astype(float)
df['Current price(USDT)'] = df['Current price(USDT)'].astype(float)
df['Asset value(USDT)'] = df['balance']*df['Current price(USDT)']
usdtToinr = float(usdtToinr)
df['Asset value(INR)'] = df['Asset value(USDT)']*usdtToinr

coins = df['currency'].values.tolist()
for i in range(len(coins)):
    coins[i] = coins[i].replace('USDT','')
    
df['currency'] = coins
df = df[['currency','locked_balance','balance','Current price(USDT)','Asset value(USDT)','Asset value(INR)']]
myINR = float(myINR)
myUSDT = float(myUSDT)
Total_usdt = float(df['Asset value(USDT)'].sum()) + myUSDT + myINR*usdtToinr
Total_inr = float(df['Asset value(INR)'].sum()) + myINR + myUSDT/usdtToinr
print(tabulate(df, headers='keys', tablefmt='psql',showindex=False))
print("\nINR in the wallet: ",myINR)
print("USDT in the wallet: ",myUSDT)
print("\nTotal portfolio value(USDT): ",Total_usdt)
print("Total portfolio value(INR): ",Total_inr,"\n")
profit = Total_inr - investment
print("\nTotal profit: ",profit)

def today_profit():
    profit = Total_inr - investment
    profit = int(profit)
    x = datetime.now()
    data = (str(x.strftime("%d-%b-%Y")),str(profit))
    with open('coindcx_log.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    column_names = ["Date", "Profit"]
    data= pd.read_csv("coindcx_log.csv",names=column_names)
    dates = data.Date.tolist()
    profits = data.Profit.tolist()
    plt.plot(dates,profits)
    plt.xlabel("Date")
    plt.ylabel("Profit(INR)")
    plt.show()

today_profit()
