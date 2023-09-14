##################
# lib file: 放一些工具函数，与具体业务无直接关系
##################


import pymysql
import time
# 单例模式 https://blog.csdn.net/qq_32539403/article/details/83343581
# 方法很好 https://blog.csdn.net/qy20115549/article/details/82972993
# 更多方法 https://www.cnblogs.com/ddjl/p/8670545.html
# python mysql使用持久链接 https://blog.csdn.net/wzm112/article/details/7745835

#v0.2 self._db.commit() 防止查询缓存，保证数据最新
#v0.3 加了 _reConn() 数据库连接失效后自动重连
class DBUtil():
    """mysql 辅助工具"""
    _db=None
    #在这里配置自己的SQL服务器
    _config = {
        'host':"s3.biomooc.com",
        'port':3306,
        'username':"root",
        'password':'123456',
        'database':"english",
        'charset':"utf8"
    }
    #返回db，方便使用函数
    def db(self):
        return self._db
    #单例模式
    def __connect(self):
        if(self._db == None):
            try:
                self._db = pymysql.connect(
                    host = self._config['host'],
                    port = self._config['port'],
                    user = self._config['username'],
                    passwd = self._config['password'],
                    db = self._config['database'],
                    charset = self._config['charset']
                )
                self._cur=self._db.cursor()
                return True;
            except Exception as e:
                print(e)
                #raise BaseException("连接失败。DataBase connect error,please check the db config.")
                return False;
        print('run empty __connect()')
        return True; #永远不会被执行
    #初始化
    def __init__(self):
        self.__connect()

    # 连接异常后自动重连3次
    def _reConn (self,num = 28800,stime = 3): #重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
            _number = 0 #重连次数
            _status = True
            while _status and _number <= num:
                try:
                    self._db.ping()       #cping 校验连接是否异常
                    _status = False
                except:
                    self._db = None #如果ping不通，则清空，重新连接
                    now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print('>>>重新连接数据库， tried =',_number, '; now:',now)
                    if self.__connect()==True: #重新连接,成功退出
                        _status = False
                        break
                    _number +=1
                    time.sleep(stime)      #连接不成功,休眠3秒钟,继续循环，直到成功或重试次数结束
    #

    #结束销毁连接
    def close(self):
        '''结束查询和关闭连接'''
        if self._cur is not None:
            self._cur.close()
        if self._db is not None:
            self._db.close()
    #创建表
    def create_table(self,sql_str):
        '''创建数据表'''
        try:
            self._cur.execute(sql_str)
        except Exception as e:
            print(e)
    #
    def query(self,sql):
        '''查询数据并返回 tuple
             cursor 为连接光标
             sql为查询语句
        '''
        try:
            self._reConn()
            self._db.commit() #防止缓存
            self._cur.execute(sql)
            rows = self._cur.fetchall()
            return rows
        except Exception as e:
            print(e)
            return False
    #
    def execute(self,sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        try:
            self._reConn()
            self._cur.execute(sql) #成功了总是1
            rs= self._cur.lastrowid  # 最新插入行的主键id
            self._db.commit()
            return rs
        except Exception as e:
            print(e)
            self._db.rollback()
        return False
        #
    def executeMany(self,sqlArr): #对比试验显示，这比着单独执行sql语句速度更慢了。可能是保证都执行，就要牺牲性能。
        '''
        更新多个记录，成功返回最后的id
        '''
        try:
            self._reConn()
            for sql in sqlArr:
                self._cur.execute(sql) #成功了总是1
            rs= self._cur.lastrowid  # 最新插入行的主键id
            self._db.commit()
            return rs
        except Exception as e:
            print(e)
            self._db.rollback()
        return False
    #删除列
    def delCol(self, tableName, colName):
        sql="alter table %s drop %s;"
        rs1=self.execute(sql %(tableName, colName)) #3 如果重复，会报错
        print('删除%s表中的 %s列, rs1=%s' % (tableName, colName, rs1) )
#



from flask import jsonify
#CORS (Cross-Origin Resource Sharing)
def cors(arrOrStr):
    res=jsonify(arrOrStr)
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Backend', 'wjl_dawnDict_server/0.3')
    res.headers.add('Email', 'jimmymall at 163 dot com')
    return res;
#