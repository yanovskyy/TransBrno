import requests
import lxml.html as lh


url = "https://www.kb.cz"

r = requests.get('https://www.kb.cz/cs/transparentni-ucty/')

doc = lh.fromstring(r.text.encode('ISO-8859-1'))


for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
    url_account = url + div.cssselect('td.ar > a')[0].get('href')
    first_page = requests.get(url_account)

    #print(first_page.encoding)

    doc2 = lh.fromstring(first_page.text.encode('ISO-8859-1'))

    for div2 in doc2.cssselect('#content > div.listing-object > table > tbody > tr'):
        for div3 in div2.cssselect('td > table > tbody > tr > td'):
            #print('firstpage')
            print(div3.text)
#        print(div2.cssselect('td:nth-child(2) > table > tbody > tr:nth-child(1) > td')[0].text.encode('utf-8'))

    x = 1

    while requests.get(url_account[:-6]+"-"+str(x)+".shtml").status_code == 200:
        for div2 in doc2.cssselect('#content > div.listing-object > table > tbody > tr'):
            for div3 in div2.cssselect('td > table > tbody > tr > td'):
                print(div3.text)
        #print('nextpage {}'.format(x))
        x += 1


    #s = requests.get(url + div.cssselect('td.ar > a')[0].get('href'))

    #with open("C:/Users/pavli/Desktop/tst.html", 'w') as f:
    #    f.write(str(s.text.encode('utf-8')))

#content > div.pagination-wrapper > ul > li:nth-child(6)
