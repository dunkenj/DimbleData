from BeautifulSoup import BeautifulSoup as b
from collections import Counter
import urllib2, numpy
import matplotlib.pyplot as plt
import sqlite3 as lite
import numpy
# Creates or opens a file called mydb with a SQLite3 DB
db = lite.connect('QTdb')


response = urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_Question_Time_episodes')
html = response.read()

soup = b(html)

people = []
genders = []
parties = []

tables = soup.findAll('table','wikitable')[2:] #First two tables are other content
year_headers = soup.findAll('h2')[2:-4] # Likewise with headers
years = []

def find_party_get_party_party_on(url):
    response = urllib2.urlopen(url)
    html = response.read()

    poop = b(html)

    trs = poop.findAll('tr')
    
    drunk = 'Unknown'
    
    for tr in trs:
        a = tr.findAll('th')
        if len(a) >= 1:
            k = a[0]
            if k.text == 'Political party':
                t = tr.findAll('td')
                ass = t[0].findAll('a')
                if len(ass) >= 1:
                    drunk = ass[-1].text
                    break
                
    text = [p.getText() for p in poop.findAll('p')[:5]]
    conc_text = "".join(text).lower()

    C = Counter(conc_text.split())
    #print C['he'], C['she']

    if C['he'] > C['she']:
        tonk = 'Male'

    elif C['she'] > C['he']:
        tonk = 'Female'

    else:
        tonk = 'Not Found'
    
    return drunk, tonk

for year in year_headers:
    spans = year.findAll('span')
    years.append(int(spans[0].text))

for i, table in enumerate(tables[-4:]):
    print i
    for row in table.findAll('tr'):
        cols = row.findAll('td')
        if len(cols) >= 3:
            links = cols[2].findAll('a')
            names = []
            for link in links:
                purl = 'http://en.wikipedia.org'+link.get('href')
                if '#' not in purl:
                    print link.text,
                    print purl,
                    party, gender = find_party_get_party_party_on(purl)
                    print party, gender
                    genders.append(gender)
                    parties.append(party)
                    names.append(link.text)
                    people.append(link.text)
                    
            names2 = cols[2]            
            nstring = names2.getText().split(',')            
            for name in nstring:
                if name not in names:
                    names.append(name)
                    people.append(name)
            #print names
        else:
            continue


counts = Counter(people)

gendercount = Counter(genders)

parties = numpy.array(parties)

parties[parties == 'Scottish Conservative Party'] = 'Conservative'
parties[parties == 'Conservative Party'] = 'Conservative'
parties[parties == 'Labour Party'] = 'Labour'
parties[parties == 'Labour Co-operative'] = 'Labour'
parties[parties == 'Liberal Democrat'] = 'Liberal Democrats'
parties[parties == '[1]'] = 'Unknown'

partycount = numpy.array(Counter(parties).most_common(8)[1:])


order = numpy.argsort(counts.values())
names = numpy.array(counts.keys())[order][::-1]
appearances = numpy.array(counts.values())[order][::-1]


N = 20

app_percentage = (appearances[:N] / float(numpy.sum(appearances[:N]))) * 100


index = numpy.arange(N)+0.25
bar_width = 0.5

"""
PLOT THAT SHIT
"""




Fig = plt.figure(figsize=(10,6))
Ax = Fig.add_subplot(111)
Apps = Ax.bar(index,app_percentage,bar_width, color='dodgerblue',alpha=0.8,linewidth=0)
Ax.set_xticks(index+ 0.5*bar_width)
Ax.set_xticklabels(names[:N],rotation=90)
Ax.set_ylabel('Appearance Percentage')
amin,amax = numpy.min(app_percentage), numpy.max(app_percentage)

def autolabel(Bars):
    # attach some text labels
    for Bar in Bars:
        height = Bar.get_height()
        Ax.text(Bar.get_x()+Bar.get_width()/2., 1.03*height, '%.1f'%float(height),
                ha='center', va='bottom',fontsize=9)

autolabel(Apps)

Ax.set_ylim([amin-1,amax+1])
Ax.set_title('Top '+str(N)+' QT guests')
Fig.subplots_adjust(bottom=0.26,right=0.95,left=0.07)
Fig.savefig('QTappearances.png',fmt='png')

Fig2 = plt.figure(figsize=(8,6))
Ax2 = Fig2.add_subplot(111)

Ax2.pie(partycount[:,1],labels=partycount[:,0],autopct='%.1f%%',
        pctdistance=0.8)
Ax2.axis('equal')

Fig3 = plt.figure(figsize=(8,6))
Ax3 = Fig3.add_subplot(111)

Ax3.pie(gendercount.values(),labels=gendercount.keys(),autopct='%.1f%%')
Ax3.axis('equal')

plt.show()




db.close()