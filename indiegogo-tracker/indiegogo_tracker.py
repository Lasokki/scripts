""" 
Simple script for pulling balance of a Indiegogo-campaign.

Usage:
indiegogo_tracker.py "http://URL" seconds_between_checks
Both fields are mandatory

Author: Erkki Mattila, 2014
"""

import requests, re, time, sys, BeautifulSoup, datetime

numpa = re.compile('\d+')
session = requests.session()
url = sys.argv[1]

old_balance = 0
balance = 0
first_run = True

while True:
    req = session.get(url)

    doc = BeautifulSoup.BeautifulSoup(req.content)

    title = doc.find("h1")
    
    bal_div = doc.find("div", attrs={"class" : "i-balance"})
    bal_span = bal_div.find("span", attrs={"class" : "currency currency-xlarge"})

    old_balance = balance
    dollar_format_balstr = bal_span.contents[0].string
    
    ballist = numpa.findall(dollar_format_balstr)

    balstring = ""
    for i in ballist:
        balstring = balstring + i

    balance = int(balstring)

    if first_run == True:
        old_balance = balance
        first_run = False

    delta_bal_str = ""
    if balance > old_balance:
        delta_balance = balance - old_balance
        delta_bal_str = " | +$" + str(delta_balance)

    print title.string
    print datetime.datetime.now().strftime("%H:%M:%S") + " | " + dollar_format_balstr + delta_bal_str
    time.sleep(float(sys.argv[2]))
