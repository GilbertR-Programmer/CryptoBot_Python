
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
	orderId = ''
	originCurrencyAvailable = client.get_asset_balance(asset=originCurrencySymbol)['free']
	originCurrencyAvailable = Decimal(originCurrencyAvailable) * Decimal(0.9)
	i = 0
	precision = int(client.get_symbol_info(symbol=tradeSymbol)['baseAssetPrecision'])
	stepSize = Decimal(client.get_symbol_info(symbol=tradeSymbol)['filters'][2]['stepSize'])
	
	while ((Decimal(client.get_asset_balance(asset=targetedCurrencySymbol)['free']) <= 0) or (i > 2)):
		if(i>0):
			try:
				print("canceling",orderId)
				result = client.cancel_order(
				symbol= tradeSymbol,
				orderId= orderId)

			except BinanceAPIException as e:
				print(e)
			except BinanceOrderException as e:
				print(e)
		
		try:
			buyInPrice = Decimal(client.get_ticker(symbol=tradeSymbol)['askPrice'])
			purchaseQuantity = originCurrencyAvailable/buyInPrice
			availableSteps = math.trunc(purchaseQuantity/stepSize)
			purchaseQuantity = availableSteps * stepSize
			purchaseQuantity = round(purchaseQuantity,precision)
			print("price buying at",buyInPrice)
			print("amount buying",purchaseQuantity)
			buy_order = client.order_limit_buy(
			symbol=tradeSymbol,
			quantity=purchaseQuantity,
			price=round(buyInPrice,precision),
			)

			orderId = buy_order['orderId']
		

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		time.sleep(2)
		i += 1
	
	if(i <= 2):
		print("BOUGHT")
		time.sleep(30)
		endTrading(tradeSymbol,buyInPrice, targetedCurrencySymbol)

def endTrading(tradeSymbol, buyInPrice, targetedCurrencySymbol):
	sellPrice = 0
	orderMade = False
	orderId = ''
	quantityOwned = Decimal(client.get_asset_balance(asset=targetedCurrencySymbol)['free'])
	precision = int(client.get_symbol_info(symbol=tradeSymbol)['baseAssetPrecision'])	
	while ((quantityOwned > Decimal(0)) or(Decimal(client.get_asset_balance(asset=targetedCurrencySymbol)['locked']) > 0)):
		if(orderMade):
			try:
				print("canceling",orderId)
				result = client.cancel_order(
				symbol= tradeSymbol,
				orderId= orderId)
				orderMade = False

			except BinanceAPIException as e:
				print(e)
			except BinanceOrderException as e:
				print(e)

		quantityOwned = Decimal(client.get_asset_balance(asset=targetedCurrencySymbol)['free'])
		try:
			
			while(orderMade == False):
				sellPrice = Decimal(client.get_symbol_ticker(symbol=tradeSymbol)['price'])
				sellPrice = round(sellPrice,precision)
				print("testing Price",sellPrice)
				time.sleep(1)
				if(sellPrice > Decimal(buyInPrice) * Decimal(1.002004)):
					print("price selling at",sellPrice)
					print("amount selling",quantityOwned)
					sell_order = client.order_limit_sell(
					symbol=tradeSymbol,
					quantity=quantityOwned,
					price=sellPrice,
					)
					orderMade = True
			
					orderId = sell_order['orderId']
		

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		
		time.sleep(2)
	print("SOLD")


checkCurrency("ADA")
#beginTrading("BIFIBNB","BIFI","BNB")
#endTrading("IQBNB",0.00008630,"IQ")

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