import logging
import acctkn
from kiteconnect import KiteConnect
logging.basicConfig(level=logging.DEBUG)
def gettoken():
    rt = acctkn.rtk()
    ap = acctkn.atp()
    se = acctkn.sec()
    api_key = ap
    api_secret = se
    request_token = rt
    print(rt)
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret)
    print(data["access_token"])
    access_token = open('access_token.txt', 'w')
    access_token.write(data["access_token"])
    access_token.close()
    gettkn = data["access_token"]
    return gettkn
# Place an order

tkn = gettoken()
print(tkn)







