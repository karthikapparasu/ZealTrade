import requests
import json
import apiconfig
headers = {"Content-Type": "application/json; charset=utf-8",
           "Authorization": apiconfig.bearertoken()}

def placeorder(complexty, discqty, exch, pCode, prctyp, price, qty, ret, symbol_id, trading_symbol, transtype, trigPrice):
    url = apiconfig.endpoint() + apiconfig.placeorder()
    request = [{
        "complexty": complexty,
        "discqty": discqty,
        "exch": exch,
        "pCode": pCode,
        "prctyp": prctyp,
        "price": price,
        "qty": qty,
        "ret": ret,
        "symbol_id": symbol_id,
        "trading_symbol": trading_symbol,
        "transtype": transtype,
        "trigPrice": trigPrice
    }]
    response = requests.post(url, headers=headers, json=request)
    res = response.json()
    #print(res[0]["stat"])
    #print(res[0]["NOrdNo"])
    if response.status_code == 200:
        if res[0]["stat"] == "Ok":
            return res[0]["NOrdNo"]
        else:
            return res[0]["Emsg"]
    else:
        return "Unable to connect with remote server: API issue."


def scriptdetails(exch, symbol):
    url = apiconfig.endpoint() + apiconfig.scriptdetails()
    request = {
        "exch": exch,
        "symbol": symbol,
    }
    response = requests.post(url, headers=headers, json=request)
    res = response.json()
    #print(res)
    #print(res["stat"])
    # print(res[0]["NOrdNo"])
    if response.status_code == 200:
        if res["stat"] == "Ok":
            return res["LTP"]
        else:
            return res["Emsg"]
    else:
        return "Unable to connect with remote server: API issue."


#orderid = placeorder("REGULAR",0,"NSE","MIS","MKT","",1,"DAY","","INFY","BUY","")
#print(orderid)

#orderid = scriptdetails("NSE", "RCOM")
#print(orderid)


