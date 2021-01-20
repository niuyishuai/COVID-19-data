# coding:UTF-8
# using file "time_series_covid19_confirmed_global.csv" from dataset made by John Hopkins University.
# for all files, clone https://github.com/CSSEGISandData/COVID-19.git
import datetime,os,csv
import pandas as pd
from sys import argv

def get_data(Region='France',level='country'):
    # Region:     str, the name of Country/Region, default value = 'France'
    # level:      str, 'province' or 'country' level, default value = 'country'

    check_dataset()
    if not level in ['province','country']:
        print('level error')
        exit(-1)
    df = pd.read_csv('time_series_covid19_confirmed_global.csv',error_bad_lines=False)
    df1 = pd.read_csv('time_series_covid19_deaths_global.csv',error_bad_lines=False)
    df2 = pd.read_csv('time_series_covid19_recovered_global.csv',error_bad_lines=False)
    if not Region in list(df['Country/Region']):
        print('Region name error')
        exit(-1)

    data = df.groupby(['Country/Region']).get_group(Region).drop(['Country/Region','Lat','Long'],axis=1)
    data1 = df1.groupby(['Country/Region']).get_group(Region).drop(['Country/Region','Lat','Long'],axis=1)
    data2 = df2.groupby(['Country/Region']).get_group(Region).drop(['Country/Region','Lat','Long'],axis=1)

    data.rename(columns=lambda x:x[:-2]+'20'+x[-2:], inplace=True)
    data1.rename(columns=lambda x:x[:-2]+'20'+x[-2:], inplace=True)
    data2.rename(columns=lambda x:x[:-2]+'20'+x[-2:], inplace=True)

    if os.path.exists('./data/'+Region+'/') == False:
        os.makedirs('./data/'+Region+'/')

    # write to .csv
    if level == 'country':
        file = data.drop(['Province/Sta20te'],axis=1).sum().to_frame()
        file.columns = ['Confirmed']
        # add Deaths Recovered
        file['Deaths'] = data1.drop(['Province/Sta20te'],axis=1).sum().tolist()
        file['Recovered'] = data2.drop(['Province/Sta20te'],axis=1).sum().tolist()
        file['CurrentConfirmed'] = file['Confirmed'] - file['Deaths'] - file['Recovered']
        filename = './data/'+Region+'/'+level+'.csv'
        file.to_csv(filename)
    else:
        data.set_index(['Province/Sta20te'], inplace=True)
        data1.set_index(['Province/Sta20te'], inplace=True)
        data2.set_index(['Province/Sta20te'], inplace=True)

        for index in data.index:
            file = data.loc[index].to_frame()
            file.columns = ['Confirmed']
            file['Deaths'] = data1.loc[index].tolist()
            file['Recovered'] = data2.loc[index].tolist()
            file['CurrentConfirmed'] = file['Confirmed'] - file['Deaths'] - file['Recovered']
            filename = './data/'+Region+'/'+str(index)+'.csv'
            file.to_csv(filename)

def get_name(Region='all'):
    # Region: str, country name or 'all'
    check_dataset()
    df = pd.read_csv('time_series_covid19_confirmed_global.csv',error_bad_lines=False)
    if Region == 'all':
        namelist = sorted(list(set(df['Country/Region'])))
    else:
        if not Region in list(df['Country/Region']):
            print('Region name error')
            exit(-1)
        group_1 = df.groupby('Country/Region').get_group(Region)['Province/State']
        namelist = list(set(group_1))

    # write to csv
    if os.path.exists('./name/') == False:
        os.makedirs('./name/')
    filename = './name/'+Region+'.csv'
    with open(filename,'w',newline='') as f:
        csv_writer = csv.writer(f)
        for name in namelist:
            csv_writer.writerow([name])

def check_dataset():
    filepath = './time_series_covid19_recovered_global.csv'
    if not os.path.exists(filepath):
        if os.path.exists('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'):
            print('Please run this file under directory /COVID-19/csse_covid_19_data/csse_covid_19_time_series/')
        print('Data files don\'t exist! You can download it or git clone https://github.com/CSSEGISandData/COVID-19.git')

if __name__ == "__main__":
    # get_name('France')

    if len(argv) > 1:
        region = argv[1]
        if len(argv) > 2:
            level = argv[2]
            get_data(region,level)
        else:
            get_data(region)
    else:
        get_data('United Kingdom','province')
