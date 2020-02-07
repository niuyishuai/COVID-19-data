import requests
import json
import xlwt
import datetime
import os

#%%
def migration(level='city',type='move_out',date='20200101'):
    # 执行 API 调用并储存响应
    url = 'http://huiyan.baidu.com/migration/'+level+'rank.jsonp?dt=country&id=0&type='+type+'&date='+date+'&callback=jsonp_1580737583074_8938529'
    r = requests.get(url)

    # 转化为 json 数据
    req_data = extract_json_data(r)
    # 保存为 json 文件
    # filename = 'wuhan.json'
    # with open(filename,'w')as f:
    #     f.write(sub_str)

    # 写入 Excel
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(type,cell_overwrite_ok=True)
    if level == 'city':
        row0 = ["城市","省份","比例"]
    else:
        row0 = ["  ","省份","比例"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

    i = 0
    for req_dict in req_data['data']['list']:
        if level == 'city':
            city_name = req_dict['city_name']
            sheet1.write(i+1,0,city_name,set_style('Times New Roman',220,True))
        province_name = req_dict['province_name']
        value = req_dict['value']
        sheet1.write(i+1,1,province_name,set_style('Times New Roman',220,True))
        sheet1.write(i+1,2,value,set_style('Times New Roman',220,True))
        i = i+1
    # 判断并生成路径
    target_path = './migration/'+level+'/'+type+'/'
    if os.path.exists(target_path)==False:
        os.makedirs(target_path)
    f.save(target_path + date + '.xls')

#%% 定义 Excel 属性
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

#%% extract json data
def extract_json_data(r):
    start1 = '('
    end1 = ')'
    s = r.text.find(start1)
    e = r.text.find(end1)
    sub_str = r.text[s+1:e]
    return json.loads(sub_str)

#%% download migration data
def download_data():
    dateend = datetime.datetime.now()
    datestart = datetime.datetime.strptime('20200101','%Y%m%d')
    while datestart < dateend:
        for level in ['city','province']:
            for type in ['move_in','move_out']:
                date = datestart.strftime('%Y%m%d')
                migration(level,type,date)
        datestart+= datetime.timedelta(days=+1)

download_data()