# coding=utf-8
import time
from io import StringIO
import gzip
import json
# from dewu.dewu_frida import dw
import requests
# from geetest_slide3.main import click_slide
headers = {
    'duuuid': 'd3912f6303c7eb8a',
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
    'X-Auth-Token': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJkMzkxMmY2MzAzYzdlYjhhIiwic3ViIjoiZDM5MTJmNjMwM2M3ZWI4YSIsImlhdCI6MTYyOTE2NjU3MiwiZXhwIjoxNjYwNzAyNTcyLCJ1dWlkIjoiZDM5MTJmNjMwM2M3ZWI4YSIsInVzZXJJZCI6MTcwODU0MTQ4NSwidXNlck5hbWUiOiJcdTVlMDVcdTZjMTRcdTUxYjBcdTg0ZGQ2ZlgiLCJpc0d1ZXN0Ijp0cnVlfQ.UyavvJNs9oWyb_Wm7EGDlqxoSIiAa42r0L7LSuwexMjZ2qCBJMG19ujb_JJKymc2uhwHD5yMqRqguBpmqYgwN2KQifaglNxI5aY195TiEH809mpljL0zBUqpZHVYppAVTg4UrPxhjcJx9A4LMIvChXdx6kdqUHyDsaqzGx0bNs-4s5ZA24Ix0mseelZl4uQkzemZVTGhu-5imoR0TwU_lEsDnD_mWKjrmIJSLe5P8O-1oubOWoMWos8MJF_B16UVbyTnWCWkDp0LKlIBhRfZF6-uvYxcnhm72H53BKsCMfs_a8HoWUpR-YiFw1GcFOaMGzobHZMvEhvta-EfDfCh-A',
    'Content-Type': 'application/json; charset=utf-8',
    'Host': 'app.dewu.com',
    'Accept-Encoding': 'gzip',
}

# script = dw.get_script()

"""
风控问题接口请求次数频繁之后会出现极验的滑块验证
解决滑块方法：click_validate
出现滑块之后通过切换Ip代理的方式行不通。
"""






#解决滑块验证码方法
# def click_validate(validate,chanllge):
#     """
#     :param validate:   如果滑块成功会返回 validate
#     :param chanllge:    这个就是每个滑块的标识
#     :return:  msg = ok   stutas = 200 代表过了滑块
#     """
#
#     times = int(time.time() * 1000)
#     url = 'https://app.dewu.com/api/v1/app/security-anti-spider/secondVerify'
#     script = dw.get_script()
#     new_sign = script.exports.getnewsign(times, '',click_validate.__name__.split('_')[-1],'',
#                                          validate,chanllge)
#     headers['timestamp'] = str(new_sign['times'])
#
#     data = {
#         "challenge":chanllge,
#         "loginToken":"",
#         "newSign":new_sign['sign'],
#         "platform":"android",
#         "seccode":"{}|jordan".format(validate),
#         "serverStatus":1,
#         "timestamp":str(new_sign['times']),
#         "uuid":"d3912f6303c7eb8a",
#         "v":"4.60.1",
#         "validate":validate
#     }
#
#     response = requests.post(url=url, headers=headers, json=data)
#     results = response.json()
#     msg = results['msg']
#     status = results['status']
#
#     return msg,status







# 鞋子分类接口
def get_shoe_category(category_id):
    """
    :param id:  分类id  鞋子的id是3 默认给3 就行了
    :return:
    """
    times = int(time.time() * 1000)
    url = 'https://app.dewu.com/api/v1/app/commodity/ice/search/doCategoryDetail'
    #获取frida script  这个要在代码初始化的时候写
    # script = dw.get_script()

    sign_data = {
        "times":times,
        "id":category_id,
        "category":get_shoe_category.__name__.split('_')[-1],
        "page":"",
        "validate":"",
        "chanllge":""
    }
    postdata = json.dumps(sign_data)
    postf = StringIO()
    gf = gzip.GzipFile(fileobj=postf,mode='wb')
    gf.write(postdata)
    gf.close()
    postdata = postf.getvalue()

    new_sign = requests.post(url='https://18.216.112.157:24338/sign',data=postdata,verify=False)
    print new_sign

    headers['timestamp'] = str(new_sign['times'])
    data = {
        "catId":"3",
        "loginToken": "",
        "newSign": new_sign['sign'],
        "platform": "android",
        "timestamp": str(new_sign['times']),
        "uuid": "d3912f6303c7eb8a",
        "v": "4.60.1"
    }

    req = requests.post(url=url,headers=headers,json=data)
    return req.text

