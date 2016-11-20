# -*- coding: utf-8 -*-

import requests
import lxml.html as lh
import classes
import locale
import database_manager as dm

locale.setlocale(locale.LC_ALL, 'cs_CZ')

url = "https://www.kb.cz"
url_ucty = "https://www.kb.cz/cs/transparentni-ucty/"

r = requests.get(url_ucty)

doc = lh.fromstring(r.text)

page_no = 1
fp = True

def get_transactions(url, acc_num):
    transactions = []
    request = requests.get(url)
    doc = lh.fromstring(request.text.encode('ISO-8859-1'))
    for row in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        sender = None
        receiver = None
        datum = None
        amount = None
        currency = None
        for i, cell in enumerate(row.cssselect('tr > td:nth-child(1)')):
            if i == 0:
                datum = cell.text
            elif i == 3:
                sender = cell.text[:-5]
            elif i == 2:
                receiver = acc_num
        for i, cell in enumerate(row.cssselect('tr > td:nth-child(4)')):
            amount = locale.atof(cell.text[:-3].replace(u'\xa0', ''))
            currency = cell.text[-3:]

        if sender and receiver and datum and currency and amount:
            transactions.append(classes.Transaction(sender, receiver, datum, amount, currency))

    return transactions


try:
    while requests.get(url_ucty + "index-" + str(page_no) + ".shtml").status_code == 200:
        if fp:
            doc = lh.fromstring(requests.get(url_ucty).text)
            fp = False
            page_no -= 1
        else:
            doc = lh.fromstring(requests.get(url_ucty + "index-" + str(page_no) + ".shtml").text)
        am = dm.AccountsManager()
        tm = dm.TransactionsManager()
        for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
            url_account = url + div.cssselect('td.ar > a')[0].get('href')
            first_page = requests.get(url_account)

            doc2 = lh.fromstring(first_page.text.encode('ISO-8859-1'))
            account_num = doc2.cssselect("#content > h1")[0].text[12:-5]
            bank_code = account_num[-4:]

            try:
                account_name = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(2) > strong")[0].text
                account_balance = doc2.cssselect("#content > div.highlight-block > ul > li:nth-child(4) > strong")[
                    0].text
                account_currency = account_balance[-2:]
            except IndexError as e:
                print("bordel", account_num)
                pass

            if account_name and account_currency and account_balance:
                account = classes.Account(account_num, account_name, bank_code, account_balance, account_currency,
                                          isTransparent=1)
                am.createAccounts([account])

            x = 1
            while requests.get(url_account[:-6] + "-{}.shtml".format(str(x))).status_code == 200:
                page_url = (url_account[:-6] + "-" + str(x) + ".shtml")
                transactions = get_transactions(page_url, account_num)
                x += 1
                tm.createTransactions(transactions)

            get_transactions(url_account, account_num)
        page_no += 1
except ConnectionError as e:
    pass
