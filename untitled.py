from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, json
from flaskext.mysql import MySQL
from yahoo_finance import Share

from lxml import html
import requests
from exceptions import ValueError
import json
from collections import OrderedDict



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '24singh96'
app.config['MYSQL_DATABASE_DB'] = 'login'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app = Flask(__name__)

company_symbol = ['AAPL', 'GOOGL', 'MSFT', 'CSCO', 'INTC', 'AMZN', 'VOD', 'QCOM', 'EBAY', 'INFY', 'DVMT', 'FB', 'CBS',
                  'BBRY', 'AGNC', 'NVDA', 'TXN', 'SBUX', 'NFLX', 'ADBE', 'TSLA', 'CERN', 'EA', 'WDC', 'ADSK', 'ATVI',
                  'TMUS', 'MAT', 'FOXA', 'CTSH', 'DISCA', 'PYPL', 'GPRO', 'CTXS']

company_name = ['Apple Inc.', 'Google Inc.', 'Microsoft Corporation', 'Cisco Systems', 'Intel Corporation',
                'Amazon.com Inc', 'Vodafone Group Plc', 'Qualcomm, Inc.', 'eBay Inc.', 'Infosys Technologies Limited',
                'Dell Inc.', 'Facebook, Inc.', 'CBSAdvisor, Inc.', 'BlackBerry Limited', 'American Capital Agency',
                'NVIDIA Corporation', 'Texas Instruments Incorporated', 'Starbucks Corporation', 'Netflix, Inc.',
                'Adobe Systems Incorporated', 'Tesla, Inc.', 'Marriott International', 'Electronic Arts Inc.',
                'Western Digital Corporation', 'Autodesk, Inc.', 'Activision Blizzard Inc.', 'T-Mobile US',
                'Mattel Inc', '21st Century Fox Class A', 'Cognizant Technology', 'Discovery Communications Inc.',
                'Paypal Holdings Inc', 'GoPro, Inc.', 'Citrix Systems, Inc.']

