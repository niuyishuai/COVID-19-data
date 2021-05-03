import pandas as pd
import json

def changedate(x):
    date = x.split('-')
    date = date[1:3] + [date[0]]
    return '/'.join(date)

def get_code():
    data = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
    dicts = dict(zip(data['State_Code'], data['State']))
    with open('id.json', 'w') as f:
        json.dump(dicts, f)

def get_country():
    data = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
    data = data[['Date_YMD','Total Confirmed', 'Total Deceased', 'Total Recovered']]
    data['Current Confirmed'] = data['Total Confirmed'] - data['Total Recovered'] - data['Total Deceased']
    data.columns = ['date','Confirmed','Deaths','Recovered','CurrentConfirmed']

    data['date'] = data['date'].apply(changedate)
    data.to_csv('country.csv',index=False)

def get_province():
    data = pd.read_csv('https://api.covid19india.org/csv/latest/states.csv')
    data = data[['Date','State','Confirmed','Deceased','Recovered']]
    data.columns = ['Date','State','Confirmed','Deaths','Recovered']
    data.to_csv('states.csv',index=False)

# get_code()
get_country()
get_province()