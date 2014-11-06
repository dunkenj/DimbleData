from BeautifulSoup import BeautifulSoup as b
from collections import Counter
import urllib2, numpy
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://en.wikipedia.org/wiki/Nigel_Farage')
html = response.read()

soup = b(html)

trs = soup.findAll('tr')

for tr in trs:
    a = tr.findAll('th')
    if len(a) >= 1:
        k = a[0]
        if k.text == 'Political party':
            t = tr.findAll('td')
            ass = t[0].findAll('a')
            print ass[-1].text
            break
            