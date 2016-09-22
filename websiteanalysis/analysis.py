from bs4 import BeautifulSoup
from slugify import slugify

host='energie-campus.cybus.io'
port='1883'

soup = BeautifulSoup(open("die-technik"), "html5lib")

def codeWithoutClass(tag):
    return tag.name=='code' and not tag.has_attr('class') and tag.string.find('{')<0

f=open('staubsauger_config.txt', 'w')

all_widgets=soup.find_all('div', class_='textwidget')
for w in all_widgets:
    h3=w.find('h3')
    if h3!=None:
        name=slugify(w.find('h3').string)

        for tr in w.find_all('tr'):
            first_td=tr.find('td')
            if first_td!=None:
                content=first_td.string
                if content.find('-')!=0 and not content.endswith('/set'):
                    f.write(name+' '+first_td.string+' '+host+' '+port+'\n')

f.close()
