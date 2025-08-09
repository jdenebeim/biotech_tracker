#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jack Denebeim
"""

import os
import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.text import MIMEText

email = os.environ["EMAIL_ADDRESS"]
password = os.environ["EMAIL_APP_PASSWORD"]
url = "https://www.biospace.com/biospace-layoff-tracker"

response = requests.get(url)
 
# Check if the request was successful
if response.status_code == 200:
    # Create a Beautiful Soup object
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
 
email_message = datetime.date.today().strftime("%B %d, %Y")

found_update = False

for child in (soup.find_all('b')):
    if (not found_update):
        for sib in child.next_siblings:
            if(sib.name == 'i'):
                mon = sib.text.split(sep = " ")[0]
                if ("." in mon):
                    mon_num = datetime.datetime.strptime(mon[:-1], '%b').month
                else:
                    mon_num = datetime.datetime.strptime(mon, '%B').month
                day_num = sib.text.split(sep = " ")[1]
                date = datetime.date(2025, int(mon_num), int(day_num))
                if (date == datetime.date.today()):
                    email_message += f"\nThere was an update!\n{url}"
                    found_update = True

if (not found_update):
    email_message += f"\nNo updates today.\n{url}"

def send_email(subject, body, sender_email, app_password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = sender_email  # sending to yourself

    with smtplib.SMTP('smtp.mail.me.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

print(email_message)   

send_email(
    subject="Layoff_Tracker_Update!",
    body=email_message,
    sender_email=email,
    app_password=password)
