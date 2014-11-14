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

people_all = []
genders_all = []
parties_all = []

people_multi = []
genders_multi = []
parties_multi = []

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

for i, table in enumerate(tables[:]):
    genders_temp = []
    people_temp = []
    parties_temp = []
    
    
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
                    #print purl,
                    party, gender = find_party_get_party_party_on(purl)
                    print party, gender
                    genders_all.append(gender)
                    parties_all.append(party)
                    names.append(link.text)
                    people_all.append(link.text)
                    
                    genders_temp.append(gender)
                    parties_temp.append(party)
                    
            names2 = cols[2]            
            nstring = names2.getText().split(',')            
            for name in nstring:
                if name not in names:
                    names.append(name)
                    people_all.append(name)
                    people_temp.append(name)
            #print names
        else:
            continue

    counts = Counter(people_temp)
    gendercount = Counter(genders_temp)
    partycount = Counter(parties_temp)

    total = numpy.sum(gendercount.values())
    for key in gendercount:
        gendercount[key] /= float(total)

    total = numpy.sum(partycount.values())
    for key in partycount:
        partycount[key] /= float(total)
        
    genders_multi.append(gendercount)
    parties_multi.append(partycount)
    people_multi.append(counts)
    

counts = Counter(people_all)

gendercount = Counter(genders_all)
total = numpy.sum(gendercount.values())
for key in gendercount:
    gendercount[key] /= total

parties = numpy.array(parties_all)

parties[parties == 'Scottish Conservative Party'] = 'Conservative'
parties[parties == 'Conservative Party'] = 'Conservative'
parties[parties == 'Labour Party'] = 'Labour'
parties[parties == 'Labour Co-operative'] = 'Labour'
parties[parties == 'Liberal Democrat'] = 'Liberal Democrats'
parties[parties == '[1]'] = 'Unknown'

partycount = numpy.array(Counter(parties_all).most_common(8)[1:])


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



Fig4 = plt.figure(figsize=(8,6))
Ax4 = Fig4.add_subplot(111)

MaleYears = [x['Male'] for x in genders_multi]
FemaleYears = [x['Female'] for x in genders_multi]
UnknownYears = [x['Not Found'] for x in genders_multi]

Ax4.plot(numpy.arange(len(years)),MaleYears,lw=3,label='Male')
Ax4.plot(numpy.arange(len(years)),FemaleYears,lw=3,label='Female')
Ax4.plot(numpy.arange(len(years)),UnknownYears,lw=3,label='Not found')

Ax4.set_xticks(numpy.arange(len(years))[::5])
Ax4.set_xticklabels(years[::5])
Ax4.set_ylim([0,1])
#Ax4.set_xlim([-0.5,9.5])
Ax4.legend()
Ax4.set_xlabel('Year')
Ax4.set_ylabel('Fraction of Guests')

plt.show()




db.close()