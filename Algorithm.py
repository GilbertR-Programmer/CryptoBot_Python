
from dotenv import load_dotenv
import time
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


def checkCurrency(currency):
	paymentOptions = ["BNB", "BTC", "ETH"]
	symbol = ""
	for payment in paymentOptions:
		if(TestTrade(currency + payment)):
			symbol = currency + payment
			break
	print(symbol)

def TestTrade(paymentMethod):
	try:
		checkTrade = client.get_symbol_ticker(symbol=paymentMethod)
	except BinanceAPIException as e:
		print(e)
		return False
	return True

def beginTrading(tradeSymbol, targetedCurrencySymbol, originCurrencySymbol):
	buyInPrice = 0
	originCurrencyAvailable = client.get_asset_balance(asset=originCurrencySymbol)['free']
	originCurrencyAvailable = float(originCurrencyAvailable)*0.45
	i = 0
	while (client.get_asset_balance(asset=targetedCurrencySymbol) is type(None)):
		if(i>0):
			print('allo')
		buyInPrice = client.get_ticker(symbol=tradeSymbol)['askPrice']
		try:
			
   			buy_order = client.order_limit_buy(
				symbol=tradeSymbol,
				quantity=originCurrencyAvailable/buyInPrice,
				price=buyInPrice,
			)
			

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		time.sleep(1)
		i += 1
		print(buy_order['orderId'])


beginTrading("EOSETH","EOS","ETH")


# get latest price from Binance API
#ETHGBP_price = 0
#try:
#	ETHGBP_price = client.get_symbol_ticker(symbol='GARBUTP')
#except BinanceAPIException as e:
	# error handling goes here
#	print(e)

#print(ETHGBP_price)
# print full output (dictionary)
# print(ETHUSD_price)
#print(ETHBTC_price)


#print('before buying balance of btc:',client.get_asset_balance(asset='BTC'))
#print('before buying balance of eth:',client.get_asset_balance(asset='ETH'))
# print just the price
# print('ethereum price in USD is',ETHUSD_price['price'])
# print('ethereum price in GBP is',ETHGBP_price['price'])

# make a test order first. This will raise an exception if the order is incorrect.
#while True:
	#print('Sell Price')
	#HOW MUCH YOU GET FOR SELLING
	#print(client.get_symbol_ticker(symbol='ETHBTC')['price'])
	#print()
	#time.sleep(1)
	#print('Buy Price')
	#HOW MUCH YOU NEED TO PAY TO BUY
	#print(client.get_ticker(symbol='ETHBTC')['askPrice'])

#print(client.get_ticker(symbol='ETHBTC'))	

#try:
	#time.sleep(10)
#	print('howdy')
   #buy_order = client.order_market_sell(
	#	symbol='ETHBTC',
	#	quantity=1
	#)

#except BinanceAPIException as e:
	# error handling goes here
#	print(e)
#except BinanceOrderException as e:
	# error handling goes here
#	print(e)

#print('after buying balance of btc:',client.get_asset_balance(asset='BTC'))
#print('after buying balance of eth:',client.get_asset_balance(asset='ETH'))
#print(client.get_asset_balance(asset='EOS')['free'])
print(client.get_account())