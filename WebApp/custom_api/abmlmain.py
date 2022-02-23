from kiteconnect import KiteConnect
import csv
import time
import math
import abml
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
WeeklyExpiry = '2022-01-20'
Specify_the_Entry_TIME_HHMM = '0920'
TradeSymbol_CE = None
TradeSymbol_PE = None
TradeSymbol_CE_Price = None
TradeSymbol_PE_Price = None
Final_PE_Price = None
Final_CE_Price = None
CE_Executed = None
PE_Executed = None
global StopLossPercent
StopLossPercent = 1
def def_place_mkt_order_sell(symbl, instrument_type):
    print("Im inside def_place_mkt_order_sell for: ", symbl, instrument_type)
    try:
        #order_id = "1234" + symbl
        if instrument_type == 'CE':
            global TradeSymbol_CE
            TradeSymbol_CE = symbl
        if instrument_type == 'PE':
            global TradeSymbol_PE
            TradeSymbol_PE = symbl
        order_id = abml.placeorder("REGULAR", 0, "NFO", "MIS", "MKT", "", 1, "DAY", "", symbl, "SELL", "")
        #order_id = kite.place_order(tradingsymbol=symbl, variety=kite.VARIETY_REGULAR,
                                    #exchange=kite.EXCHANGE_NFO,
                                    #transaction_type=kite.TRANSACTION_TYPE_SELL,
                                    #quantity=2000,
                                    #order_type=kite.ORDER_TYPE_MARKET,
                                    #product=kite.PRODUCT_MIS, price=None, validity=None,
                                    #disclosed_quantity=None, trigger_price=None,
                                    #squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)

        print("Order placed. ID is:", order_id)
        return order_id
    except Exception as e:
        print("exception occured:" + str(e))


def def_place_mkt_order_buy(symbl):
    print("Im inside def_place_mkt_order_buy for: ", symbl)
    try:
        #order_id = "4321" + symbl
        order_id = abml.placeorder("REGULAR", 0, "NFO", "MIS", "MKT", "", 1, "DAY", "", symbl, "BUY", "")
        #Placeorder.def_abml_place_order(symbl)
        #order_id = kite.place_order(tradingsymbol=symbl, variety=kite.VARIETY_REGULAR,
                                    #exchange=kite.EXCHANGE_NFO,
                                    #transaction_type=kite.TRANSACTION_TYPE_BUY,
                                    #quantity=2000,
                                    #order_type=kite.ORDER_TYPE_MARKET,
                                    #product=kite.PRODUCT_MIS, price=None, validity=None,
                                    #disclosed_quantity=None, trigger_price=None,
                                    #squareoff=None, stoploss=None, trailing_stoploss=None, tag=None)

        print("Order placed. ID is:", order_id)
        return order_id
    except Exception as e:
        print("exception occured:" + str(e))

