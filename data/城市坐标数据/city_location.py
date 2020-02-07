import json
import xlrd
import xlwt
import numpy as np
from urllib.request import urlopen, quote

# 保存数据到excel工作簿
def save(data, path='city_coordinate.xls'):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = data.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])

    f.save(path)

# 提取城市坐标
def extract_city_coordinates(citylstfile='data_city.xlsx', ak='lxuvSE7TmLRquQPMmzhLsrEMjeOdy5CD '):
    data = xlrd.open_workbook(citylstfile)
    Sheet1 = data.sheet_by_name('Sheet1')
    citys = Sheet1.col_values(1)
    del citys[0]  # 删除lst
    print(citys)
    
    lst = ['城市', '经度', '纬度']
    
    # API规则范例
    # http://api.map.baidu.com/geocoder?address=地址&output=输出格式类型&key=用户密钥&city=城市名
    # http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation //GET请求
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    
    for i in citys:
        # 生成API URL
        add = quote(i)
        url += '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API
        
        # 读取json数据
        req = urlopen(url)
        res = req.read().decode()
        temp = json.loads(res)
        
        print(i, temp['result']['location']['lng'],temp['result']['location']['lat'])  # 经纬度
          
        # 经纬度
        coordinate = i, temp['result']['location']['lng'], temp['result']['location']['lat']
        coordinate = np.array(coordinate)
        lst = np.row_stack((lst, coordinate))
    return lst


# 主函数
def main():
    lst = extract_city_coordinates('city_lst.xlsx', 'lxuvSE7TmLRquQPMmzhLsrEMjeOdy5CD ')
    print(lst)
    save(lst, 'city_coordinate.xls')

# 执行
main()