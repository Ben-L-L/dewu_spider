import requests
import time
import re
import json
import random
import execjs
from geetest_slide3.utils import get_standard_img,get_track
from geetest_slide3.SlideCrack import SlideCrack
class Geetest(object):
    def __init__(self):
        self.img = 'https://api.geetest.com/get.php?'
        self.get_cookie = 'https://api.geetest.com/ajax.php?'
        self.check_url = 'https://api.geetest.com/ajax.php?'
        self.session = requests.session()
        self.geetest = self.geetest_demo

    def get_img(self,challenge,gt):
        params = {
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'client_type': 'android',
            'callback': 'geetest_{}'.format(int(time.time()*1000)),
        }
        self.session.get(url=self.get_cookie,params=params)
        Img_pam ={
            'is_next': 'true',
            'mobile':'true',
            'type': 'slide3',
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'https': 'true',
            'protocol': 'https://',
            'offline': 'false',
            'product': 'embed',
            'api_server': 'api.geetest.com',
            # 'isPC': 'true',
            # 'autoReset': 'true',
            'width': '100%',
            'callback': 'geetest_{}'.format(int(time.time()*1000)),
        }
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        req = self.session.get(url=self.img,params=Img_pam,headers=headers)
        results = json.loads(re.search('.*?\((.*?)\)',req.text,re.S).group(1))
        #缺口图
        quekou = 'https://static.geetest.com/' + results['bg']
        fullbg = 'https://static.geetest.com/' + results['fullbg']


        #新chanllge
        new_chanllge = results['challenge']
        #新gt
        new_gt = results['gt']
        #gct_path
        gct_path = results['gct_path']

        #轨迹需要的c
        c = results['c']

        #轨迹需要的s
        s = results['s']



        return quekou,fullbg,new_chanllge,new_gt,gct_path,c,s



    def get_params(self,quekou,fullbg,new_chanllge,new_gt,ct,c,s):
        #底图还原操作。打canvas断点能看到极验的还原算法

        standard_img = get_standard_img(self.session.get(quekou).content)
        standard_img.save('../geetest_slide3/bg.png')

        standard_img = get_standard_img(self.session.get(fullbg).content)
        standard_img.save('../geetest_slide3/fullbg.png')

        silde = SlideCrack('../geetest_slide3/bg.png', '../geetest_slide3/fullbg.png')
        #确定滑块x轴坐标
        gap_position = silde.run()

        track = get_track(offset=gap_position)

        # x轴坐标
        # offect = track[-1][0] - 1
        offect = track[-1][0]


        userresponse = self.geetest.call('U', offect, new_chanllge)

        passtime =track[-1][-1]

        imgload = random.randint(60,90)

        rq = self.geetest.call("Q",new_gt + new_chanllge[0:32] + str(passtime))

        aa = self.geetest.call('guiji_aa',self.geetest.call('guiji',track),c,s)



        #构造w参数所需要的的
        o = {
            "lang": "zh-cn",
            "userresponse": userresponse,  #x轴坐标和获取图片返回的chanllge
            "passtime": passtime, #滑动最后的时间
            "imgload": imgload,  #图片加载时间
            "aa": aa,  #轨迹相关
            "ep": {
                "v": "7.8.3",
                "te": False,
                "me": True,
                "tm": {
                    "a": 1625190276804,   #各种加载时间 好像可以伪造
                    "b": 1625190277183,
                    "c": 1625190277183,
                    "d": 0,
                    "e": 0,
                    "f": 1625190276805,
                    "g": 1625190276810,
                    "h": 1625190276828,
                    "i": 1625190276828,
                    "j": 1625190276906,
                    "k": 1625190276844,
                    "l": 1625190276906,
                    "m": 1625190277177,
                    "n": 1625190277178,
                    "o": 1625190277186,
                    "p": 1625190277367,
                    "q": 1625190277367,
                    "r": 1625190277369,
                    "s": 1625190277370,
                    "t": 1625190277370,
                    "u": 1625190277370
                },
                "td": -1
            },
            "rp": rq #获取图片返回的gt + chanllge + passtime(滑动最后的时间)
        }
        #把变动的ct更新进来
        o.update(ct)

        w = self.geetest.call('w',o)
        return w


    def check(self,new_chanllge,new_gt,w):


        params = {
            'gt': new_gt,
            'challenge': new_chanllge,
            'lang': 'zh-cn',
            'pt': '3',
            'client_type': 'web_mobile',
            'w': w,
            'callback': 'geetest_{}'.format(int(time.time())),
        }

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }

        req = self.session.get(url=self.check_url,headers=headers,params=params)
        results = json.loads(re.search('.*?\((.*?)\)',req.text,re.S).group(1))
        return results



    def get_gct(self,gct_path):
        t = {
            "lang": "zh-cn",
            "ep": {
                "v": "7.8.3",
                "te": False,
                "me": True,
                "tm": {
                    "a": 1625190276804,  # 各种加载时间 好像可以伪造
                    "b": 1625190277183,
                    "c": 1625190277183,
                    "d": 0,
                    "e": 0,
                    "f": 1625190276805,
                    "g": 1625190276810,
                    "h": 1625190276828,
                    "i": 1625190276828,
                    "j": 1625190276906,
                    "k": 1625190276844,
                    "l": 1625190276906,
                    "m": 1625190277177,
                    "n": 1625190277178,
                    "o": 1625190277186,
                    "p": 1625190277367,
                    "q": 1625190277367,
                    "r": 1625190277369,
                    "s": 1625190277370,
                    "t": 1625190277370,
                    "u": 1625190277370
                },
                "td": -1
            },
        }

        url = 'https://static.geetest.com{}'.format(gct_path)
        req = requests.get(url=url)
        data = req.text.replace('return function(t)', 'return window.get_ct=function(t)')

        js_code = f"""
        window=global;
        {data}
        function get_ct(t){{
            window.get_ct(t)
            return t

        }}
        """
        results = execjs.compile(js_code).call('get_ct', t)
        return results






    @property
    def geetest_demo(self):
        with open(r'/new_geetest.js', 'r', encoding='utf-8')as f:
            js_code = f.read()

        ctx = execjs.compile(js_code)
        return ctx



def click_slide(challenge,gt):

    gy = Geetest()
    quekou, fullbg, new_chanllge, new_gt, gct_path, c, s = gy.get_img(challenge, gt)
    # 获取gct.js中变动的值
    ct = gy.get_gct(gct_path)
    w = gy.get_params(quekou, fullbg, new_chanllge, new_gt, ct, c, s)
    # 提交验证
    results = gy.check(new_chanllge, new_gt, w)
    return results,new_chanllge



