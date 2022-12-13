import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 53.544388  # Your latitude
MY_LONG = 113.490929  # Your longitude
my_email = "pgpahnder@gmail.com"
password = "tbuunelzwugygrqd"


def is_position_close():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.

    return ((MY_LAT - 5 <= iss_latitude and MY_LAT + 5 >= iss_latitude) and (MY_LONG - 5 <= iss_longitude and MY_LONG + 5 >= iss_longitude))


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    return (time_now.hour >= sunset or time_now.hour <= sunrise)


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)
    if is_position_close() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="pgpahnded@yahoo.com",
                                msg="Subject:ISS Is Overhead\n\nGet outside you should be able to see the ISS in the night sky!!")

    else:
        print("Its not close")