google_links = ['https://www.google.com/finance?q=NASDAQ%3AAAPL&ei=LKiZWejREcOvuATThbuACQ',
                'https://www.google.com/finance?q=NASDAQ%3AGOOGL&ei=hqiZWfGDONGkuASQ7oUg',
                'https://www.google.com/finance?q=NASDAQ%3AMSFT&ei=nKiZWdipLtG8uQSv6IUQ',
                'https://www.google.com/finance?q=NASDAQ%3ACSCO&ei=waiZWaiZD9KqugSFtKLICg',
                'https://www.google.com/finance?q=NASDAQ%3AINTC&ei=5KiZWbHFN9GkuASQ7oUg',
                'https://www.google.com/finance?q=NASDAQ%3AAMZN&ei=DKmZWbHYB4rBugSfhozIDg',
                'https://www.google.com/finance?q=NASDAQ%3AVOD&ei=KKmZWfnOLI67ugS8vYeQBw',
                'https://www.google.com/finance?q=NASDAQ%3AQCOM&ei=SKmZWYm1JYyKuwSZ7azoCAV',
                'https://www.google.com/finance?q=NASDAQ%3AEBAY&ei=WamZWfDmF4fCuASxrJawBQ',
                'https://www.google.com/finance?q=NYSE%3AINFY&ei=j6mZWbjvNtOouAS4h7_QAw',
                'https://www.google.com/finance?q=NYSE%3ADVMT&ei=p6mZWcCuL4GtuAScnZT4CQ',
                'https://www.google.com/finance?q=NASDAQ%3AFB&ei=wamZWdCMAYWtugSnu42QCA',
                'https://www.google.com/finance?q=NASDAQ%3ACBS&ei=3amZWaGHCN2-uwSkyKB4',
                'https://www.google.com/finance?q=NASDAQ%3ABBRY&ei=_KmZWYCXIsOvuATThbuACQ',
                'https://finance.google.com/finance?q=NYSE:AGNC',
                'https://www.google.com/finance?q=NASDAQ%3ANVDA&ei=HqqZWaDoO9G8uQSv6IUQ',
                'https://www.google.com/finance?q=NASDAQ%3ATXN&ei=M6qZWZn3KcjRuATVkbaYDA',
                'https://www.google.com/finance?q=NASDAQ%3ASBUX&ei=TKqZWaDlPNGkuASQ7oUg',
                'https://www.google.com/finance?q=NASDAQ%3ANFLX&ei=XKqZWYi-IoGtuAScnZT4CQ',
                'https://www.google.com/finance?q=NASDAQ%3AADBE&ei=caqZWcmXGszMuATmi4SwBA',
                'https://www.google.com/finance?q=NASDAQ%3ATSLA&ei=gaqZWaiVOs6ruAS6yYTADg',
                'https://www.google.com/finance?q=NASDAQ%3ACERN&ei=kKqZWcDqG4i6uQSOvrqYDA',
                'https://www.google.com/finance?q=NASDAQ%3AEA&ei=o6qZWbjeEt2-uwSkyKB4',
                'https://www.google.com/finance?q=NASDAQ%3AWDC&ei=uqqZWfGYMYrBugSfhozIDg',
                'https://www.google.com/finance?q=NASDAQ%3AADSK&ei=1qqZWbjnD467ugS8vYeQBw',
                'https://www.google.com/finance?q=NASDAQ%3AATVI&ei=66qZWdiAEsejugTW54WoCg',
                'https://www.google.com/finance?q=NASDAQ%3ATMUS&ei=C6uZWZCPFYbOuATGs5DQDA',
                'https://www.google.com/finance?q=NASDAQ%3AMAT&ei=HKuZWYnoFJKQuQS13q-QAw',
                'https://www.google.com/finance?q=NASDAQ%3AFOXA&ei=LKuZWYnKHsejugTW54WoCg',
                'https://www.google.com/finance?q=NASDAQ%3ACTSH&ei=QquZWeCVGIfCuASxrJawBQ',
                'https://www.google.com/finance?q=NASDAQ%3ADISCA&ei=T6uZWYmkAdOouAS4h7_QAw',
                'https://www.google.com/finance?q=NASDAQ%3APYPL&ei=c6uZWfrSAYbguQTQsrP4Dw',
                'https://www.google.com/finance?q=NASDAQ%3AGPRO&ei=gKuZWfmiEYi6uQSOvrqYDA',
                'https://www.google.com/finance?q=NASDAQ%3ACTXS&ei=j6uZWcDzGMvSuASc2b7ICw']

def load_portfolio():
    conn = mysql.connect()
    cur = conn.cursor()
    if 'username' in session:
        username = session['username']
    cur.execute("SELECT * FROM user WHERE username = %s", username)
    userdetails = [dict(
        id=row[0],
        username=row[5],
        password=row[6],
        stock=row[7],
        purse=row[8],
        playervalue=row[9]
    ) for row in cur.fetchall()]
    return userdetails

@app.route('/login', methods=['GET', 'POST'])
def login():
    print "login"
    error = ""

    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [username_form])  # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE username = %s;", [username_form])
            for row in cur.fetchall():
                if password_form == row[0]:
                    cur.execute("SELECT * FROM user WHERE username = %s", [username_form])
                    userdetails = [dict(
                        id=row[0],
                        username=row[5],
                        password=row[6],
                        stock=row[7],
                        purse=row[8],
                        playervalue=row[9]
                    ) for row in cur.fetchall()]
                    session['username'] = request.form['username']
                    currentownership = getcurrentstock()
                    print session['username']
                    print userdetails,currentownership
                    return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
                else:
                    error = "Invalid credential"
        else:
            error = "Invalid Credential"
        conn.commit()
    return render_template('index.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print "index"
    error = ""

    if 'username' in session:
        username_form = session['username']
        print "username is "+username_form
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", [username_form])
        userdetails = [dict(
            id=row[0],
            username=row[5],
            password=row[6],
            stock=row[7],
            purse=row[8],
            playervalue=row[9]
        ) for row in cur.fetchall()]
        currentownership = getcurrentstock()
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)

    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [username_form])  # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE username = %s;", [username_form])
            for row in cur.fetchall():
                if password_form == row[0]:
                    cur.execute("SELECT * FROM user WHERE username = %s", [username_form])
                    userdetails = [dict(
                        id=row[0],
                        username=row[5],
                        password=row[6],
                        stock=row[7],
                        purse=row[8],
                        playervalue=row[9]
                    ) for row in cur.fetchall()]
                    session['username'] = request.form['username']
                    currentownership = getcurrentstock()
                    return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
                else:
                    error = "Invalid credential"
        else:
            error = "Invalid Credential"
        conn.commit()
    return render_template('index.html', error=error)

