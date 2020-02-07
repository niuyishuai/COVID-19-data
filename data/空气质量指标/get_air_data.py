import pandas
import os
import json
import numpy

def get_site_city_dir():
    site_list_df = pandas.read_csv('site_list.csv',header=0, delimiter=',')
    code = site_list_df['监测点编码'].tolist()
    city = site_list_df['城市'].tolist()
    site_city_dir = dict(zip(code, city))
    return site_city_dir

def types():
    return ['AQI', 'PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO']

def statistic_day(file_path):
    df = pandas.read_csv(file_path, header=0, delimiter=',').fillna(method='ffill')
    df = df.fillna(method='bfill')
    df = df.rename(columns={'3207A.1': '3207A'})
    # types = ['AQI', 'PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO']
    type_index_dir = {'AQI': list(range(0, 360, 15)), 'PM2.5': list(range(1, 360, 15)),
     'PM10': list(range(3, 360, 15)), 'SO2': list(range(5, 360, 15)), 'NO2': list(range(7, 360, 15)),
     'O3':list(range(9, 360, 15)), 'CO':list(range(13, 360, 15))}
    type_mean_dir = {}
    for air_type in types():
        type_df_mean = df.ix[type_index_dir[air_type]].mean()
        type_df_mean = type_df_mean.drop(['date', 'hour'])
        type_mean_dir[air_type] = type_df_mean.values
        site_list = type_df_mean.index
    day_df = pandas.DataFrame(type_mean_dir, index=site_list).T
    day_df = day_df.rename(columns=get_site_city_dir())
    return day_df

def same_columns_mean(df):
    '''
    对dataframe中有相同列名的数据求平均
    '''
    city_list = list(df.columns)
    new_df = {}
    for city in city_list:
        city_df = df[[city]]
        city_mean = city_df.mean(axis=1).values
        new_df[city] = city_mean
    new_df = pandas.DataFrame(new_df, index=types())
    new_df = new_df.dropna(axis=1, how='all')
    return new_df

def output_city_day(data_dir):
    files = os.listdir(data_dir)
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        df = statistic_day(file_path)
        df = same_columns_mean(df)
        day = file_name.replace('china_sites_', '')
        df.to_csv(os.path.join('city_day', day))
        print(day)
    return 0