def ORDER_mkt_order_BUY():
    tradingsymbol = 'NIFTY BANK'
    print(tradingsymbol)
    ohlc = kite.ltp('NSE:{}'.format(tradingsymbol))
    print(ohlc)
    #ltp = abml.scriptdetails("NFO", tradingsymbol)
    #ltp = 36000
    ltp = ohlc['last_price']
    print('\n BANKNIFTY SPOT Price:', ltp)
    # val = 31712.5
    # print(val)
    val = ltp
    val2 = math.fmod(val, 100)
    x = val - val2
    print('Round off Value', x)
    abs_val = "{:.0f}".format(x)  # to remove .0 string.
    PE_PRICE = "{}".format("{:.0f}".format(x + 0))
    PE_PRICE_2 = "{}".format("{:.0f}".format(x))
    print('\n Identified Contract from Instrument:', "{:.0f}".format(x))
    bn = 'BANKNIFTY'
    with open('../instruments.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for column in csv_reader:
            #print(column[4])
            if column[6] == PE_PRICE_2 and column[3] == bn and column[5] == WeeklyExpiry and column[9] == 'PE':
                # place CALL order
                # ord_id = 210107202793135
                ord_id_pe = def_place_mkt_order_sell(column[2], 'PE')
                orders.append(ord_id_pe)
                print('\n CALL contract SELL PE Executed: ', column[2])
            if column[6] == PE_PRICE_2 and column[3] == bn and column[5] == WeeklyExpiry and column[9] == 'CE':
                # place CALL order
                # ord_id = 210107202793135
                ord_id_ce = def_place_mkt_order_sell(column[2], 'CE')
                orders.append(ord_id_ce)
                print('\n CALL contract SELL CE Executed: ', column[2])

    print('\n The Executed Sell order IDs are : ', orders)
    PLACE_Buy_Options()


####################-------------------------------------------------------MAIN PROGRAM--------------------------------------------------
def PLACE_Buy_Options():
    ltp_CE = kite.ltp('NFO:{}'.format(TradeSymbol_CE))
    TradeSymbol_CE_Price = ltp_CE['NFO:{}'.format(TradeSymbol_CE)]['last_price']
    global StopLossPercent
    print('StopLossPercent:', StopLossPercent)
    Final_CE_Price_inc = (TradeSymbol_CE_Price * StopLossPercent) / 100
    global Final_CE_Price
    Final_CE_Price = TradeSymbol_CE_Price + Final_CE_Price_inc
    print('CE Price while selling', TradeSymbol_CE_Price)
    print('Final CE Price including Stop loss', Final_CE_Price)
    ltp_PE = kite.ltp('NFO:{}'.format(TradeSymbol_PE))
    TradeSymbol_PE_Price = ltp_PE['NFO:{}'.format(TradeSymbol_PE)]['last_price']
    Final_PE_Price_inc = (TradeSymbol_PE_Price * StopLossPercent) / 100
    global Final_PE_Price
    Final_PE_Price = TradeSymbol_PE_Price + Final_PE_Price_inc
    print('PE Price while selling', TradeSymbol_PE_Price)
    print('Final PE Price including Stop loss', Final_PE_Price)
    global CE_Executed
    global PE_Executed
    CE_Executed = 1
    PE_Executed = 1
    while True:
        ltp_CE_Current = kite.ltp('NFO:{}'.format(TradeSymbol_CE))
        TradeSymbol_CE_Price_Current = ltp_CE_Current['NFO:{}'.format(TradeSymbol_CE)]['last_price']
        print('Current CE Price', TradeSymbol_CE_Price_Current)
        print('Bought CE Price', Final_CE_Price)
        ltp_PE_Current = kite.ltp('NFO:{}'.format(TradeSymbol_PE))
        TradeSymbol_PE_Price_Current = ltp_PE_Current['NFO:{}'.format(TradeSymbol_PE)]['last_price']
        print('Current PE Price', TradeSymbol_PE_Price_Current)
        print('Bought PE Price', Final_PE_Price)
        if ((TradeSymbol_CE_Price_Current == Final_CE_Price or TradeSymbol_CE_Price_Current > Final_CE_Price) and CE_Executed == 1 ):
            print("\n The order execution started")
            print('Order placed for CE at: ', Final_CE_Price)
            ord_id_pe = def_place_mkt_order_buy(TradeSymbol_CE)
            Final_PE_Price = TradeSymbol_PE_Price
            print('Final Price changed for PE without stoploss', Final_PE_Price)
            orders.append(ord_id_pe)
            CE_Executed = 0
            print('\n CALL contract BUY CE Executed: ', TradeSymbol_CE, 'Price: ', TradeSymbol_CE_Price_Current)

        else:
            if(CE_Executed == 1):
               print("\n Going to wait 5 more seconds to check CE: ", Final_CE_Price, ' & CURRENT TIME IS',
                  datetime.now())
               time.sleep(2)
        if ((TradeSymbol_PE_Price_Current == Final_PE_Price or TradeSymbol_PE_Price_Current > Final_PE_Price) and PE_Executed == 1):
            print("\n The order execution started")
            print('Order placed for PE at: ', Final_PE_Price)
            ord_id_pe = def_place_mkt_order_buy(TradeSymbol_PE)
            PE_Executed = 0
            Final_CE_Price = TradeSymbol_CE_Price
            print('Final Price changed for CE without stoploss', Final_CE_Price)
            orders.append(ord_id_pe)
            print('\n CALL contract BUY PE Executed: ', TradeSymbol_PE, 'Price: ', TradeSymbol_PE_Price_Current)

        else:
            if (PE_Executed == 1):
             print("\n Going to wait 5 more seconds to check PE: ", Final_PE_Price, ' & CURRENT TIME IS',
                  datetime.now())
             time.sleep(2)
        if(CE_Executed == 0 and PE_Executed == 0):
            print("Order Covered up for the day")
            break
        else:
            print("Processing...")
    print('\n The Executed Buy order IDs are : ', orders)


def PLACE_Long_Put_Options():
    print("\n Current time: ", datetime.now())
    curr_dt = time.strftime("%Y%m%d", time.localtime())
    set_order_placement_time_first = curr_dt + Specify_the_Entry_TIME_HHMM
    print("\n Order placement TIME configured as : ", set_order_placement_time_first)

    while True:

        curr_tm_chk = time.strftime("%Y%m%d%H%M", time.localtime())
        if (set_order_placement_time_first == curr_tm_chk or curr_tm_chk > set_order_placement_time_first):
            print("\n The order execution started")
            ORDER_mkt_order_BUY()
            break
        else:
            print("\n Going to wait 5 more seconds till: ", set_order_placement_time_first, ' & CURRENT TIME IS',
                  datetime.now())
            time.sleep(5)

PLACE_Long_Put_Options()

