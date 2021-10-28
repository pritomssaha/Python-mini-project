import requests
import smtplib
from geopy.geocoders import Nominatim
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


def get_location(current_position):
    app = Nominatim(user_agent="tutorial")

    # get location raw data
    location = app.geocode(current_position).raw
    # print raw data
    longitude = location["lon"]
    latitude = location["lat"]
    return [longitude, latitude]


res = requests.get("http://api.open-notify.org/iss-now.json")
data = res.json()
print(data["iss_position"]["latitude"])

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

get_current_position = input("What is your current position: ")
latitude = float(get_location(get_current_position)[1])
longitude = float(get_location(get_current_position)[0])

if latitude - 1 <= iss_latitude <= latitude + 1 and longitude - 1 <= iss_longitude <= longitude + 1:
    send_email()
