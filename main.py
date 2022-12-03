from WoZaiXiaoYuanPuncher import WoZaiXiaoYuanPuncher
from jsonHandler import JsonReader

JSON_FILE = "./config/source.json"


if __name__ == '__main__':
    obj = JsonReader(JSON_FILE)
    src_info = obj.getJson()
    for item in src_info:
        wzxy = WoZaiXiaoYuanPuncher(item)
        # wzxy.testLoginStatus()
        login_state = wzxy.testLoginStatus()
        if login_state == 1:
            wzxy.PunchIn()
        elif login_state != 1 and wzxy.login():
            item['cookies'] = wzxy.cookies['JWSESSION']
            obj.writejson(src_info)
            wzxy.PunchIn()
        # print(wzxy.getResult())
        wzxy.sendNotification()
