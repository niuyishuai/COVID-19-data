# coding:UTF-8
import requests,json,os,datetime,time
import xlwt,xlrd
from xlutils.copy import copy

def details():
    with open('./details/details_qq.json') as f:
        data = json.load(f)['data']
        req_data = json.loads(data)['chinaDayList']
    default = set_style('Times New Roman',220,True)

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('CountryDetails',cell_overwrite_ok=True)
    row0 = ["日期","确诊","疑似","死亡","治愈","现存确诊","现存重症","死亡率","治愈率"]
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],default)
    i = 0
    for day_data in req_data:                              
        day = day_data['date']
        date = datetime.datetime.strptime(day,'%m.%d').strftime('2020%m%d')
        confirm = day_data['confirm']
        suspect = day_data['suspect']
        dead = day_data['dead']
        heal = day_data['heal']
        nowConfirm = day_data['nowConfirm']
        nowSevere = day_data['nowSevere']
        deadRate = day_data['deadRate']
        healRate = day_data['healRate']

        sheet1.write(i+1,0,date,default)
        sheet1.write(i+1,1,confirm,default)
        sheet1.write(i+1,2,suspect,default)
        sheet1.write(i+1,3,dead,default)
        sheet1.write(i+1,4,heal,default)
        sheet1.write(i+1,5,nowConfirm,default)
        sheet1.write(i+1,6,nowSevere,default)
        sheet1.write(i+1,7,deadRate,default)
        sheet1.write(i+1,8,healRate,default)
        i = i+1
    target_path = './details/'                                 # 判断生成路径
    if os.path.exists(target_path) == False:
        os.makedirs(target_path)
    f.save(target_path+'qq全国疫情.xls')

def set_style(name,height,bold=False):                         # 定义 Excel 属性
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def update_data():                                             # 更新数据
    # print("connecting to API ...")
    # url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'                 # 下载 API 数据并保存
    # headers = {
    # 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    # }
    # y = False;z = 0
    # while y == False:
    #     try:
    #         r = requests.get(url,headers,stream = True,timeout = 1)
    #         y = True
    #     except Exception:
    #         print('10秒后重试')
    #         time.sleep(10)
    #         z += 1
    #         if z == 10:print('请求失败');exit(-1)
    # with open('./details/details_qq.json','w') as f:
    #     f.write(r.text)
    details()

update_data()
