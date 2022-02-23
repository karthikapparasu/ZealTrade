import logging
import acctkn
from kiteconnect import KiteTicker

logging.basicConfig(level=logging.DEBUG)
# Initialise

att = acctkn.att()
ap = acctkn.atp()
api_key = ap
access_token = att
print(att)
kws = KiteTicker(api_key, access_token)


def on_ticks_price(ws, ticks):
    print(ws)
    print(ticks)
    # Callback to receive ticks.
    response = format(ticks)
    print(response)
    logging.debug("Ticks: {}".format(ticks))
    print(ticks[0]['instrument_token'])
    instrument_token_value = ticks[0]['instrument_token']
    last_price_value = ticks[0]['last_price']
    print(last_price_value)

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([10027778])
    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [10027778])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks_price
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
