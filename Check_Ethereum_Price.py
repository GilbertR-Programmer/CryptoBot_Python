
from dotenv import load_dotenv
load_dotenv()

import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

# init
api_key = os.getenv('TEST_API_KEY')
api_secret = os.getenv('TEST_API_SECRET')

client = Client(api_key, api_secret)
#this sets it to the binance test area
client.API_URL = 'https://testnet.binance.vision/api'
## main

# get latest price from Binance API

ETHBTC_price = client.get_symbol_ticker(symbol='ETHBTC')
#ETHGBP_price = client.get_symbol_ticker(symbol='ETHGBP')
# print full output (dictionary)
# print(ETHUSD_price)
print(ETHBTC_price)
# print just the price
# print('ethereum price in USD is',ETHUSD_price['price'])
# print('ethereum price in GBP is',ETHGBP_price['price'])

# make a test order first. This will raise an exception if the order is incorrect.
try:
   #buy_order_limit = client.create_order(
    #    symbol='ETHBTC',
	#    side='BUY',
	#    type='LIMIT',
	#    quantity=1,
	#    price=ETHBTC_price['price']
    #)

except BinanceAPIException as e:
	# error handling goes here
	print(e)
except BinanceOrderException as e:
	# error handling goes here
	print(e)

#print(client.get_account())