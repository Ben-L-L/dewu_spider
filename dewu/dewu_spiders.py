# coding=utf-8
import time
from StringIO import StringIO
# from io import BytesIO
import gzip
import json
import requests
# from geetest_slide3.main import click_slide

headers = {
    'duuuid': 'dae0d85008025953',
    # 'duuuid': 'd3912f6303c7eb8a',
    'duimei': '867979020517048',
    'duplatform': 'android',
    'appId': 'duapp',
    'duchannel': 'myapp',
    'duv': '4.60.1',
    'duloginToken': '',
    'dudeviceTrait': 'Nexus+6P',
    'dudeviceBrand': 'google',
    'timestamp': '',
    'shumeiid': '20210813103822a0e8fc8fdc893d42af2eac25674db97501b14e7ccfb136ef',
    'oaid': '',
    'User-Agent': 'duapp/4.60.1(android;6.0.1)',
    'X-Auth-Token': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJkMzkxMmY2MzAzYzdlYjhhIiwic3ViIjoiZDM5MTJmNjMwM2M3ZWI4YSIsImlhdCI6MTYyOTE5OTYyOSwiZXhwIjoxNjYwNzM1NjI5LCJ1dWlkIjoiZDM5MTJmNjMwM2M3ZWI4YSIsInVzZXJJZCI6MTcwODU0MTQ4NSwidXNlck5hbWUiOiJcdTVlMDVcdTZjMTRcdTUxYjBcdTg0ZGQ2ZlgiLCJpc0d1ZXN0Ijp0cnVlfQ.lYxcYYTNFQEzBkGCHMLqq9iZ1mBSpnaoeQlzEGgwwlS5jNtl9KpLVsT4K6N6w4tf47t3gAX5EDh1zqA-_AK7uKO-ecJB3Q1HKJFZhLqZnYmo1lYVfZC2rqF-TOiIpm0dYLECs3gSIVuvlHSIXkTvZDISuohHEkxgAd-jyq0UTZvMdV7nG05quFPfErOJO-j_4ZMudg-6y_LUdlUajAdZYuDyRMosq-xlEJOsZuFLBOjSBJuSNI_jrmTYVdcqRSZH2OzJQFOAv5_Q57aEIdloj0AWfdNLvFRMk5_KxLd83fXmr98lDWtKQsstSUmgMa8f_rD9UIPEV0s1A3qcXmLdsg',
    'Content-Type': 'application/json; charset=utf-8',
    'Host': 'app.dewu.com',
    'Accept-Encoding': 'gzip',
}
"""
风控问题接口请求次数频繁之后会出现极验的滑块验证
解决滑块方法：click_validate
出现滑块之后通过切换Ip代理的方式行不通。
"""

def post_data(sign_data):
    postdata = json.dumps(sign_data)
    postf = StringIO()
    gf = gzip.GzipFile(fileobj=postf, mode='wb')
    gf.write(postdata)
    gf.close()
    postdata = postf.getvalue()

    new_sign = requests.post(url='https://18.216.112.157:24338/sign', data=postdata, verify=False)
    return new_sign




