from BeautifulSoup import BeautifulSoup as b
from collections import Counter
import urllib2, numpy
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_Question_Time_episodes')
html = response.read()

soup = b(html)

people = []

tables = soup.findAll('table','wikitable')[2:] #First two tables are other content
year_headers = soup.findAll('h2')[2:-4] # Likewise with headers
years = []

for year in year_headers:
    spans = year.findAll('span')
    years.append(int(spans[0].text))

for i, table in enumerate(tables[-10:]):
    print i
    for row in table.findAll('tr'):
        cols = row.findAll('td')
        if len(cols) >= 3:        
            names = cols[2]
            nstring = names.getText().split(',')            
            for name in nstring:
                people.append(name)
        else:
            continue


counts = Counter(people)

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
plt.show()