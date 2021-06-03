import requests
import time

wx_push_access_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wwb29d27fb30b4b334&corpsecret=mN8N_E8wQxhermZvdfpvKs83JGhvk5oDobArJEbZ0Lg'
try:
    wx_push_token = requests.post(wx_push_access_url, data="").json()['access_token']
    print(wx_push_token)
except:
    print('error')
time.sleep(1)
wx_push_data = {
    "agentid": "1000002",
    "msgtype": "text",
    "touser": "@all",
    "text": {
        "content": "*********疫苗可预约提醒*********\n" +
                   "区域：" +
                   "社康名称：" +
                   "疫苗厂商：" +
                   "可打日期：" +
                   "可打时间：" +
                   "社康地址：" +
                   "立即预约："
    },
    "safe": 0
}

wx_push = requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(wx_push_token),
                    json=wx_push_data)
print(wx_push.json())
print(wx_push.json()["errmsg"]=='ok')
# 成功：{'errcode': 0, 'errmsg': 'ok', 'invaliduser': ''}
# 失败：{'errcode': 40056, 'errmsg': 'invalid agentid, hint: [1622686176_210_34d8bba0f4b4a2b5ccb08c1e1bac8fb2], from ip: 116.236.97.154, more info at https://open.work.weixin.qq.com/devtool/query?e=40056'}
