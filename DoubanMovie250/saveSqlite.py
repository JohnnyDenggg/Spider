import sqlite3

# # 1. 创建数据库
# conn = sqlite3.connect('test.db')  # 打开数据库，没有则创建数据库
# c = conn.cursor()
#
#
# # 2. 创建表格
# sql = '''
#     create table company (id int primary key not null,
#                           name text not null,
#                           age int not null,
#                           address char(50),
#                           salary real);
# '''
# c.execute(sql)
# conn.commit()  # 提交数据库操作
# conn.close()

# 3. 查询数据库
# conn = sqlite3.connect('test.db')  # 打开数据库，没有则创建数据库
# c = conn.cursor()
# sql1 = '''
#     insert into company (id,name,age,address,salary) values (1,'张三',18,'成都',10000);
# '''
# sql2 = '''
#     insert into company (id,name,age,address,salary) values (2,'李四',34,'北京',16000);
# '''
# c.execute(sql1)
# c.execute(sql2)
# conn.commit()  # 提交数据库操作
# conn.close()

# 4. 获取数据
conn = sqlite3.connect('test.db')  # 打开数据库，没有则创建数据库
c = conn.cursor()
sql1 = "select id,name,address,salary from company"
cursor = c.execute(sql1)

for row in cursor:
    print("id=",row[0])
    print('name =',row[1])
    print('address =',row[2])
    print('salary =',row[3],'\n')
conn.close()