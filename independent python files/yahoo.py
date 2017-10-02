from yahoo_finance import Share
import urllib2
import base64
import json
yahoo = Share('AAPL')
print yahoo.get_open()

'''
def makechanges(name_of_company,company,companystock):
        stock = request.form['stock']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT companies FROM user WHERE username = %s;", [username])
        for row in cur.fetchall():
            for temp in row:
                lala = temp.split(',')
        j = 0
        for temp in lala:
            if temp == name_of_company:
                break
            j = j + 1
        cur.execute("SELECT stock FROM user WHERE username = %s;", [username])
        for row in cur.fetchall():
            for temp in row:
                lala = temp.split(',')
                print lala
        print j
        stock = convertnum(stock)
        lala[j] = float(lala[j]) + float(stock)
        lala[j] = str(lala[j])
        answer = ""
        for i in lala:
            if i != "":
                answer += i + ','

        temp = "update user set stock = \"" + answer + "\"  where username = \"" + username + "\";"
        cur.execute(temp)
        conn.commit()
        cur.execute("SELECT purse FROM user WHERE username = %s;", [username])
        for row in cur.fetchall():
            for temp in row:
                currency = float(temp)
        print currency
        company = convertnum(company[2])
        company = float(company)
        currency = currency - float(stock) * company
        currency = str(currency)
        temp = "update user set purse = \"" + currency + "\"  where username = \"" + username + "\";"
        print temp
        cur.execute(temp)
        conn.commit()
        j = 0

def convertnum(stockvalue):
    temp = ""
    for num in stockvalue:
        if(num != ','):
            temp+=num
    return temp
'''
