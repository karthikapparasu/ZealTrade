#!c:\users\pcuser1.pcuser1-pc\appdata\local\programs\python\python38\python.exe
# https://api.kite.trade/instruments -- download instruments using this.

from kiteconnect import KiteConnect
import csv
import time
import math
from datetime import datetime, timedelta
import acctkn
import logging
from kiteconnect import KiteTicker
import requests
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
att = acctkn.att()
ap = acctkn.atp()
logging.info('Access token ' +att)
kite = KiteConnect(api_key=ap)
kws = KiteTicker(ap, att)
kite.set_access_token(att)
orders = []

def def_place_mkt_order_buy(symbl):
    print("Im inside def_place_mkt_order_buy for: ", symbl)
    try:

        print("\n Entered at: ", ' & CURRENT TIME IS',
              datetime.now())
        order_id = kite.place_order(tradingsymbol=symbl, variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_BSE,
                                    transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    quantity=1,
                                    order_type=kite.ORDER_TYPE_LIMIT,
                                    price=0.66,
                                    product=kite.PRODUCT_CNC, validity=None,
                                    disclosed_quantity=None, trigger_price=None,
                                    squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)
        print("\n Exit at: ", ' & CURRENT TIME IS',
              datetime.now())
        print("Order placed. ID is:", order_id)
        return order_id
    except Exception as e:
        print("exception occured:" + str(e))

#def_place_mkt_order_buy("SHALPRO")

