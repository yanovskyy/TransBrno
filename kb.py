# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
import classes
import locale

url = "https://www.kb.cz"

url_ucty = "https://www.kb.cz/cs/transparentni-ucty/"

r = requests.get(url_ucty)

doc = lh.fromstring(r.text)

page_no = 1

def get_transactions(url):
    request = requests.get(url)
    doc = lh.fromstring(request.text.encode('ISO-8859-1'))
    for row in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        for cell in row.cssselect('tr > td'):
            if len((row.cssselect("tr > td"))) != 11:
                print(cell.text)


while requests.get(url_ucty+"index-"+str(page_no)+".shtml").status_code == 200:
    for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        url_account = url + div.cssselect('td.ar > a')[0].get('href')
        first_page = requests.get(url_account)
        doc2 = lh.fromstring(first_page.text.encode('ISO-8859-1'))
        account_num = doc2.cssselect("#content > h1")[0].text[:-5]
        bank_code = account_num[-4:]
        try:
            account_name = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(2) > strong")[0].text
            account_balance = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(4) > strong")[0].text
            account_currency = account_balance[-2:]
            account_num = classes.Account(account_num, account_name, bank_code, account_balance, account_currency,
                                      isTransparent=1)
        except:
            pass

        get_transactions(url_account)
        x = 1

        while requests.get(url_account[:-6]+"-{}.shtml".format(str(x))).status_code == 200:
            page_url = (url_account[:-6]+"-"+str(x)+".shtml")
            get_transactions(page_url)
            x += 1


    page_no +=1