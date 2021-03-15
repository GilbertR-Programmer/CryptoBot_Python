
#Written by Treblig. 

from dotenv import load_dotenv
from decimal import Decimal
import time
import math
load_dotenv()

import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

# init
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

client = Client(api_key, api_secret)
#this sets it to the binance test area
#client.API_URL = 'https://testnet.binance.vision/api'
## main


def checkCurrency(currency):
	paymentOptions = ["BNB", "BTC"]
	symbol = ""
	origin = ""
	for payment in paymentOptions:
		if(testTrade(currency + payment)):
			symbol = currency + payment
			origin = payment
			beginTrading(symbol,currency,origin)
			break

def testTrade(paymentMethod):
	try:
		checkTrade = client.get_symbol_ticker(symbol=paymentMethod)
	except BinanceAPIException as e:
		print(e)
		return False
	return True

def beginTrading(tradeSymbol, targetedCurrencySymbol, originCurrencySymbol):
	buyInPrice = 0
	purchaseQuantity = 0
	originCurrencyAvailable = client.get_asset_balance(asset=originCurrencySymbol)['free']
	originCurrencyAvailable = Decimal(originCurrencyAvailable) * Decimal(0.9)
	i = 0
	precision = int(client.get_symbol_info(symbol=tradeSymbol)['baseAssetPrecision'])
	stepSize = Decimal(client.get_symbol_info(symbol=tradeSymbol)['filters'][2]['stepSize'])
	
	while (i == 0):
		if(i>0):
			print('allo')
		
		try:
			buyInPrice = Decimal(client.get_ticker(symbol=tradeSymbol)['askPrice'])
			purchaseQuantity = originCurrencyAvailable/buyInPrice
			availableSteps = math.trunc(purchaseQuantity/stepSize)
			purchaseQuantity = availableSteps * stepSize
			purchaseQuantity = round(purchaseQuantity,precision)
			#print(purchaseQuantity*buyInPrice)
			print(buyInPrice)
			print("amount buying",purchaseQuantity)
			buy_order = client.order_limit_buy(
			symbol=tradeSymbol,
			quantity=purchaseQuantity,
			price=round(buyInPrice,precision),
			)
			print(buy_order['orderId'])
		

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		time.sleep(1)
		i += 1
		print(buyInPrice)
	
	time.sleep(45)
	endTrading(tradeSymbol,buyInPrice, purchaseQuantity)

def endTrading(tradeSymbol, buyInPrice, purchaseQuantity):
	i = 0
	sellPrice = 0
	orderId = ''
	precision = int(client.get_symbol_info(symbol=tradeSymbol)['baseAssetPrecision'])
	#stepSize = Decimal(client.get_symbol_info(symbol=tradeSymbol)['filters'][2]['stepSize'])
	
	while (i == 0):
		if(i>0):
			result = client.cancel_order(
    		symbol= tradeSymbol,
    		orderId= orderId)
		
		try:
			sellPrice = Decimal(client.get_symbol_ticker(symbol=tradeSymbol)['price'])
			sellPrice = round(sellPrice,precision)
			if(sellPrice > buyInPrice):
				#print(purchaseQuantity*buyInPrice)
				print(sellPrice)
				print("amount selling",purchaseQuantity)
				sell_order = client.order_limit_sell(
				symbol=tradeSymbol,
				quantity=purchaseQuantity,
				price=sellPrice,
				)
			
				print(sell_order['orderId'])
				orderId = sell_order['orderId']
		

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		time.sleep(1)
		i += 1
		print(sellPrice)


#checkCurrency("WAN")
#beginTrading("AVAXBNB","AVAX","BNB")
endTrading("WANBNB",0.00488,19.0)

#minor testing for the get _symbol_ticker(part of development)
#print(Decimal(client.get_symbol_ticker(symbol="OGNBNB")['price']))

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
#print(client.get_account())