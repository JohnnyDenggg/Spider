from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3


def main():
    url = 'https://movie.douban.com/top250?start='
    # 爬取数据
    datalist = getData(url)
    savePath = '豆瓣电影250.xls'
    dbPath = 'movie250.db'
    # 保存数据
    saveData(datalist,savePath)   # 保存到Excel
    saveData2DB(datalist,dbPath)  # 保存到Sqlite数据库

def askUrl(url):
    head = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
    request = urllib.request.Request(url,headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

# 创建正则表达式对象，表示规则
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(.*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

# 爬取网页
def getData(baseurl):
    datalist = []  # 存放所有电影的信息
    for i in range(0,10):
        url = baseurl + str(i*25)
        # print(url)
        html = askUrl(url)  # 获取网页数据
        # 逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_='item'):
            data = []
            item = str(item)
            link = re.findall(findLink,item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if (len(titles)==2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace('/','')
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 外文名留空
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            judge = re.findall(findJudge,item)[0]
            data.append(judge)
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace('。','')
                data.append(inq)
            else:
                data.append('')
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd)
            bd = re.sub('/',' ',bd)
            data.append(bd.strip())  # 去掉空格
            datalist.append(data)
    print(len(datalist))

    return datalist

# 保存excel数据
def saveData(dataList,savepath):

    book = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 样式压缩效果
    sheet = book.add_sheet('豆瓣电影250',cell_overwrite_ok=True)  # 单元格内容覆盖重写
    col = ('电影详情链接','图片链接','影片中文名','影片外国名','评分','评价数','概况','相关信息')
    for i in range(0,8):
        sheet.write(0,i,col[i])  # 列标题
    for i in range(0,250):
        data = dataList[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)
    print('数据已保存')

# 初始化数据库，创建表格
def init_db(dbPath):
    sql = '''
        create table movie250 ( id integer primary key autoincrement,
                                info_link text,
                                pic_link text,
                                cname varchar,
                                ename varchar,
                                score numeric,
                                rated numeric,
                                introduction text,
                                info text
                                )
    '''
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveData2DB(dataList,dbPath):
    init_db(dbPath)  # 初始化数据库，创建表格
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    for data in dataList:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie250 (info_link,pic_link,cname,ename,score,rated,introduction,info)
                            values (%s)
            '''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print('数据已保存')

if __name__ == '__main__':
    main()
