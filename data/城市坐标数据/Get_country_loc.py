import json,requests,os,csv
from bs4 import BeautifulSoup

country_list = ['Italy','Germany','United kingdom','India']
country_ch   = ['意大利','德国','英国','印度']
country_ench = dict(zip(country_list,country_ch))
with open('country_name.json') as f:
    country_dict = json.load(f)

for country in country_list:
    filename = country_ench[country]+'.csv'
    if not os.path.exists(filename):
        with open(filename,'w',encoding='utf-8',newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['num','city','population(2000)','Latitude(DD)','longitude(DD)'])

    url1 = "http://www.tageo.com/index-e-{}-cities-{}.htm".format(country_dict[country],country_dict[country].upper())
    url2 = "http://www.tageo.com/index-e-{}-cities-{}-step-1.htm".format(country_dict[country],country_dict[country].upper())
    url_list = [url1,url2]

    for url in url_list:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml').find('table',class_='V2').find_all('tr')[1:]
        for tr in soup:
            # print(tr)
            td = tr.find_all('td')
            row = [td[0].string,td[1].b.string,td[2].string,td[3].string,td[4].string]
            with open(filename,'a',encoding='utf-8',newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(row)
