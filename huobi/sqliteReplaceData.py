'''
    为什么打印不出来数据？？？
'''

import sqlite3


def getData():
    # coin=highPrice=lowPrice=enterpriseId=agentId=secret = ''
    conn = sqlite3.connect('huobi.db')
    cur = conn.cursor()
    sql1 = '''
        CREATE TABLE IF NOT EXISTS huobi (id int primary key not null,
                            coin char(50) not null,
                            highPrice char(50) not null,
                            lowPrice char(50) not null,
                            enterpriseId char(50) not null,
                            agentId char(50) not null,
                            secret char(50) not null);
    '''
    sql2 = '''
        REPLACE INTO huobi (id,coin,highPrice,lowPrice,enterpriseId,agentId,secret) values (1,"dogeusdt","111","0.1","abc","def","ghi");
    '''
    sql3 = '''
        select * from huobi
    '''
    sql4 = '''
        select count(*) as aaa from huobi
    '''
    cur.execute(sql1)
    # cur.execute(sql2)
    cur.execute(sql3)
    if len(list(cur)) != 1:
        print('没有数据')
    else:
        cur.execute(sql3)
        for row in cur:
            coin=row[1]
            highPrice=row[2]
            lowPrice=row[3]
            enterpriseId=row[4]
            agentId=row[5]
            secret=row[6]
            # print(coin,highPrice,lowPrice,enterpriseId,agentId,secret)
    # conn.commit()
    cur.close()
    conn.close()
    return coin,highPrice,lowPrice,enterpriseId,agentId,secret

# getData()
# coin,highPrice,lowPrice,enterpriseId,agentId,secret = getData()
# print(coin,highPrice,lowPrice,enterpriseId,agentId,secret)

def insertData():
    aa = '111'
    bb = '222'
    cc = '444'
    conn = sqlite3.connect('huobi.db')
    cur = conn.cursor()
    sql2 = '''
            REPLACE INTO huobi (id,coin,highPrice,lowPrice,enterpriseId,agentId,secret) values (1,"dogeusdt","111","0.1",?,?,?);
        '''
    cur.execute(sql2,(aa,bb,cc))
    # cur.execute('REPLACE INTO huobi (id,coin,highPrice,lowPrice,enterpriseId,agentId,secret) values (1,"dogeusdt","111","0.1",?,?,?)',(aa,bb,cc))
    conn.commit()
    cur.close()
    conn.close()

insertData()