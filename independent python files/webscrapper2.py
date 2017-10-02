from lxml import html
import requests
from exceptions import ValueError
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep


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


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker', help='')
    args = argparser.parse_args()
    ticker = args.ticker
    print "Fetching data for %s" % (ticker)
    scraped_data = parse(ticker)
    print scraped_data