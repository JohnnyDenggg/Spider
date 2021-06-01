import urllib.request,urllib.error
from bs4 import BeautifulSoup


def main():
    url = 'https://www.huobi.ci/zh-cn/exchange/doge_usdt/'
    getData(url)


def getData(url):
    askUrl(url)

def askUrl(url):
    head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    request = urllib.request.Request(url,headers=head)
    html=''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html


if __name__ == '__main__':
    main()