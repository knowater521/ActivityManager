import xlrd
from sqlalchemy import Column, Text, create_engine, VARCHAR, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Setting
mysqlUser = 'warehouse'
mysqlPwd = 'root'
mysqlPort = '3306'
dataBase = 'warehouse'

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    __tablename__ = 'name'
    user = Column(VARCHAR, primary_key=True)
    pwd = Column(Text)
    admin = Column(BOOLEAN, default=0)

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def __repr__(self):
            return "{0} {1} admin:{2}".format(self.user, self.pwd, self.admin)


class AddUser:
    # 初始化数据库连接:
    def __init__(self):
        engine = create_engine('mysql+pymysql://{0}:{1}@localhost:{2}/{3}?charset=utf8'.format(mysqlUser, mysqlPwd,
                                                                                               mysqlPort, dataBase))
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=engine)
        self.session = None
        self.data = None

    def create_session(self):
        print("尝试连接数据库")
        try:
            self.session = self.DBSession()
        except Exception as err:
            print(err, '数据库连接失败,程序即将退出')
            exit()

    def close_session(self):
        print("断开数据库连接")
        self.session.close()
        self.session = None

    def read_database(self):
        if self.session is None:
            self.create_session()

        user = self.session.query(User).all()
        print('\n目前数据库内容：\n')
        for one in user:
            print(one)
        print('---End---')

    def open_xls(self):
        xls_file = 'name.xls'
        try:
            self.data = xlrd.open_workbook(xls_file)
        except IOError:
            print('文件打开失败')

    def read_excel(self):
        if self.session is None:
            self.create_session()

        self.open_xls()
        table = self.data.sheets()[0]
        rows = table.nrows  # 行数
        print("共{}行".format(rows))
        for rownum in range(0, rows):
            row = table.row_values(rownum)
            if row:
                print(row[0], row[1])
                # 创建新User对象:
                new_user = User(row[0], row[1])
                # 添加到session:
                self.session.add(new_user)
        print('sql生成完毕，即将导入')
        # 提交即保存到数据库:
        self.session.commit()
        print('导入成功')
        # 关闭session:
        self.close_session()
        print('程序运行完毕，断开数据库连接')
        print('success')

    def clear_table(self):
        if self.session is None:
            self.create_session()
        self.session.query(User).delete()
        self.session.commit()
        print("清空完成")

if __name__ == '__main__':
    x = AddUser()
    xx = input('输入Y表示清空数据表，输入其他不请空')
    if xx == 'Y':
        print('清空数据表')
        input('按回车键开始')
        x.clear_table()
    else:
        print('不请空数据表')
    x.read_database()
    input('按回车键开始导入user.xls内的用户信息')
    x.read_excel()

# print(read_excel("/Users/CYC/Desktop/test.xls"))
