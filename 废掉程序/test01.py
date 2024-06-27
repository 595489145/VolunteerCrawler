import requests
import csv
import json

# 代理
proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'https://127.0.0.1:7890'
}


# 请求高校列表api
def getSchoolList(page=1, ifUseProxy=False):
    # 请求api
    url = ("https://api.zjzw.cn/web/api/?keyword=&page=5&province_id=&ranktype=&request_type=1&size=20&top_school_id=[120,3703,227,1400,3117,1398,1724,597,602,721]&type=&uri=apidata/api/gkv3/school/lists&signsafe=4f2c6c77a052acdee5fa718fe75f05ef").format(page)
    # 请求头
    '''
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '240',
        'Content-Type': 'application/json',
        'Host': 'api.zjzw.cn',
        'Origin': 'https://www.gaokao.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.gaokao.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="109", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    '''



    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Access-Control-Request-Headers': 'content-type',
        'Access-Control-Request-Method': 'POST',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'api.zjzw.cn',
        'Origin': 'https://www.gaokao.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.gaokao.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    # 返回请求体
    if ifUseProxy:
        r = requests.post(url=url, headers=headers, proxies=proxy)
    else:
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
    getSchoolList(6)