def getcurrentstock():
    conn = mysql.connect()
    cur = conn.cursor()
    if 'username' in session:
        username = session['username']
    print "username is "+username
    cur.execute("SELECT * FROM user WHERE username = %s", [username])
    for row in cur.fetchall():
        print row
        newarray = row[7].split(',')
        stocks = []
        j = 0
        k=0
        for i in newarray:
            if i != '0' :
                stocks.append([])
                stocks[k].append(i)
                stocks[k].append(j)
                k = k+1
            j = j + 1
        currentownership = [dict(
            stock=row[0],
            name=company_name[row[1]],
            symbol=company_symbol[row[1]]
        ) for row in stocks]
        updateleaderboard()
        return currentownership


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    print "sign up"
    error = ""
    if 'username' in session:
        return "User already exists with username "+session['username']
    if request.method == 'POST':
        print "sign up post"
        Signupuser = request.form['signupusername']
        Signuppass = request.form['signuppassword']
        Signupname = request.form['signupname']
        Signupreg = request.form['signupreg']
        Signupmob = request.form['signupmob']
        Signupcol = request.form['signupcol']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [Signupuser])  # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            error = "Incorrect Credentials"
            return render_template('signup.html', error=error)
            #cur.execute("SELECT password FROM user WHERE username = %s;", [Signupuser])
            #for row in cur.fetchall():
             #   for lol in row:
             #       if Signuppass == lol:

        temp = "insert into user(name,regno,college,mobileno,username,password,stock,purse,playervalue) values (\""+Signupname+"\",\""+Signupreg+"\",\""+Signupmob+"\",\""+Signupcol+"\",\""+Signupuser+"\",\""+Signuppass+"\",\"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\",100000,10000);"
        print temp
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(temp)
        conn.commit()
        cur.execute("SELECT * FROM user WHERE username = %s", [Signupuser])
        userdetails = [dict(
            id=row[0],
            username=row[5],
            password=row[6],
            stock=row[7],
            purse=row[8],
            playervalue=row[9]
        ) for row in cur.fetchall()]
        session['username'] = request.form['signupusername']
        currentownership = getcurrentstock()
        if currentownership == "" :
            print "currentownership"
            return render_template('portfolio.html', userdetails=userdetails)

        return render_template('portfolio.html',userdetails=userdetails, currentownership=currentownership)
    return render_template('signup.html',error=error)

@app.route('/NYSE', methods=['GET', 'POST'])
def NYSE():
    companystock = [dict(
        name = company_name[k],
        symbol = company_symbol[k]
    ) for k in range(0,33)]
    return render_template('NYSE.html', companystock=companystock)

