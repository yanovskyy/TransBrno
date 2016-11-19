# -*- coding: utf-8 -*-

import requests
import lxml.html as lh



url = "https://www.kb.cz"

r = requests.get('https://www.kb.cz/cs/transparentni-ucty/')

doc = lh.fromstring(r.text)


for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
    url_account = url + div.cssselect('td.ar > a')[0].get('href')
    first_page = requests.get(url_account)

    doc2 = lh.fromstring(first_page.text)

    with open("C:/Users/pavli/Desktop/tst.html", 'w') as f:
        f.write(str(first_page.text.encode('utf-8')))

    for div2 in doc2.cssselect('#content > div.listing-object > table > tbody > tr'):
        for div3 in div2.cssselect('td > table > tbody > tr > td'):
            print(div3.text.encode('utf-8').decode('utf-8', "ignore"))
#        print(div2.cssselect('td:nth-child(2) > table > tbody > tr:nth-child(1) > td')[0].text.encode('utf-8'))

#content > div.listing-object > table > tbody > tr:nth-child(5) > td:nth-child(2) > table > tbody > tr.breakable > td
#content > div.listing-object > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td
#content > div.listing-object > table.transaction-table.stack-table.stack-table-sm.listing-table.large-only.small-only > tbody > tr:nth-child(19) > td > table > tbody > tr:nth-child(2) > td
#content > div.listing-object > table.transaction-table.stack-table.stack-table-sm.listing-table.large-only.small-only > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(3) > td
"""
    print(first_page.text.encode('utf-8'))

    x = 1
    while requests.get(url_account[:-6]+"-"+str(x)+".shtml").status_code == 200:
        print(x)
        x += 1


    #s = requests.get(url + div.cssselect('td.ar > a')[0].get('href'))

    #with open("C:/Users/pavli/Desktop/tst.html", 'w') as f:
    #    f.write(str(s.text.encode('utf-8')))

#content > div.pagination-wrapper > ul > li:nth-child(6)
"""
