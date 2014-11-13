from BeautifulSoup import BeautifulSoup as b
from collections import Counter
import urllib2, numpy
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://en.wikipedia.org/wiki/Chris_Huhne')
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
            if len(ass) >= 1:
                print ass[-1].text
                break
            
text = [p.getText() for p in soup.findAll('p')]
ttext = "".join(text).lower()

C = Counter(ttext.split())
print C['he'], C['she']

if C['he'] > C['she']:
    tonk = 'Male'

elif C['she'] > C['he']:
    tonk = 'Female'

else:
    tonk = 'Not Found'
    
print tonk