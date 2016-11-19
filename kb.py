# -*- coding: utf-8 -*-

import requests
import lxml.html as lh

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
            print(cell.text)
            # return slovnik dat


while requests.get(url_ucty+"index-"+str(page_no)+".shtml").status_code == 200:
    for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
        url_account = url + div.cssselect('td.ar > a')[0].get('href')
        first_page = requests.get(url_account)
        doc2 = lh.fromstring(first_page.text.encode('ISO-8859-1'))

        get_transactions(url_account)


        # print(doc2.cssselect("#content > h1")[0].text)
        #for div2 in doc2.cssselect('#content > div.listing-object > table > tbody > tr'):
         #   for div3 in div2.cssselect('tr > td'):
          #      pass
               # print(div3.text)
            #print("################################")

        #print(first_page.text.encode('utf-8'))

        x = 1

        while requests.get(url_account[:-6]+"-{}.shtml".format(str(x))).status_code == 200:
            page_url = (url_account[:-6]+"-"+str(x)+".shtml")
            get_transactions(page_url)
            #for div2 in doc2.cssselect('#content > div.listing-object > table > tbody > tr'):
             #   for div3 in div2.cssselect('tr > td'):
              #     pass
                   # print(div3.text)
            #print('nextpage {}'.format(x))
            x += 1


    page_no +=1

        #s = requests.get(url + div.cssselect('td.ar > a')[0].get('href'))

        #with open("C:/Users/pavli/Desktop/tst.html", 'w') as f:
        #    f.write(str(s.text.encode('utf-8')))

    #content > div.pagination-wrapper > ul > li:nth-child(6)
