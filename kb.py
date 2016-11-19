# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
import classes
import locale

locale.setlocale(locale.LC_ALL, 'cz')

url = "https://www.kb.cz"

url_ucty = "https://www.kb.cz/cs/transparentni-ucty/"

r = requests.get(url_ucty)

doc = lh.fromstring(r.text)

page_no = 1

def get_transactions(url):
    request = requests.get(url)
    doc = lh.fromstring(request.text.encode('ISO-8859-1'))
    for row in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        sender = None
        receiver = None
        datum = None
        amount = None
        currency = None
        for i, cell in enumerate(row.cssselect('tr > td:nth-child(1)')):
            if i==0:
                datum = cell.text
            elif i==3:
                sender = cell.text
            elif i==2:
                receiver = cell.text
        for i, cell in enumerate(row.cssselect('tr > td:nth-child(4)')):
            print(cell.text[:-3].replace(u'\xa0',''))
            amount = locale.atof(cell.text[:-3].replace(u'\xa0',''))
            currency = cell.text[-3:]

        if sender and receiver and datum and currency and amount:
            transaction = classes.Transaction(sender, receiver, datum, amount, currency)



while requests.get(url_ucty+"index-"+str(page_no)+".shtml").status_code == 200:
    for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        url_account = url + div.cssselect('td.ar > a')[0].get('href')
        first_page = requests.get(url_account)

        print (url_account)

        doc2 = lh.fromstring(first_page.text.encode('ISO-8859-1'))
        account_num = doc2.cssselect("#content > h1")[0].text
        try:
            account_name = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(2) > strong")[0].text
            account_balance = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(4) > strong")[0].text
            print(account_name)
            print(account_balance)
        except:
            pass

        get_transactions(url_account)
        x = 1

        while requests.get(url_account[:-6]+"-{}.shtml".format(str(x))).status_code == 200:
            page_url = (url_account[:-6]+"-"+str(x)+".shtml")
            get_transactions(page_url)
            x += 1



    page_no +=1
