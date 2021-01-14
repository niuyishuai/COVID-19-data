import json
from bs4 import BeautifulSoup

with open('country_name.html','r',encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(),'lxml')
a_list = soup.find('table',border=0).tr.find_all('a')
country_dict = {}
for a in a_list:
    if '-e-' in a['href']:
        country_dict[a.string] = a['href'].split('.')[0].split('-')[-1]
with open('country_name.json','w',encoding='utf-8') as g:
    g.write(json.dumps(country_dict))