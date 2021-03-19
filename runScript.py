
#imports
from dotenv import load_dotenv
from decimal import Decimal
import time
import math
import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from flask import Flask, request, Response
load_dotenv()
app = Flask(__name__)

# init api keys
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
	print("Beginning Buying")
	buyInPrice = 0
	purchaseQuantity = 0
	orderId = ''
	originCurrencyAvailable = client.get_asset_balance(asset=originCurrencySymbol)['free']
	originCurrencyAvailable = Decimal(originCurrencyAvailable) * Decimal(0.9)
	i = 0
	precision = int(client.get_symbol_info(symbol=tradeSymbol)['baseAssetPrecision'])
	stepSize = Decimal(client.get_symbol_info(symbol=tradeSymbol)['filters'][2]['stepSize'])
	
	while ((Decimal(client.get_asset_balance(asset=targetedCurrencySymbol)['free']) <= 0) and (i < 3)):
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
			buy_order = client.create_order(
			symbol=tradeSymbol,
			side='BUY',
			type='LIMIT',
			timeInForce='GTC',
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
	
	if((i <= 2) and (i > 0)):
		print("BOUGHT")
		time.sleep(25)
		endTrading(tradeSymbol,buyInPrice, targetedCurrencySymbol)

def endTrading(tradeSymbol, buyInPrice, targetedCurrencySymbol):
	print("Beginning Selling")
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
			i = 0
			while((orderMade == False) and (i < 9)):
				sellPrice = Decimal(client.get_symbol_ticker(symbol=tradeSymbol)['price'])
				sellPrice = round(sellPrice,precision)
				print("testing Price",sellPrice)
				time.sleep(1)
				if(sellPrice > Decimal(buyInPrice) * Decimal(1.002004)):
					print("price selling at",sellPrice)
					print("amount selling",quantityOwned)
					sell_order = client.create_order(
					symbol=tradeSymbol,
					side='SELL',
					type='LIMIT',
					timeInForce='GTC',
					quantity=quantityOwned,
					price=sellPrice,
					)
					orderMade = True
			
					orderId = sell_order['orderId']
				i += 1
		

		except BinanceAPIException as e:
			print(e)
		except BinanceOrderException as e:
			print(e)

		
		time.sleep(2)
	print("SOLD")


@app.route('/webhook', methods=['POST'])
def respond():
    try:
		return Response(status=200)
        print("running on",request.json['currency'])
        #checkCurrency(request.json['currency'])
        #return Response(status=200)
    except:
        print("something went not as expected (probably currency stuff)")
        return Response(status=200)
    

@app.route('/running')
def running():
  return 'Yes The System is running'

app.run(host='0.0.0.0', port=80)