def updateleaderboard():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT username FROM user ORDER BY purse DESC")
    names = []
    player = []

    for row in cur.fetchall():
        for i in row:
            temp = "SELECT stock FROM user WHERE username = \"" + str(i) + "\";"
            cur.execute("SELECT stock FROM user WHERE username = %s;", [i])
            print temp
            for row in cur.fetchall():
                for lol in row:
                    userstock = lol.split(',')
            cur.execute("SELECT stock from stock");
            userstockprice = []
            for row in cur.fetchall():
                for lol in row:
                    userstockprice.append(lol)
            playerval = 0
            cur.execute("SELECT purse FROM user WHERE username = %s;", [i])
            for row in cur.fetchall():
                for lol in row:
                    playerval += float(lol)

            for j in range(0, 33):
                playerval += float(userstock[j]) * float(userstockprice[j])

            cur.execute("update user set playervalue = \"" + str(playerval) + "\"WHERE username = %s;", [i])
            conn.commit()

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT username FROM user ORDER BY purse DESC")
    names=[]
    player=[]

    for row in cur.fetchall():
        for i in row:
            temp="SELECT stock FROM user WHERE username = \""+str(i)+"\";"
            cur.execute("SELECT stock FROM user WHERE username = %s;", [i])
            print temp
            for row in cur.fetchall():
                for lol in row:
                    userstock = lol.split(',')
            cur.execute("SELECT stock from stock");
            userstockprice = []
            for row in cur.fetchall():
                for lol in row:
                    userstockprice.append(lol)
            playerval = 0
            cur.execute("SELECT purse FROM user WHERE username = %s;", [i])
            for row in cur.fetchall():
                for lol in row:
                    playerval+=float(lol)

            for j in range(0,33):
                playerval+=float(userstock[j])*float(userstockprice[j])

            cur.execute("update user set playervalue = \""+str(playerval)+"\"WHERE username = %s;", [i])
            conn.commit()

    i=0
    cur.execute("SELECT playervalue FROM user ORDER BY playervalue DESC limit 10")
    for row in cur.fetchall():
        for lol in row:
            player.append(lol)
            i=i+1

    cur.execute("SELECT username FROM user ORDER BY playervalue DESC limit 10")
    for row in cur.fetchall():
        for lol in row:
            names.append(lol)

    print player

    userstock = [dict(
        name=names[j],
        playerval=player[j],
    )for j in range(0,i)]

    return render_template('leaderboard.html',userstock=userstock)

@app.route('/AAPL', methods=['GET', 'POST'])
def AAPL():
    companystock,stock,purse,currentstock = getStock2('AAPL')
    error = ""
    if request.method == 'POST':
        error=makechanges('AAPL',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)


