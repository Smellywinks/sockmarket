import urllib2
import json
import time

def fetchPreMarket(symbol, exchange):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s:%s" % (exchange, symbol)
    u = urllib2.urlopen(url)
    content = u.read()
    data = json.loads(content[3:])
    info = data[0]
    t = str(info["elt"])    # time stamp
    l = float(info["l"])    # close price (previous trading day)
    p = float(info["el"])   # stock price in pre-market (after-hours)
    #return (t,l,p)
    return info