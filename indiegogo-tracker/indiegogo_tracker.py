#!/usr/bin/python

""" 
Simple script for pulling balance of a Indiegogo-campaign.

Usage:
indiegogo_tracker.py "http://URL" seconds_between_checks
Both fields are mandatory

Author: Erkki Mattila, 2014
"""

import requests, re, time, sys, BeautifulSoup, datetime

def get_doc(url):
    req = session.get(url)
    doc = BeautifulSoup.BeautifulSoup(req.content)
    return doc

def search_balance(doc):

    numpa = re.compile('\d+')
    
    bal_div = doc.find("div", attrs={"class" : "i-balance"})
    bal_span = bal_div.find("span", attrs={"class" : "currency currency-xlarge"})

    dollar_format_balstr = bal_span.contents[0].string
    
    ballist = numpa.findall(dollar_format_balstr)

    balstring = ""
    for i in ballist:
        balstring = balstring + i

    balance = int(balstring)

    return balance

def print_balance(balance, old_balance, title):
    delta_bal_str = ""
    if balance > old_balance:
        delta_balance = balance - old_balance
        delta_bal_str = " | +$" + str(delta_balance)
        
    print title.string
    print datetime.datetime.now().strftime("%H:%M:%S") + " | " + str(balance) + delta_bal_str

if __name__ == "__main__":
    session = requests.session()
    url = sys.argv[1]
    delay = float(sys.argv[2])

    old_balance = 0
    balance = 0

    while True:
        doc = get_doc(url)
        balance = search_balance(doc)
        title = doc.find("h1")
        print_balance(balance, old_balance, title)
        old_balance = balance
        time.sleep(delay)
