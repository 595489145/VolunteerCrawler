import requests
import csv
import json

def getSchoolList(page):
    # 请求api
    url = ("https://api.zjzw.cn/web/api/?keyword=&page=7&province_id=&ranktype=&request_type=1&size=20&top_school_id=[120,3703,227,1400,3117,1398,1724,597,602,721]&type=&uri=apidata/api/gkv3/school/lists&signsafe=4f2c6c77a052acdee5fa718fe75f05ef").format(1)
    headers = {
        'Cookie': 'acw_tc=ac11000117194685500844446eda0037d2d3da341d1fe6f1d4f6bb7a6f0599; aliyungf_tc=a98cf5d5ec0af14f61e48a45c811a15c1c74d960de004ec30841a31f71ddc186; JSESSIONID=1140A10EAAAD9DDC0BFFF0E08FE62FDE',
        'Content-Length': '0',
        'Host': 'api.zjzw.cn',
        'User-Agent': 'PostmanRuntime/7.39.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # 返回请求体
    r = requests.post(url=url, headers=headers)
    print(r.text)
    data = json.loads(r.text)
    if not data['data']:
        print("查询不到此页的学校信息")
        return
    for schoolInfo in data['data']['item']:  # ['numFound']总条数
        print(schoolInfo)

        # 提取学校id，get请求使用
        school_id = schoolInfo['school_id']
        # 提取学校名称
        high_title = schoolInfo['hightitle']
        # 提取学校是否公办或者民办
        nature_name = schoolInfo['nature_name']
        # 提取学校地址
        address = schoolInfo['province_name'] + "省" + schoolInfo['city_name'] + schoolInfo['county_name']
        # 提取学校是否是985，211，双一流
        ifDual = (schoolInfo['province_name'] == "")
        if985= (schoolInfo['f985'] == "1")
        if211 = (schoolInfo['f211'] == "1")


        # 进入学校主页
        pass

if __name__ == '__main__':
    getSchoolList(1)

