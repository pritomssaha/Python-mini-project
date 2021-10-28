import requests
import os
from datetime import date
from datetime import timedelta
from twilio.rest import Client

url = "https://www.alphavantage.co/query"
symbol = "TSLA"
apikey = os.environ['API_KEY']

param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": apikey
}


def send_sms(data):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token =  os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=data,
        from_= os.environ['from_number'],
        to= os.environ['to_number']
    )


today = (date.today())
yesterday = today - timedelta(days=1)
day_before_yesterday = str(today - timedelta(days=2))
today = str(today)
yesterday = str(yesterday)

response = requests.get(url=url, params=param)
data = response.json()

yesterday_price = float(data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_price = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])
percentile = (yesterday_price - day_before_yesterday_price) / day_before_yesterday_price * 100
formatted_num = '{0:.2f}'.format(percentile)

print(formatted_num)

if percentile > 0:
    data = f"Tesla price is up by ⬆{percentile}%️"
    send_sms(data)
else:
    data = f"Tesla price is up by ⬇{percentile}%️"
    send_sms(data)
