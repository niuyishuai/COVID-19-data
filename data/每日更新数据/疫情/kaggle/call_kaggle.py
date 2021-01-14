# coding:UTF-8
# using file "covid_19_data.csv" from dataset "Novel Corona Virus 2019 Dataset" of SRK in Kaggle. 
import datetime,os,csv
import pandas as pd

def get_data(Region='Mainland China',level='province',start_time='20200122',end_time='20201231'):
    # Region:     str, the name of Country/Region, default value = 'Mainland China'
    # level:      str, 'province' or 'country' level, default value = 'province'
    # start_time: str, the first date with form "%Y%m%d", default value = '20200122'
    # end_time:   str, the last date with form "%Y%m%d", default value = 'last_observe'
    # return data_dict = {date:[[province_1,Confirmed,Deaths,Recovered],...]} (for country level, province_1 = Region)

    check_dataset()
    df = pd.read_csv('./nCov/covid_19_data.csv',error_bad_lines=False)
    if (Region in list(df['Country/Region'])) == False:
        print('Region name error')
        exit(-1)
    
    group_country = df.groupby(['Country/Region']).get_group(Region)
    if level == 'country':
        data = group_country.groupby(['ObservationDate'])[['Confirmed','Deaths','Recovered']]
    elif level == 'province':
        data = group_country.groupby(['ObservationDate'])[['Province/State','Confirmed','Deaths','Recovered']]
    else:
        print("level must be \'country\' or \'province\'")
        exit(-1)
    
    startdate = datetime.datetime.strptime(start_time,'%Y%m%d')
    enddate = datetime.datetime.strptime(end_time,'%Y%m%d')
    first_observe = list(group_country['ObservationDate'])[0]
    last_observe = list(group_country['ObservationDate'])[-1]
    start_file = datetime.datetime.strptime(first_observe,'%m/%d/%Y')
    end_file = datetime.datetime.strptime(last_observe,'%m/%d/%Y')
    if startdate < start_file:
        startdate = start_file
        start_time = start_file.strftime('%Y%m%d')
    if end_file < enddate:
        enddate = end_file
        end_time = end_file.strftime('%Y%m%d')

    data_dict = {}
    while startdate <= enddate:
        date = startdate.strftime('%m/%d/%Y')
        if level == 'province':
            data_date = data.get_group(date).values.tolist()
            data_dict[date] = data_date
        if level == 'country':
            data_date = data.get_group(date).sum().values.tolist()
            print(data_date)
            data_dict[date] = [[Region]+data_date]
        startdate += datetime.timedelta(days=+1)
        
    # Write to .csv
    
    if level == 'province':
        row0 = ['Date','Province/State','Confirmed','Deaths','Recovered']
    else:
        row0 = ['Date','','Confirmed','Deaths','Recovered']
    if os.path.exists('./kaggle/') == False:
        os.mkdir('./kaggle/')
    if os.path.exists('./kaggle/'+Region+'/') == False:
        os.mkdir('./kaggle/'+Region+'/')
    filename = './kaggle/'+Region+'/'+level+'_'+start_time+'_'+end_time+'.csv'
    with open(filename,'w',newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(row0)
        for date in data_dict:
            for row in data_dict[date]:
                csv_writer.writerow([date]+row)
    
    return data_dict

def get_name(Region='all'):
    # Region: str, country name or 'all'
    # return namelist = [province_1,...], if Region = 'all', namelist = [country_1,...]
    check_dataset()
    df = pd.read_csv('./nCov/covid_19_data.csv',error_bad_lines=False)
    if Region == 'all':
        group_1 = df['Country/Region']
        namelist = []
        for name in group_1:
            if (name in namelist) == False:
                namelist.append(name)
    else:
        if (Region in list(df['Country/Region'])) == False:
            print('Region name error')
            exit(-1)
        group_1 = df.groupby('Country/Region').get_group(Region)['Province/State']
        namelist = []
        for name in group_1:
            if (name in namelist) == False:
                namelist.append(name)

    # write to csv
    if os.path.exists('./kaggle/') == False:
        os.mkdir('./kaggle/')
    if os.path.exists('./kaggle/name/') == False:
        os.mkdir('./kaggle/name/')
    filename = './kaggle/name/'+Region+'.csv'
    with open(filename,'w',newline='') as f:
        csv_writer = csv.writer(f)
        for name in namelist:
            csv_writer.writerow([name])
    return namelist

def check_dataset():
    filepath = './nCov/covid_19_data.csv'
    if not os.path.exists(filepath):
        print('Downloading covid_19_data.csv')
        os.system('git clone https://github.com/hjp3268/nCov.git')

if __name__ == "__main__":
    get_name('all')
    # get_data(Region='US',level='province',start_time='20200122',end_time='20200124')