def get_city_province_dir():
    city_province_dir = {}
    with open('province_city.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)['provinceList']
    for province_data in raw_data:
        province_name = province_data['name']
        if len(province_data['cityList']) == 1:
            city_province_dir[get_short_name(province_name)] = get_short_name(province_name)
        else:
            cities = []
            for city in province_data['cityList']:
                city_province_dir[get_short_name(city['name'])] = get_short_name(province_name)
    city_province_dir['重庆'] = '重庆'
    city_province_dir['阿坝州'] = '四川'
    city_province_dir['甘孜州'] = '四川'
    city_province_dir['凉山州'] = '四川'
    city_province_dir['黔西南州'] = '贵州'
    city_province_dir['黔东南州'] = '贵州'
    city_province_dir['黔南州'] = '贵州'
    city_province_dir['楚雄州'] = '云南'
    city_province_dir['红河州'] = '云南'
    city_province_dir['文山州'] = '云南'
    city_province_dir['西双版纳州'] = '云南'
    city_province_dir['大理州'] = '云南'
    city_province_dir['德宏州'] = '云南'
    city_province_dir['迪庆州'] = '云南'
    city_province_dir['怒江州'] = '云南'
    city_province_dir['那曲地区'] = '西藏'
    city_province_dir['阿里地区'] = '西藏'
    city_province_dir['库尔勒'] = '新疆'
    city_province_dir['寿光'] = '山东'
    city_province_dir['章丘'] = '山东'
    city_province_dir['即墨'] = '山东'
    city_province_dir['胶南'] = '山东'
    city_province_dir['胶州'] = '山东'
    city_province_dir['莱西'] = '山东'
    city_province_dir['莱州'] = '山东'
    city_province_dir['平度'] = '山东'
    city_province_dir['蓬莱'] = '山东'
    city_province_dir['招远'] = '山东'
    city_province_dir['荣成'] = '山东'
    city_province_dir['文登'] = '山东'
    city_province_dir['乳山'] = '山东'
    city_province_dir['吴江'] = '江苏'
    city_province_dir['昆山'] = '江苏'
    city_province_dir['常熟'] = '江苏'
    city_province_dir['张家港'] = '江苏'
    city_province_dir['太仓'] = '江苏'
    city_province_dir['句容'] = '江苏'
    city_province_dir['江阴'] = '江苏'
    city_province_dir['宜兴'] = '江苏'
    city_province_dir['金坛'] = '江苏'
    city_province_dir['溧阳'] = '江苏'
    city_province_dir['海门'] = '江苏'
    city_province_dir['临安'] = '浙江'
    city_province_dir['富阳'] = '浙江'
    city_province_dir['义乌'] = '浙江'
    city_province_dir['诸暨'] = '浙江'
    city_province_dir['瓦房店'] = '辽宁'
    city_province_dir['临夏州'] = '甘肃'
    city_province_dir['甘南州'] = '西藏'
    city_province_dir['海东地区'] = '青海'
    city_province_dir['海北州'] = '青海'
    city_province_dir['黄南州'] = '青海'
    city_province_dir['海南州'] = '青海'
    city_province_dir['玉树州'] = '青海'
    city_province_dir['海西州'] = '青海'
    city_province_dir['果洛州'] = '青海'
    city_province_dir['吐鲁番地区'] = '新疆'
    city_province_dir['哈密地区'] = '新疆'
    city_province_dir['昌吉州'] = '新疆'
    city_province_dir['阿克苏地区'] = '新疆'
    city_province_dir['克州'] = '新疆'
    city_province_dir['喀什地区'] = '新疆'
    city_province_dir['和田地区'] = '新疆'
    city_province_dir['伊犁哈萨克州'] = '新疆'
    city_province_dir['塔城地区'] = '新疆'
    city_province_dir['阿勒泰地区'] = '新疆'
    city_province_dir['石河子'] = '新疆'
    city_province_dir['五家渠'] = '新疆'
    city_province_dir['博州'] = '新疆'
    city_province_dir['大兴安岭地区'] = '黑龙江'
    city_province_dir['湘西州'] = '湖南'
    city_province_dir['延边州'] = '吉林'
    city_province_dir['恩施州'] = '湖北'
    city_province_dir['铜仁地区'] = '贵州'
    city_province_dir['虢州'] = '贵州'
    city_province_dir['博州'] = '新疆'

    return city_province_dir
    
def get_short_name(longname):
    # if longname == '市辖区':
    #     longname = None
    longname = longname.replace('内蒙古自治区', '内蒙古').replace('广西壮族自治区', '广西').replace('西藏自治区', '西藏').replace('新疆维吾尔自治区', '新疆')
    longname = longname.replace('宁夏回族自治区', '宁夏').replace('市', '').replace('县', '').replace('区', '').replace('省', '')
    return longname
    
def add_province_to_list():
    city_province_dir = get_city_province_dir()
    site_data = pandas.read_csv('site_list.csv', header=0, index_col=0)
    site_data['省份'] = 0
    for index, row in site_data.iterrows():
        # print(row['城市'])
        try:
            province_name = city_province_dir[row['城市']]
        except:
            province_name = numpy.nan
        site_data.loc[index, '省份'] = province_name
    site_data.to_csv('site_province_list.csv')
    return 0


def output_province_day(data_dir):
    files = os.listdir(data_dir)
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        df = pandas.read_csv(file_path, header=0, index_col=0)
        df = df.rename(columns=get_city_province_dir())
        df = same_columns_mean(df)
        day = file_name.replace('china_sites_', '')
        df.to_csv(os.path.join('province_day', day))
        print(day)
    return 0

def static_month(data_dir):
    files = os.listdir(data_dir)           
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        df = pandas.read_csv(file_path, header=0, index_col=0)
        day = file_name.replace('china_sites_', '')
        df.to_csv(os.path.join('province_day', day))
        print(day)
    

if __name__ == "__main__":
    # === output city data ===
    # output_city_day('data')
    # === add province to site_list === 
    # add_province_to_list()
    # === output province data ===
    # output_province_day('city_day')
    # === 

