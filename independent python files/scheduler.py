import datetime
import time
from apscheduler.scheduler import Scheduler
from googlefinance import getQuotes

import requests
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, json
from flaskext.mysql import MySQL
from googlefinance import getQuotes
import json
from yahoo_finance import Share

from lxml import html
import requests
from exceptions import ValueError
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep

company_symbol = ['AAPL', 'GOOGL', 'MSFT', 'CSCO', 'INTC', 'AMZN', 'VOD', 'QCOM', 'EBAY', 'INFY', 'DVMT', 'FB', 'CBS',
                  'BBRY', 'JPM', 'NVDA', 'TXN', 'SBUX', 'NFLX', 'ADBE', 'TSLA', 'CERN', 'EA', 'WDC', 'ADSK', 'ATVI',
                  'TMUS', 'MAT', 'FOXA', 'CTSH', 'DISCA', 'PYPL', 'GPRO', 'CTXS']

def parse(ticker):
    url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    response = requests.get(url)
    print "Parsing %s" % (url)
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(
        ticker)
    summary_json_response = requests.get(other_details_json_link)
    financialData =[]
    financialData.append([])
    financialData.append("NA")
    financialData.append("NA")
    financialData.append("NA")
    financialData.append("NA")
    financialData.append("NA")
    financialData.append("NA")
    try:
        json_loaded_summary = json.loads(summary_json_response.text)
        financialData[0] = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        financialData[1] = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']
        financialData[2] =json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["totalRevenue"]['fmt']
        financialData[3] = ticker
        financialData[4] = url
        earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        financialData[5] = eps
        return financialData
    except ValueError:
        print "Failed to parse json response"
        return {"error": "Failed to parse json response"}

stockprice = []
for j in range(0,33):
    stockprice.append(0)

def updatestocks():
    for j in range(0,33):
        financial_data = parse(company_symbol[j])
        stockprice[j] = financial_data[1]
        print stockprice[j]

#updatestocks()

import threading

def work ():
  threading.Timer(300, work).start ()
  updatestocks()
work ()