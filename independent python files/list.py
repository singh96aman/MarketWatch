from googlefinance import getQuotes
from googlefinance import getNews
import json

# CompanyName, Index, LastTradePrice, LastTradeTime, Stock Symbol, Dividend, Yield
def getStock():
    company = ['AAPL','GOOGL','MSFT','CSCO','INTC','AMZN','VOD','QCOM','EBAY','INFY','DVMT','FB','TRIP','BBRY','PBYI','NVDA','TXN','SBUX','NFLX','ADBE','TSLA','MAR','EA','WDC','ADSK','ATVI','TMUS','MAT','FOXA','CTSH','DISCA','PYPL','GPRO','CTXS']
    company_name = ['Apple Inc.','Google Inc.','Microsoft Corporation','Cisco Systems','Intel Corporation','Amazon.com Inc','Vodafone Group Plc','Qualcomm, Inc.','eBay Inc.','Infosys Technologies Limited','Dell Inc.','Facebook, Inc.','TripAdvisor, Inc.','BlackBerry Limited','Puma Biotechnology Inc.','NVIDIA Corporation','Texas Instruments Incorporated','Starbucks Corporation','Netflix, Inc.','Adobe Systems Incorporated','Tesla, Inc.','Marriott International','Electronic Arts Inc.','Western Digital Corporation','Autodesk, Inc.','Activision Blizzard Inc.','T-Mobile US','Mattel Inc','21st Century Fox Class A','Cognizant Technology','Discovery Communications Inc.','Paypal Holdings Inc','GoPro, Inc.','Citrix Systems, Inc.']
    stock = []
    k=0
    for name in company:
        stock.append([])
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k].append("NA")
        stock[k][0]=company_name[k]
        newarray = json.dumps(getQuotes(name))
        array = newarray.split('"')
        j=0
        for temp in array:
            j=j+1
            if temp.find('Index') != -1 :
                stock[k][1]=array[j+1]
            if temp.find('LastTradePrice') != -1:
                stock[k][2]=array[j+1]
            if temp.find('LastTradeTime') != -1:
                stock[k][3]=array[j+1]
            if temp.find('StockSymbol') != -1:
                stock[k][4]=array[j+1]
            if temp.find('Dividend') != -1:
                stock[k][5]=array[j+1]
            if temp.find('Yield') != -1:
                stock[k][6]=array[j+1]
        k=k+1
    return stock

#hello = getStock()
company = ['ABB','ACC','AAPL']
#val = [10,25,15]
#j=0
#for name in company:
#    if name == 'AAPL':
#        val[j]=int(val[j])+100
#    j=j+1
#print val
#print hello
#print json.dumps(getQuotes('ACC'))
print(json.dumps(getNews("GOOG"), indent=2))
