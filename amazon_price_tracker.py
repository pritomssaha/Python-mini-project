from bs4 import BeautifulSoup
import requests
import smtplib
import os

email = os.environ['EMAIL']
password = os.environ['PASSWORD']


def send_email():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(email, password)
    connection.sendmail(from_addr=email, to_addrs=email,
                        msg=f"Subject: Hello \n\n iss satellite is close to your location")
    connection.close()


header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}
res = requests.get(
    "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=dp_fod_2?pd_rd_i=B08PQ2KWHS&psc=1",
    headers=header)
try:
    res_text = res.text
except res.raise_for_status():
    print(res.status_code)

soup = BeautifulSoup(res_text, "html.parser")
span = soup.findAll(name="span", class_="a-offscreen")
price = float(span[1].getText().split("$")[1])

if price < 100:
    send_email()
