import requests
import json


class WoZaiXiaoYuanPuncher:
    def __init__(self, item):
        self.data = item
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; vivo X21A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4365 MMWEBSDK/20221012 Mobile '
                          'Safari/537.36 MMWEBID/9027 MicroMessenger/8.0.30.2260(0x28001E95) WeChat/arm64 Weixin '
                          'NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxce6d08f781975d91',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        self.cookies = {
            'JWSESSION': item['cookies']
        }
        self.session = requests.session()
        self.status_code = -1

    def login(self):
        url = 'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username'
        params = {
            'username': self.data['username'],
            'password': self.data['password'],
            'openId': 'o0-5d1jAWziY50H3mwgP4aycekdk',
            'unionId': 'oUXUs1Wt1SCup3vp3na13tnMLV0E',
            'wxworkOpenId': '',
            'wxworkUserId': '',
            'wxworkCorpId': '',
            'phoneInfo': '3____linux; android 10; bah3-w59 build/huaweibah3-w59; wv',
        }
        response = self.session.get(url=url, params=params, headers=self.headers)
        res = json.loads(response.text)
        if res['code'] == 0:
            jwsession = response.headers['JWSESSION']
            self.setJwsession(jwsession)
            return True
        else:
            self.status_code = 3
            return False

    def setJwsession(self, jwsession):
        self.cookies['JWSESSION'] = jwsession

    def getJwsession(self):
        return self.cookies['JWSESSION']

    def testLoginStatus(self):
        url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/home/getHomeApps?env=3"
        response = self.session.get(url=url, headers=self.headers, cookies=self.cookies)
        res = json.loads(response.text)
        # print(res)
        if res['code'] == 0:
            return 1
        elif res['code'] == 103:
            self.status_code = 3
            return 0
        else:
            self.status_code = 0
            return -1

    def PunchIn(self):
        url = "https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch"
        response = self.session.post(url=url, headers=self.headers, cookies=self.cookies)
        res = json.loads(response.text)
        if res['code'] == 0:
            for i in res['data']['list']:
                if int(i['state']) == 1 and int(i['type']) == 0:
                    self.doPunchIn(str(i['id']))
                    break
                else:
                    self.status_code = 2
        elif res['code'] == 103:
            self.status_code = 3
        else:
            self.status_code = 0

    def doPunchIn(self, ID):
        url = "https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch=" + ID
        headers = {
            'Host': 'gw.wozaixiaoyuan.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'JWSESSION': self.cookies['JWSESSION'],
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SCMR-W09 Build/HUAWEISCMR-W09; wv) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4343 MMWEBSDK/20221012 Mobile '
                          'Safari/537.36 MMWEBID/8277 MicroMessenger/8.0.30.2260(0x28001E55) WeChat/arm64 Weixin '
                          'Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxce6d08f781975d91',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://gw.wozaixiaoyuan.com',
            'X-Requested-With': 'com.tencent.mm',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://gw.wozaixiaoyuan.com/h5/mobile/health/0.3.7/health/detail?id=' + ID,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'JWSESSION=' + self.cookies['JWSESSION'] + '; ' + 'JWSESSION=' + self.cookies['JWSESSION']
        }
        sign_data = {
            "t1": self.data['data_list']['t1'],
            "t2": self.data['data_list']['t2'],
            "t3": self.data['data_list']['t3'],
            "type": 0,
            "locationMode": 0,
            "location": self.data['data_list']['location'],
            "locationType": 0
        }
        data = json.dumps(sign_data)
        response = self.session.post(url=url, data=data, headers=headers)
        res = json.loads(response.text)
        if res["code"] == 0:
            self.status_code = 1
        else:
            self.status_code = 0

    def sendNotification(self):
        notify_result = self.getResult()
        url = 'http://www.pushplus.plus/send'
        token = self.data['push_plus_token']
        title = "⏰ 我在校园打卡结果通知"
        content = "#### 打卡情况:\n" + notify_result
        msg = {
            "token": token,
            "title": title,
            "content": content,
            "template": "markdown"
        }
        requests.post(url, data=msg)

    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 2:
            return "❌ 打卡失败, 已打卡/不在打卡时间"
        elif res == 3:
            return "❌ 打卡失败，未登录,请重新登录"
        else:
            return "❌ 打卡失败，发生未知错误"
