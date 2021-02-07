import requests as rqt
import datetime as dts
import yagmail
# import sched
import time
from keep_alive import keep_alive

# s = sched.scheduler(time.time, time.sleep)

# user credentials
MAIL = "your_id@yahoo.com"
PASSCODE = "your-password"

MY_LAT = 12.971599
MY_LNG = 77.594566
MY_LOC = (MY_LAT, MY_LNG)
# print(MY_LOC)
iss_location = ()


def iss_nearby():
    global iss_location
    # Get ISS location
    iss_api = rqt.get("http://api.open-notify.org/iss-now.json")
    data_iss = iss_api.json()['iss_position']
    iss_lat = float(data_iss['latitude'])
    iss_lng = float(data_iss['longitude'])
    iss_location = (iss_lat, iss_lng)
    print(iss_location)
    # Check if ISS is close to me
    if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LNG - 5 <= iss_lng <= MY_LNG + 5:
        print("bingo\n ISS is above you")
        return True


def night_sky():
    # Check for sun rise and sun set

    # Providing parameters to api's
    location = {"lat": MY_LAT, "lng": MY_LNG, "formatted": 0}

    # Getting Current Time
    now = dts.datetime.now()
    current_hr = now.hour
    # print(type(current_hr))

    sn_api = rqt.get("https://api.sunrise-sunset.org/json", params=location)
    sn_api.raise_for_status()
    data = sn_api.json()['results']
    sunrise = data['sunrise']
    sunset = data['sunset']
    morning = int(sunrise.split("T")[1].split(":")[0])
    evening = int(sunset.split("T")[1].split(":")[0])

    if current_hr >= evening or current_hr <= morning:
        print("It's Dark out there")
        return True


# Mail to ppl


def mailer():
    with yagmail.SMTP(user=MAIL,
                      password=PASSCODE,
                      host='smtp.mail.yahoo.com',
                      port=587,
                      smtp_ssl=False,
                      smtp_starttls=True) as server:
        if iss_nearby() and night_sky():
            subject = 'ISS is nearby'
            html = "<h1>ISS is above head</h1>"
            body = f"Peep out the night sky,<br>ISS Location:{iss_location}"
            server.send(to="where_to_send@gmail.com",
                        subject=subject,
                        contents=[html, body])
            # s.enter(delay=60, priority=1, action=mailer)


keep_alive()
# Call the function
while True:
    print("Running...")
    mailer()
    time.sleep(60)

