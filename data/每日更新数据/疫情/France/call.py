import pandas as pd
from bs4 import BeautifulSoup
import json

def get_code():
    code = {}
    with open('France.html','r',encoding='utf-8') as f:
        Soup = BeautifulSoup(f,'lxml')
        
    a = Soup.table.tbody.find_all('tr')
    for b in a[2:]:
        if b.td.div.string == '海外省及大区':
            break
        name = b.find_all('td')[-2].find_all('div')[-1].string
        num = b.find_all('td')[-1].div.string
        code[num] = name
    hjp = Soup.find('div',class_='hjp').string.replace('    ','').split('\n')
    for b in hjp:
        name = b[b.find('（')+1:b.find('）')]
        num = b[-3:]
        code[num] = name
    with open('France_code.json','w',encoding='utf-8') as f:
        json.dump(code,f)

def cum_case(group):
    indexs = list(group.index)
    for j in range(1,len(indexs)):
        group.at[indexs[j],'cumCase'] = group.at[indexs[j],'cumCase'] + group.at[indexs[j-1],'cumCase']


def get_data():
    df_pos = pd.read_csv('dep-pos.csv',sep=';',low_memory=False)[['dep','jour','P']]
    group = df_pos.groupby(['dep','jour']).sum()
    group = group.reset_index()
    group.columns = ['dep','date','cumCase']
    group = group.groupby('dep')
    for i in group:
        cum_case(i[1])
        i[1].to_csv('cum-case.csv',mode='a',index=0,header=0)

def get_DR():
    df = pd.read_csv('hosp.csv',sep=';')[['dep',"sexe",'jour','rad','dc']]
    df.columns = ['dep',"sex",'date','Recovered','Deaths']
    group = df.groupby('sex').get_group(0).drop(['sex'],axis=1)
    group.to_csv('RecoverDeath.csv',index=0)



# get_code()
# get_data()
get_DR()