@app.route('/GOOGL', methods=['GET', 'POST'])
def GOOGL():
    companystock,stock,purse,currentstock = getStock2('GOOGL')
    error = ""
    if request.method == 'POST':
        error=makechanges('GOOGL',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/MSFT', methods=['GET', 'POST'])
def MSFT():
    companystock,stock,purse,currentstock = getStock2('MSFT')
    error = ""
    if request.method == 'POST':
        error=makechanges('MSFT',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/CSCO', methods=['GET', 'POST'])
def CSCO():
    companystock,stock,purse,currentstock = getStock2('CSCO')
    error = ""
    if request.method == 'POST':
        error=makechanges('CSCO',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/INTC', methods=['GET', 'POST'])
def INTC():
    companystock,stock,purse,currentstock = getStock2('INTC')
    error = ""
    if request.method == 'POST':
        error=makechanges('INTC',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/AMZN', methods=['GET', 'POST'])
def AMZN():
    companystock,stock,purse,currentstock = getStock2('AMZN')
    error = ""
    if request.method == 'POST':
        error=makechanges('AMZN',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/VOD', methods=['GET', 'POST'])
def VOD():
    companystock,stock,purse,currentstock = getStock2('VOD')
    error = ""
    if request.method == 'POST':
        #print "hello"
        error=makechanges('VOD',stock)
        #print "whatff"
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/QCOM', methods=['GET', 'POST'])
def QCOM():
    companystock,stock,purse,currentstock = getStock2('QCOM')
    error = ""
    if request.method == 'POST':
        error=makechanges('QCOM',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/INFY', methods=['GET', 'POST'])
def INFY():
    companystock,stock,purse,currentstock = getStock2('INFY')
    error = ""
    if request.method == 'POST':
        error=makechanges('INFY',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/DVMT', methods=['GET', 'POST'])
def DVMT():
    companystock,stock,purse,currentstock = getStock2('DVMT')
    error = ""
    if request.method == 'POST':
        error=makechanges('DVMT',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/FB', methods=['GET', 'POST'])
def FB():
    companystock,stock,purse,currentstock = getStock2('FB')
    error = ""
    if request.method == 'POST':
        error=makechanges('FB',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/CBS', methods=['GET', 'POST'])
def CBS():
    companystock,stock,purse,currentstock = getStock2('CBS')
    error = ""
    if request.method == 'POST':
        error=makechanges('CBS',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/BBRY', methods=['GET', 'POST'])
def BBRY():
    companystock,stock,purse,currentstock = getStock2('BBRY')
    error = ""
    if request.method == 'POST':
        error=makechanges('BBRY',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/AGNC', methods=['GET', 'POST'])
def PBYI():
    companystock,stock,purse,currentstock = getStock2('AGNC')
    error = ""
    if request.method == 'POST':
        error=makechanges('AGNC',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/NVDA', methods=['GET', 'POST'])
def NVDA():
    companystock,stock,purse,currentstock = getStock2('NVDA')
    error = ""
    if request.method == 'POST':
        error=makechanges('NVDA',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/TXN', methods=['GET', 'POST'])
def TXN():
    companystock,stock,purse,currentstock = getStock2('TXN')
    error = ""
    if request.method == 'POST':
        error=makechanges('TXN',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/SBUX', methods=['GET', 'POST'])
def SBUX():
    companystock,stock,purse,currentstock = getStock2('SBUX')
    error = ""
    if request.method == 'POST':
        error=makechanges('SBUX',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/NFLX', methods=['GET', 'POST'])
def NFLX():
    companystock,stock,purse,currentstock = getStock2('NFLX')
    error = ""
    if request.method == 'POST':
        error=makechanges('NFLX',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/EBAY', methods=['GET', 'POST'])
def EBAY():
    companystock,stock,purse,currentstock = getStock2('EBAY')
    error = ""
    if request.method == 'POST':
        error=makechanges('EBAY',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/ADBE', methods=['GET', 'POST'])
def ADBE():
    companystock,stock,purse,currentstock = getStock2('ADBE')
    error = ""
    if request.method == 'POST':
        error=makechanges('ADBE',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/TSLA', methods=['GET', 'POST'])
def TSLA():
    companystock,stock,purse,currentstock = getStock2('TSLA')
    error = ""
    if request.method == 'POST':
        error=makechanges('TSLA',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/CERN', methods=['GET', 'POST'])
def CERN():
    companystock,stock,purse,currentstock = getStock2('CERN')
    error = ""
    if request.method == 'POST':
        error=makechanges('CERN',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/EA', methods=['GET', 'POST'])
def EA():
    companystock,stock,purse,currentstock = getStock2('EA')
    error = ""
    if request.method == 'POST':
        error=makechanges('EA',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/WDC', methods=['GET', 'POST'])
def WDC():
    companystock,stock,purse,currentstock = getStock2('WDC')
    error = ""
    if request.method == 'POST':
        error=makechanges('WDC',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/ADSK', methods=['GET', 'POST'])
def ADSK():
    companystock,stock,purse,currentstock = getStock2('ADSK')
    error = ""
    if request.method == 'POST':
        error=makechanges('ADSK',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/ATVI', methods=['GET', 'POST'])
def ATVI():
    companystock,stock,purse,currentstock = getStock2('ATVI')
    error = ""
    if request.method == 'POST':
        error=makechanges('ATVI',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/TMUS', methods=['GET', 'POST'])
def TMUS():
    companystock,stock,purse,currentstock = getStock2('TMUS')
    error = ""
    if request.method == 'POST':
        error=makechanges('TMUS',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/MAT', methods=['GET', 'POST'])
def MAT():
    companystock,stock,purse,currentstock = getStock2('MAT')
    error = ""
    if request.method == 'POST':
        error=makechanges('MAT',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/FOXA', methods=['GET', 'POST'])
def FOXA():
    companystock,stock,purse,currentstock = getStock2('FOXA')
    error = ""
    if request.method == 'POST':
        error=makechanges('FOXA',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/CTSH', methods=['GET', 'POST'])
def CTSH():
    companystock,stock,purse,currentstock = getStock2('CTSH')
    error = ""
    if request.method == 'POST':
        error=makechanges('CTSH',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/DISCA', methods=['GET', 'POST'])
def DISCA():
    companystock,stock,purse,currentstock = getStock2('DISCA')
    error = ""
    if request.method == 'POST':
        error=makechanges('DISCA',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/PYPL', methods=['GET', 'POST'])
def PYPL():
    companystock,stock,purse,currentstock = getStock2('PYPL')
    error = ""
    if request.method == 'POST':
        error=makechanges('PYPL',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/GPRO', methods=['GET', 'POST'])
def GPRO():
    companystock,stock,purse,currentstock = getStock2('GPRO')
    error = ""
    if request.method == 'POST':
        error=makechanges('GPRO',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

@app.route('/CTXS', methods=['GET', 'POST'])
def CTXS():
    companystock,stock,purse,currentstock = getStock2('CTXS')
    error = ""
    if request.method == 'POST':
        error=makechanges('CTXS',stock)
        userdetails = load_portfolio()
        currentownership=getcurrentstock()
        if error != "":
            return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)
        return render_template('portfolio.html', userdetails=userdetails, currentownership=currentownership)
    print  companystock
    return render_template('company.html', companystock=companystock , purse=purse, currentstock=currentstock,error=error)

def getStock(name_of_company):
    global company_name,company_symbol
    stock = []
    k=0
    stock.append([])
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    j=0
    for i in company_symbol:
        if i == name_of_company:
            break
        j=j+1
    print "j is "+str(j)+"link is "
    stock[0]=company_name[j]
    yahoo = Share(name_of_company)
    stock[1] = yahoo.get_open()
    stock[2] = yahoo.get_price()
    stock[3] = yahoo.get_trade_datetime()
    stock[4] = company_symbol[j]
    stock[5] = yahoo.get_volume()
    stock[6] = yahoo.get_dividend_yield()
    stock[7] = google_links[j]
    print stock
    conn = mysql.connect()
    cur = conn.cursor()
    if 'username' in session:
        username = session['username']
    cur.execute("SELECT purse FROM user WHERE username = %s;", [username])
    print username
    for row in cur.fetchall():
        for lol in row:
            purse=lol
    companystock = [dict(
        name=stock[0],
        open=stock[1],
        lasttradeprice=stock[2],
        lasttradetime=stock[3],
        stocksymbol=stock[4],
        MarketCapital=stock[5],
        dividend=stock[6],
        link=stock[7]
    )]
    cur.execute("SELECT stock FROM user WHERE username = %s;", [username])
    print username
    for row in cur.fetchall():
        for lol in row:
            newarray = lol.split(',')
            currentstock = newarray[j]

    print purse
    return companystock,stock,purse,currentstock


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


def getStock2(ticker):
    financial_data=parse(ticker)
    j = 0
    for i in company_symbol:
        if i == ticker:
            break
        j = j + 1
    conn = mysql.connect()
    cur = conn.cursor()
    temp = "update stock set stock = \"" + str(financial_data[1]) + "\" where name = \"" + str(j) + "\";"
    cur.execute(temp)
    print temp
    conn.commit()

    print "j is " + str(j) + "link is "
    stock = []
    stock.append([])
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")
    stock.append("NA")

    stock[0] = company_name[j]
    stock[1] = financial_data[0]
    stock[2] = financial_data[1]
    stock[3] = financial_data[2]
    stock[4] = financial_data[3]
    stock[5] = financial_data[4]
    stock[6] = financial_data[5]
    stock[7] = google_links[j]

    conn = mysql.connect()
    cur = conn.cursor()
    if 'username' in session:
        username = session['username']
    cur.execute("SELECT purse FROM user WHERE username = %s;", [username])
    #print username
    for row in cur.fetchall():
        for lol in row:
            purse = lol
    companystock = [dict(
        name=stock[0],
        targetest=stock[1],
        currentprice=stock[2],
        totalrevenue=stock[3],
        stocksymbol=stock[4],
        url=stock[5],
        eps=stock[6],
        link=stock[7]
    )]
    cur.execute("SELECT stock FROM user WHERE username = %s;", [username])
    #print username
    for row in cur.fetchall():
        for lol in row:
            newarray = lol.split(',')
            currentstock = newarray[j]

    return companystock, stock, purse, currentstock


def makechanges(name_of_company,company2):
        error = ""
        stock = request.form['stockbuy']
        stocksell = request.form['stocksell']
        conn = mysql.connect()
        cur = conn.cursor()
        if 'username' in session:
            username = session['username']
        cur.execute("SELECT stock FROM user WHERE username = %s;", [username])
        for row in cur.fetchall():
            for lol in row:
                newarray=lol.split(',')
        print newarray
        j=0

        for i in company_symbol:
            if i == name_of_company:
                break
            j=j+1
        print j
        if stocksell != "":
            currentownership = int(newarray[j])
            stocksell = convertnum(stocksell)
            currentownership = currentownership - int(stocksell)
            if currentownership >=0 :
                currentownership = str(currentownership)

                newarray[j] = currentownership

                temp2 = ""
                for i in newarray:
                    temp2 += i + ","
                temp2 = temp2[:-1]

                temp = "update user set stock = \"" + temp2 + "\"  where username = \"" + username + "\";"
                cur.execute(temp)
                conn.commit()
                cur.execute("SELECT purse FROM user WHERE username = %s;", [username])
                for row in cur.fetchall():
                    for temp in row:
                        currency = float(temp)
                print currency
                #company = convertnum(company[2])
                print company2[2]
                company = float(company2[2])
                currency = currency + float(stocksell) * company
                currency = str(currency)
                temp = "update user set purse = \"" + currency + "\"  where username = \"" + username + "\";"
                print temp
                cur.execute(temp)
                conn.commit()
            else :
                error = "Not Enough Stocks To Sell !"

        if stock != "":
            cur.execute("SELECT purse FROM user WHERE username = %s;", [username])
            for row in cur.fetchall():
                for temp in row:
                    currency = float(temp)
            print currency
            #company = convertnum(company[2])
            #print company[2]
            company = float(company2[2])
            currency = currency - float(stock) * company
            if currency > 0:
                currency = str(currency)
                temp = "update user set purse = \"" + currency + "\"  where username = \"" + username + "\";"
                print temp
                cur.execute(temp)
                conn.commit()
                currentownership = int(newarray[j])
                #stock = convertnum(stock)
                currentownership = currentownership + int(stock)
                currentownership = str(currentownership)

                newarray[j] = currentownership

                temp2 = ""
                for i in newarray:
                    temp2 += i + ","
                temp2 = temp2[:-1]

                temp = "update user set stock = \"" + temp2 + "\"  where username = \"" + username + "\";"
                cur.execute(temp)
                conn.commit()
                j = 0
            else :
                error = "You don't have enough money !"
        updateleaderboard()
        return error

def updatestocks():
    for j in range(0,33):
        financial_data = parse(company_symbol[j])
        conn = mysql.connect()
        cur = conn.cursor()
        temp = "update stock set stock = \""+str(financial_data[1])+"\" where name = \""+str(j)+"\";"
        cur.execute(temp)
        print temp
        conn.commit()

def convertnum(stockvalue):
    temp = ""
    for num in stockvalue:
        if(num != ','):
            temp+=num
    return temp

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    app.run()
