import requests
import lxml.html as lh

url = "https://www.kb.cz"

r = requests.get('https://www.kb.cz/cs/transparentni-ucty/')

doc=lh.fromstring(r.text)


for div in doc.cssselect('#content > div.listing-object > table > tbody > tr'):
    url_account = url + div.cssselect('td.ar > a')[0].get('href')
    first_page = requests.get(url_account)

    x = 1
    while requests.get(url_account[:-6]+"-"+str(x)+".shtml").status_code == 200:
        print(x)
        x += 1


    #s = requests.get(url + div.cssselect('td.ar > a')[0].get('href'))

    #with open("C:/Users/pavli/Desktop/tst.html", 'w') as f:
    #    f.write(str(s.text.encode('utf-8')))

#content > div.pagination-wrapper > ul > li:nth-child(6)
