from flask import Flask
from flaskext.mail import Mail

app = Flask(__name__)
mail = Mail(app)
    mail = Mail()
    msg = mail("Hello",
                  sender="from@example.com",
                  recipients=["to@example.com"])
    mail.send(msg)
