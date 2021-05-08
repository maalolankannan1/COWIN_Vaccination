import requests
import json
import smtplib, ssl
import time
from datetime import date, datetime, timedelta

## DECLARING CONSTANTS ##
## Change values here ##
port = 465                                  # For SSL NEEDNT CHANGE
smtp_server = "smtp.gmail.com"
sender_email = "sender_mail@gmail.com"      # Replace with your sender address
receiver_email = "receiver_mail@gmail.com"  # Replace with receiver address
password = "password"                       # Replace with your sender email password
dist_id = 571                               # Replace with your District ID obtained by running find_dist.py

## DONT CHANGE VALUES BEYOND HERE ##

today = date.today()
tday = today.strftime("%d-%m-%Y")
dates = [(today + timedelta(days = i)).strftime("%d-%m-%Y") for i in range(0,7)]
while(True):
    r = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={dist_id}&date={tday}', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    slots = json.loads(r.content)
    datedict = {}
    for date in dates:
        datedict[date] = []

    for centrs in slots["centers"]:
        for ses in centrs["sessions"]:
            if(ses["min_age_limit"] == 18):
                datedict[ses["date"]].append([centrs["name"],centrs["address"],centrs["fee_type"],ses["available_capacity"],ses["vaccine"]])
    s = ""
    fl = False
    for key,values in datedict.items():
        s=s+f"\n{key}\n"
        for val in values:
            if(val[3]>0):
                s=s+f"{val}\n"
                fl = True

    if(fl == True):
        message = f"""\
        Subject: COWIN_VAC

        This message is sent from Python. 
        {s} """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print("SLOTS PRESENT")
    else:
        print("NO AVAILABLE SLOTS")

    time.sleep(30)
