import pandas as pd
import requests, json, re, os
from lxml import etree
# from bs4 import beautifulSoup

def changeDate(x):
    x = x.split(' ')
    date_dict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    x[0] = date_dict[x[0]]
    x[1] = x[1][:-1]
    return '/'.join(x)

def get_country(country):
    country_url = 'https://www.worldometers.info/coronavirus/country/{}/'.format(country)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    r = requests.get(country_url, headers=headers).text
    tree = etree.HTML(r)
    tree = tree.xpath('//*[@id="usa_table_countries_today"]/tbody[1]/tr')
    for tr in tree[1:]:
        state = tr.xpath('.//a[@href]/text()')[0]
        get_state(country, state)
    get_state(country)



def get_state(country, state='country'):
    name_dict = {'coronavirus-cases-linear':'Confirmed', 'graph-active-cases-total':'CurrentConfirmed','coronavirus-deaths-linear':'Deaths'}

    if state == 'country':
        state_url = 'https://www.worldometers.info/coronavirus/{}/{}'.format(state, country)
    else:
        if country.lower() == 'us':
            country = 'usa'
        state = state.replace(' ','-')
        state_url = 'https://www.worldometers.info/coronavirus/{}/{}'.format(country, state)
    if os.path.exists('./{}/{}.csv'.format(country, state)):
        return 0
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    r = requests.get(state_url, headers=headers).text
    date = []
    df = pd.DataFrame()
    tree = etree.HTML(r)
    tree = tree.xpath('//script[@type="text/javascript"]')
    for sc in tree:
        s = etree.tostring(sc).decode()
        if 'Highcharts' in s[:50]:
            s = s.split('{',1)
            name = re.findall('\'(.*?)\'', s[0], re.S)[0]
            if name in name_dict:
                name = name_dict[name]
                dates = re.findall('categories: \[(.*?)\]', s[1], re.S)[0][1:-1].split('","')
                date = dates
                series = re.findall('data: \[(.*?)\]', s[1], re.S)[0].split(',')
                df[name] = series
    df['date'] = date
    df['date'] = df['date'].apply(changeDate)
    df = df.set_index('date')
    print(list(df.columns))
    df = df[['Confirmed','Deaths','CurrentConfirmed']]

    if country.lower() == 'us':
        country = 'usa'
    if not os.path.exists('./{}/'.format(country)):
        os.mkdir('./{}/'.format(country))
    df.to_csv('./{}/{}.csv'.format(country, state))

get_country('us')
