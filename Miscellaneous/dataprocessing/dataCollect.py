# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:25:12 2017

@author: wangfuyun
"""

import requests,json
from openpyxl import Workbook

#http header
headers={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Content-Length':'25',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':'PHPSESSID=f1v64unhrnrbk71a8r6odn4jt8; _gac_UA-80921812-1=1.1695627710.CjwKCAjw38SoBhB6EiwA8EQVLhxkqwDqpfzV-spxgH4c7xGjfPqD6BjkC02BtvYu00EFq4S22nKgFRoCrhYQAvD_BwE; _gcl_aw=GCL.1695627711.CjwKCAjw38SoBhB6EiwA8EQVLhxkqwDqpfzV-spxgH4c7xGjfPqD6BjkC02BtvYu00EFq4S22nKgFRoCrhYQAvD_BwE; _gcl_au=1.1.1211203322.1695627711; _fbp=fb.2.1695627711597.2139030901; _gid=GA1.3.1247803474.1695865739; PrestaShop-7e6caca2bb0a3a8ea43e8d35cc88a8f2=def502003a344bd7e9cbe6daafd87a0a16baf1ba366039f29d9a99b07a892b0a2de06e5bfe9cca6a754c65711b7b6d11a32d56f93f3615f87bf8a0b6b1928578a7ccd657273ebb2774d53b8e4f91f886145b0e9ff850d58234ee4f9e5cf1941665444673da690bf8fcc4278dab733f4534d3e710709c44a9bdcd16b88c377f7af9b5c5878fb41c0be892b525059c2760d689352ec8450e4837fb49f5ef4e769ab2e480fd8de83843b5c5774cf1ce0c2d38506f6928ad5cd97a28f7dc39a0b2b4254283649f882997f4caf67ecd2aeab612c7ed57ad51999cddfead5bec165841633e93992cfc0911516080f11f6193683735a33129d347f6ab91f7637d56a9491955c02e1cc935dab181ce065df8a062a432c74e309a412ee5e15c9ae03e013921dc3afe58712c9397a014fd6bdc7c0abe3c1888f01d3e462c7aed04b3b3fbbe63d1b133378932fea639; _gat=1; _ga_K29XXK3BXZ=GS1.1.1695963686.10.1.1695966205.59.0.0; _ga=GA1.1.149016773.1695627710; _ga_MEFV9V5VEK=GS1.1.1695963686.10.1.1695966205.0.0.0'
'Host':'www.candy.com.sg',
'Origin':'https://www.candy.com.sg',
'Referer':'https://www.candy.com.sg/493-indoor',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
'X-Anit-Forge-Code':'0',
'X-Anit-Forge-Token':'None',
'X-Requested-With':'XMLHttpRequest'
}

 
def get_json(url, page):
    data = {'first': "true", 'pn': page}

#POST request
    json = requests.post(url,data,headers=headers).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i['plantname'])
        info.append(i['price'])
        info.append(i['url'])
        info.append(i['picture'])
        info.append(i['picture1'])

        info.append(i['alias'])
        info.append(i['content'])
        info.append(i['total'])
        info.append(i['3 payment'])

        info_list.append(info)
    return info_list
 

def main():
    page = 1
    url = 'https://www.candy.com.sg/493-indoor'
    info_result=[]  
    title = ['plantname','price','url','picture','picture1','alias','content',"total", "3 payment"]
    info_result.append(title)  

#iteration
    while page < 16:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        page += 1
# write csv file
        wb = Workbook()
        ws1 = wb.active
        ws1.title = lang_name
        for row in info_result:
            ws1.append(row)
        str = page + '.csv'
        wb.save(str)
       
main()