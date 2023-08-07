import pymysql
from flask import *
# create app
app=Flask(__name__)
# create route
@app.route('/cars')
# create function
def mpesa():
    # connect to the database
    con=pymysql.connect(host='localhost',user='root',password='',database='myshop_git')
    # create cursor to execute sql
    cursor=con.cursor()
    sql='SELECT * FROM mpesa'
    cursor.execute(sql)
    # check if the table is empty
    # if statement
    if cursor.rowcount==0:
        return render_template('mpesa.html',msg='No available products')
    else:
        data=cursor.fetchall()
        return render_template('mpesa.html',rows=data)
# mpesa transaction code
# import requests
import requests #send requests to safaricom mpesa
import datetime #the exact date and time
from requests.auth import HTTPBasicAuth #gives permission (authorization)
import base64 #encoding and decoding (encryption)
# github.com/modcomlearning/mpesa_sample
# copy code from line 7 to 58
@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            # GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return  'Please Complete Payment in Your Phone'
        else:
            return redirect('/cars')
app.run(debug=True)