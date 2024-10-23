import json 
import requests
from datetime import timedelta, datetime, date
import pandas as pd 
from io import BytesIO, StringIO
from urllib.request import urlopen
import base64
from pip import main
from sqlalchemy import create_engine

from mysqlconnection.connection import *
import os

main(['install', 'python-dotenv'])
from dotenv import load_dotenv

main(['install', 'mysql-connector-python'])
from mysql.connector import *

url = 'https://api.coinpaprika.com/v1/coins'

headers = {
    'Content-Type' : 'application/json'
}

response = requests.get(url, headers)
print(response.status_code)
print(response.headers)

u = BytesIO(response.content)
u.seek(0)
cont = u.read()
decoded_string = cont.decode('utf-8', errors='ignore')
with open('cryptocurrencies.txt', 'a', encoding='utf-8') as f:
    f.write(decoded_string)

### Response cleaning 
### BY WILLIAM  BAKEN6

json_load = json.loads(decoded_string)
print(type(json_load))
# print(json_load[0:30])

data = pd.DataFrame(json_load[0:50])
print(data.head(10))

data.to_csv('cryptocurrencies.csv', index=True)

###     Get API Key informations

names = list(data["id"])
print(names)
now = date.today()
last_year = now - timedelta(days=362)
str_last_year = last_year.strftime("%Y-%m-%d")
print(str_last_year)
df = pd.DataFrame()

for name in names:
    url = 'https://api.coinpaprika.com/v1/tickers/{name}/historical?start={last_year}&interval=1d'.format(name=name
        , last_year=str_last_year
    )
    response = requests.get(url)
    print(response.status_code)
    w = BytesIO(response.content)
    w.seek(0)
    contenu = w.read()
    cont_text = contenu.decode('utf-8', errors='ignore')
    json_data = json.loads(cont_text)
    df1 = pd.DataFrame(json_data)
    df1["name"] = name
    df = pd.concat([df, df1])

full_data = df
full_data.to_csv('marketprice.csv', index=True)

load_dotenv()

username = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
DB = os.getenv("database")
port = os.getenv("port")

engine = create_engine("mysql+pymysql://{username}:{password}@{host}/{database}".format(
    username=username,
    password=password,
    host=host,
    port=port,
    database=DB
))


connection = connection(host, DB, username, password)

# data.to_sql(name='currency_name', con=engine, if_exists='replace')
## DROP TABLE

drop_table = """DROP TABLE IF EXISTS `coinlist`"""

curse(connection, drop_table)

sql = """ CREATE TABLE IF NOT EXISTS `coinlist` (
    `name_id` varchar(50) NOT NULL,
    `name` varchar(50) NOT NULL,
    `symbol` varchar(10) NOT NULL,
    `rank` int(5),
    `is_new` boolean,  
    `is_active` boolean,
    `type` varchar(20)
) """

curse(connection, sql)

add_coin = """INSERT INTO `coinlist` (`name_id`, `name`, `symbol`, `rank`, `is_new`, `is_active`, `type`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
header = data.values.tolist()
# print(header)

cursemany(connection, add_coin, header)

### ADD THE SECOND DATA

prices = pd.read_csv('marketprice.csv', header=1)
print(prices.head(10))

drop_table = """DROP TABLE IF EXISTS `marketprice`"""

curse(connection, drop_table)

sql = """ CREATE TABLE IF NOT EXISTS `marketprice` (
    `line` int(30) NOT NULL,
    `date` varchar(30) NOT NULL,
    `price` float(11, 4),
    `volume` varchar(40),
    `marketcap` varchar(40),
    `name` varchar(30)
) """

curse(connection, sql)

add_price = """INSERT INTO `marketprice` (`line`, `date`, `price`, `volume`, `marketcap`, `name`) 
    VALUES (%s, %s, %s, %s, %s, %s)
"""
header2 = prices.values.tolist()
# print(header2)

cursemany(connection, add_price, header2)