# get_shoe_category(3)


#通过鞋子分类下面每个品牌的id获取不同鞋子的列表页
# def get_shoe_list(shoe_id,page):
#     """
#     :param shoe_id:  鞋子类别id 就是 get_shoe_category 返回的 brandId
#     :param page:  页数 第1页为 ''   第二页为10  第三页20  以此类推
#     :return:
#     """
#
#     times = int(time.time() * 1000)
#     url = 'https://app.dewu.com/api/v1/app/search/ice/commodity/detail_brand'
#
#     script = dw.get_script()
#
#     new_sign = script.exports.getnewsign(times, shoe_id, get_shoe_list.__name__.split('_')[-1],page)
#
#     headers['timestamp'] = str(new_sign['times'])
#     data = {"aggregation":False,
#             "brandId":shoe_id,
#             "categoryIds":[],
#             "categoryLevel1":"29",
#             "debugAgg":True,
#             "fitIds":[],
#             "lastId":page,
#             "limit":20,
#             "loginToken":"",
#             "newSign":new_sign['sign'],
#             "platform":"android",
#             "price":[],
#             "property":[],
#             "sortMode":1,
#             "sortType":0,
#             "timestamp":str(new_sign['times']),
#             "uuid":"d3912f6303c7eb8a",
#             "v":"4.60.1"
#             }
#     #
#     req = requests.post(url=url, headers=headers, json=data)
#     return req.text
#
#
#
# #通过鞋子列表页的spuid获取到鞋子的详情页
# def get_shoe_detial(spuid):
#     """
#
#
#     :param spuid:  通过列表页的spuid 获取详情信息 get_shoe_list返回的spuid
#     :return:
#     """
#     times = int(time.time() * 1000)
#     url = 'https://app.dewu.com/api/v1/app/index/ice/flow/product/detail'
#     script = dw.get_script()
#     new_sign = script.exports.getnewsign(times, spuid, get_shoe_detial.__name__.split('_')[-1])
#     headers['timestamp'] = str(new_sign['times'])
#     data = {
#         "arFileSwitch":True,
#         "groupFirstId":spuid,
#         "loginToken": "",
#         "newSign": new_sign['sign'],
#         "platform": "android",
#         "productSourceName":"",
#         "propertyValueId":0,
#         "skuId":0,
#         "spuId": spuid,
#         "timestamp": str(new_sign['times']),
#         "uuid": "d3912f6303c7eb8a",
#         "v": "4.60.1"
#     }
#
#     response = requests.post(url=url,headers=headers,json=data)
#     return response.text
#
#
# #通过列表页的spuid获取详情页下面的全部购买记录
# def get_shoe_buy_history(spuid):
#
#     """
#     :param spuid:  列表页获取到的spuid
#     :param page:  一页返回100条     页码 第一页 ''  第二页要获取到接口的lastId
#     :return:
#     """
#     page = ''
#     while True:
#         times = int(time.time() * 1000)
#         url = 'https://app.dewu.com/api/v1/app/commodity/ice/last-sold-list'
#
#         new_sign = script.exports.getnewsign(times, spuid, get_shoe_buy_history.__name__.split('_')[-1],page)
#         headers['timestamp'] = str(new_sign['times'])
#         data = {
#             "lastId": page,
#             "limit":100,
#             "loginToken": "",
#             "newSign": new_sign['sign'],
#             "platform": "android",
#             "spuId":spuid,
#             "timestamp": str(new_sign['times']),
#             "uuid": "d3912f6303c7eb8a",
#             "v": "4.60.1"
#         }
#         response = requests.post(url=url, headers=headers, json=data)
#
#
#         return response.text



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










