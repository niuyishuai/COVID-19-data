import requests
import json
import xlwt

def details(level0='province'):
    # 执行 API 调用并储存响应
    url = 'http://ncov.nosensor.com:8080/api/'
    r = requests.get(url)

    # req_data = r.json()
    # 保存为 json 文件
    filename = 'wuhan.json'
    with open(filename,'w')as f:
        f.write(r.text)

    with open ('wuhan.json') as f:
        req_data = json.load(f)
        # 写入 Excel
    for req_dic in req_data[level0]:
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(level0+'Details',cell_overwrite_ok=True)
        if level0 == 'city':
            row0 = ["城市","省份","确诊","死亡","治愈","疑似"]
            level = 'City'
        else:
            row0 = ["  ","省份","确诊","死亡","治愈","疑似"]
            level = 'Province'
        #写第一行
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

        date = req_dic['Time']
        i = 0
        for req_dict in req_dic[level+'Detail']:
            if level == 'City':
                city_name = req_dict['City']
                sheet1.write(i+1,0,city_name,set_style('Times New Roman',220,True))
            province_name = req_dict['Province']
            confirmed = req_dict['Confirmed']
            dead = req_dict['Dead']
            cured = req_dict['Cured']
            if 'Obse' in req_dict:
                obse = req_dict['Obse']
                sheet1.write(i+1,5,obse,set_style('Times New Roman',220,True))
            sheet1.write(i+1,1,province_name,set_style('Times New Roman',220,True))
            sheet1.write(i+1,2,confirmed,set_style('Times New Roman',220,True))
            sheet1.write(i+1,3,dead,set_style('Times New Roman',220,True))
            sheet1.write(i+1,4,cured,set_style('Times New Roman',220,True))
            i = i+1
        name = './details/'+level+'/'+date+'.xls'
        f.save(name)

# 定义 Excel 属性
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

for level in ['city','province']:
    details(level)