#解决滑块验证码方法
def click_validate(validate,chanllge):
    """
    :param validate:
    :param chanllge:
    :return:
    """

    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/security-anti-spider/secondVerify'

    sign_data = {
        "times": times,
        "id": "",
        "category": 'validate',
        "page": "",
        "validate": validate,
        "chanllge": chanllge,
        "make":""
    }

    new_sign = post_data(sign_data)
    headers['timestamp'] = str(json.loads(new_sign.text)['times'])
    data = {
        "challenge":chanllge,
        "loginToken":"",
        "newSign":json.loads(new_sign.text)['sign'],
        "platform":"android",
        "seccode":"{}|jordan".format(validate),
        "serverStatus":1,
        "timestamp":str(json.loads(new_sign.text)['times']),
        "uuid":"dae0d85008025953",
        "v":"4.60.1",
        "validate":validate
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response.text

# 鞋子分类接口
def get_shoe_category(category_id):
    """
    :param id:  分类id  鞋子的id是3 默认给3 就行了
    :return:
    """
    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/commodity/ice/search/doCategoryDetail'
    sign_data = {
        "times":times,
        "id":category_id,
        "category":'category',
        "page":"",
        "validate":"",
        "chanllge":"",
        "make":"",
    }
    new_sign = post_data(sign_data)
    headers['timestamp'] = str(json.loads(new_sign.text)['times'])
    data = {
        "catId":category_id,
        "loginToken": "",
        "newSign": json.loads(new_sign.text)['sign'],
        "platform": "android",
        "timestamp": str(json.loads(new_sign.text)['times']),
        "uuid": "dae0d85008025953",
        "v": "4.60.1"
    }

    req = requests.post(url=url,headers=headers,json=data)

    return req.text


#通过鞋子分类下面每个品牌的id获取不同鞋子的列表页
def get_shoe_list(unionId,page,make):
    """
    :param unionId:  先判断 if  seriesList['redirect']没有['val']的时候make==0,unionId给brandId  page 第一页给 '' 第二页给10  第三页20 以此类推
                    elif seriesList['redirect']有['val'] 并且 and recommendId in seriesList['redirect']['val'] make == 1
                    page 第一页给 '' 第二页给2  第三页给3


                    else make == 2     unionId 给seriesList['redirect']['val']   page 第一页给0，第二页给1，第三页给2 以此类推


    :param page:  第一页为 0 第二页为1 第三页为2  以此类推
    param make
    :return:
    """
    times = int(time.time() * 1000)
    if make ==0:
        url = 'https://app.dewu.com/api/v1/app/search/ice/commodity/detail_brand'

        sign_data = {
            "times": times,
            "id": unionId,
            "category": 'list',
            "page": page,
            "validate": "",
            "chanllge": "",
            "make":make
        }
        new_sign = post_data(sign_data)
        headers['timestamp'] = str(json.loads(new_sign.text)['times'])
        headers['duuuid'] = 'd3912f6303c7eb8a'

        data = {"aggregation": False,
                "brandId": unionId,
                "categoryIds": [],
                "categoryLevel1": "29",
                "debugAgg": True,
                "fitIds": [],
                "lastId": page,
                "limit": 20,
                "loginToken": "",
                "newSign": json.loads(new_sign.text)['sign'],
                "platform": "android",
                "price": [],
                "property": [],
                "sortMode": 1,
                "sortType": 0,
                "timestamp": str(json.loads(new_sign.text)['times']),
                "uuid": "d3912f6303c7eb8a",
                "v": "4.60.1"
                }
        req = requests.post(url=url, headers=headers, json=data)
        return req.text


    elif make == 1:

        sign_data = {
            "times": times,
            "id": unionId,
            "category": 'list',
            "page": page,
            "validate": "",
            "chanllge": "",
            "make": make
        }

        new_sign = post_data(sign_data)

        headers['timestamp'] = str(json.loads(new_sign.text)['times'])
        headers['duuuid'] = 'd3912f6303c7eb8a'

        url = 'https://app.dewu.com/api/v1/app/commodity/ice/boutique-recommend/detail'

        data = {
            "aggregation": {"aggregation": False, "brandId": "", "categoryId": "", "fitId": "", "highestPrice": "0",
                            "lowestPrice": "0", "property": "", "seriesId": "", "sortMode": 1, "sortType": 0},
            "lastId": page,
            "lastSpuId": 0,
            "loginToken": "",
            "newSign": json.loads(new_sign.text)['sign'],
            "platform": "android",
            "realPageNum": 0,
            "recommendId": unionId,
            "spuIds": [],
            "timestamp": str(json.loads(new_sign.text)['times']),
            "uuid": "d3912f6303c7eb8a",
            "v": "4.60.1"
        }

        req = requests.post(url=url, headers=headers, json=data)
        return req.text



    elif make == 2:
        sign_data = {
            "times": times,
            "id": unionId,
            "category": 'list',
            "page": page,
            "validate": "",
            "chanllge": "",
            "make":make
        }
        new_sign = post_data(sign_data)
        url = 'https://app.dewu.com/api/v1/app/search/ice/search/list?hideAddProduct=0&title=&unionId={}&sortMode=0&typeId=0&' \
              'sortType=0&catId=11&showHot=1&page={}&limit=20&originSearch=false&newSign={}'.format(unionId, page,
                                                                                                    json.loads(new_sign.text)['sign'])
        headers['timestamp'] = str(json.loads(new_sign.text)['times'])
        headers.pop('Content-Type')
        req = requests.get(url=url, headers=headers)
        return req.text





#通过鞋子列表页的spuid获取到鞋子的详情页
def get_shoe_detial(spuid):
    """


    :param spuid:  通过列表页的spuid 获取详情信息 get_shoe_list返回的spuid
    :return:
    """
    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/index/ice/flow/product/detail'

    sign_data = {
        "times": times,
        "id": spuid,
        "category": 'detial',
        "page": "",
        "validate": "",
        "chanllge": "",
        "make":""
    }
    new_sign = post_data(sign_data)
    headers['timestamp'] = str(json.loads(new_sign.text)['times'])
    headers['duuuid'] = 'd3912f6303c7eb8a'
    data = {
        "arFileSwitch": True,
        "groupFirstId": spuid,
        "loginToken": "",
        "newSign": json.loads(new_sign.text)['sign'],
        "platform": "android",
        "productSourceName": "classification",
        "propertyValueId": 0,
        "skuId": 0,
        "spuId": spuid,
        "timestamp": str(json.loads(new_sign.text)['times']),
        "uuid": "d3912f6303c7eb8a",
        "v": "4.60.1"
    }

    response = requests.post(url=url, headers=headers, json=data)
    return response.text


# #通过列表页的spuid获取详情页下面的全部购买记录
def get_shoe_buy_history(spuid,page):

    """
    :param spuid:  列表页获取到的spuid
    :param page:  一页返回100条     页码 第一页 ''  第二页要获取到接口的lastId  page就是 lastId
    :return:
    """

    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/commodity/ice/last-sold-list'

    sign_data = {
        "times": times,
        "id": spuid,
        "category": 'history',
        "page": page,
        "validate": "",
        "chanllge": "",
        "make":""
    }

    new_sign = post_data(sign_data)
    headers['timestamp'] = str(json.loads(new_sign.text)['times'])
    data = {
        "lastId": page,
        "limit":100,
        "loginToken": "",
        "newSign": json.loads(new_sign.text)['sign'],
        "platform": "android",
        "spuId":spuid,
        "timestamp": str(json.loads(new_sign.text)['times']),
        "uuid": "dae0d85008025953",
        "v": "4.60.1"
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response.text







#通过列表页获取spuid
def get_shoe_buy_price(spuid):
    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/inventory/price/sell/queryBuyNowInfo'

    sign_data = {
        "times": times,
        "id": spuid,
        "category": 'price',
        "page": "",
        "validate": "",
        "chanllge": "",
        "make":"",
    }

    new_sign = post_data(sign_data)
    headers['timestamp'] = str(json.loads(new_sign.text)['times'])
    headers['duuuid'] = 'd3912f6303c7eb8a'

    data = {
        "loginToken": "",
        "newSign": json.loads(new_sign.text)['sign'],
        "platform": "android",
        "spuId": spuid,
        "timestamp": str(json.loads(new_sign.text)['times']),
        "uuid": "d3912f6303c7eb8a",
        "v": "4.60.1"
    }

    response = requests.post(url=url, headers=headers, json=data)
    return response.text




"""
gt = response.json()['data']['gt']
challenge = response.json()['data']['challenge']

results, new_chanllge = click_slide(challenge=challenge, gt=gt)
validate = results['validate']
click_validate(validate, new_chanllge)



"""





#如果遇到了验证码处理的例子
"""
if response.status_code !=200:
    print('解决极验滑块验证码中----------')
    try:
        gt = response.json()['data']['gt']
        challenge = response.json()['data']['challenge']
        
        results,new_chanllge = click_slide(challenge=challenge,gt=gt)
    
        if results.get('validate',''):
            validate = results['validate']
            msg,status = click_validate(validate,new_chanllge)
            print(msg,status)
            if msg=='ok' and status == 200:
                print('滑块解决完成继续抓取----------')
                continue
    
    
        else:
            print('滑块识别失败正在重试------')
            continue
    
    except Exception as err:
        print(err)
        continue
    
    
    
    results = response.json()['data']
    lastId = results.get('lastId','')
    page = lastId
    print(page)
    for i in results['list']:
    userName = i['userName']
    print(userName)
    formatTime = i['formatTime']
    print(formatTime)






"""










