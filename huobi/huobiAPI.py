import requests
import time



# 火币API请求历史k线数据的基本url
base_url = "https://api.hadax.com/market/history/trade?symbol=dogeusdt&size=2"


# 请求函数 参数：（数字火币币种，计价稳定比币种）
def get_price(url):
    while True:
        try:
            r = requests.get(url, timeout=30)
            # print(r.json())
            break
        except:
            print("数据请求超时，10s后再次尝试")
            time.sleep(10)
    datas = r.json()  # 将字符串序列转换为json

    datas = datas["data"]  # 获取数据列表
    # print(datas)
    for data in datas:
        print(data["data"][0]["price"])
        print(data["data"][0]["direction"])




# 打印结束语句
get_price(base_url)
print("--------------------------")
print("---------COMPLETE---------")
