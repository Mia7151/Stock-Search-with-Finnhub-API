from flask import Flask,request,jsonify,make_response
import time
import datetime
import calendar
import dateutil.relativedelta
from datetime import date
import json
import requests




app = Flask(__name__,static_folder='static')

@app.route("/",methods=['GET'])
def index():
    return app.send_static_file('index3.html')

@app.route("/process", methods=['GET'])
def process():
    global api_key
    api_key="c7vg2oiad3i9ikp8201g"
    global symbol
    symbol = request.args.get('code')
    params = {
    'symbol':symbol,
    'token':api_key}
    resp = requests.get("https://finnhub.io/api/v1/stock/profile2",params)
    response = make_response(jsonify(resp.json()),resp.status_code)
    return response

@app.route("/process1", methods=['GET'])
def process1():
    url2="https://finnhub.io/api/v1/quote?symbol={}&token={}".format(symbol, api_key)
    data1=requests.get(url2)
    stock=data1.json()
    stock['t'] = time.strftime("%d %B, %Y",time.localtime(stock['t']))

    url3="https://finnhub.io/api/v1/stock/recommendation?symbol={}&token={}".format(symbol, api_key)
    data2=requests.get(url3)
    recommend=data2.json()

    if(len(recommend)==0):
         recommend1={'buy':'N.A.', 'hold': 'N.A.', 'period': 'N.A.', 'sell': 'N.A.', 'strongBuy': 'N.A.', 'strongSell': 'N.A.', 'symbol': symbol}
    else:
        recommend1=recommend[0]
    stock.update(recommend1)
    return stock
    
@app.route("/process2", methods=['GET'])
def process2():
    d2 = datetime.datetime.utcnow()
    d1 = d2 + dateutil.relativedelta.relativedelta(months=-6,days=-1)
    time1 = calendar.timegm(d1.utctimetuple())
    time2 = calendar.timegm(d2.utctimetuple())
    url = "https://finnhub.io/api/v1/stock/candle?symbol={}&resolution=D&from={}&to={}&token={}".format(symbol,time1,time2,api_key)
    data=requests.get(url)
    data=data.json()


    listdata1 = []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

    for i in range(len(data['t'])):
        listdata1.append([data['t'][i]*1000,data['c'][i],data['v'][i]])
    
    return jsonify(listdata1)

@app.route("/process3", methods=['GET'])
def process3():
    today = date.today()
    days = datetime.timedelta(30)
    fromdate= today-days

    url = "https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token={}".format(symbol,fromdate,today,api_key)
    data=requests.get(url)
    data=data.json()
    result={}
    lens = len(data)
    count = 0

    for i in range(lens):
        if data[i]['image'] and data[i]['headline'] and data[i]['datetime'] and data[i]['url'] and len(result)<5 and count < lens:
            data[i]['datetime'] = time.strftime("%d %B, %Y",time.localtime(data[i]['datetime']))
            result[count] = data[i]
            count += 1
    return result




if __name__ == '__main__':
    app.run()