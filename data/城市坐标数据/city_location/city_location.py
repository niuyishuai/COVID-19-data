import json

import xlrd

import xlwt

import numpy as np

from urllib.request import urlopen, quote


def save(data1, path):

    f = xlwt.Workbook()  # 创建工作簿

    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    [h, l] = data1.shape  # h为行数，l为列数

    for i in range(h):

        for j in range(l):

            sheet1.write(i, j, data1[i, j])

    f.save(path)

#http://api.map.baidu.com/geocoder?address=地址&output=输出格式类型&key=用户密钥&city=城市名
#http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation //GET请求
url = 'http://api.map.baidu.com/geocoding/v3/'

output = 'json'

ak = 'lxuvSE7TmLRquQPMmzhLsrEMjeOdy5CD '

data = xlrd.open_workbook('E:\研究生文件\武汉2019ncov\data_city.xlsx')

data.sheet_names()

#print("sheets：" + str(data.sheet_names()))

table = data.sheet_by_name('Sheet1')

#print(table)
Sheet1 = data.sheet_by_index(0)

city_col = Sheet1.col_values(1)

del city_col[0]

#del city_col[49]

print(city_col)

coordinate1 = ['city','经度','纬度']

a = ['北京', '天津', '石家庄', '太原', '呼和浩特', '沈阳', '大连', '长春', '哈尔滨', '上海', '南京', '杭州', '宁波', '合肥', '福州', '厦门', '南昌', '济南',
     '青岛', '郑州', '武汉', '长沙', '广州', '深圳', '南宁', '海口', '重庆', '成都', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐']
for i in city_col:

    add = quote(i)

    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API

    req = urlopen(uri)

    res = req.read().decode()

    temp = json.loads(res)

    print( i,temp['result']['location']['lng'],temp['result']['location']['lat'] ) # 经纬度

    coordinate = i, temp['result']['location']['lng'], temp['result']['location']['lat']  # 经纬度

    coordinate = np.array(coordinate)

    coordinate1 = np.row_stack((coordinate1, coordinate))

print(coordinate1.shape)

print(coordinate1)

save(coordinate1, 'city_coordinate.xls')

    #coordinate = np.array(coordinate)

    #coordinate1 = np.row_stack((coordinate1, coordinate))

#explain = np.row_stack(('city',a))

#coordinate1 = np.column_stack((a, coordinate1))

#print(coordinate1.shape)

#print(coordinate)

#save(coordinate1, 'city_coordinate.xls')

