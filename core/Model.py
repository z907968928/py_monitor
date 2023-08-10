# encoding: utf-8

import pymysql
from datetime import date, datetime
from data_service_monitor.init.init_base import database_conf
from data_service_monitor.tool.log import write_log


class DataBaseHandle(object):
    """ 定义一个 MySQL 操作类"""
    def __init__(self, db):
        DATABASES = database_conf()
        """初始化数据库信息并创建数据库连接"""
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = DATABASES[db]['HOST']
        self.username = DATABASES[db]['USER']
        self.password = DATABASES[db]['PASSWORD']
        self.database = DATABASES[db]['DB']
        self.port = DATABASES[db]['PORT']
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, self.port, charset='utf8')
        self.cursor = None

    def insert_db(self, sql, param=()):
        """ 插入数据库操作 """

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql, param)
            # ret = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(ret)
            self.db.commit()
        except Exception as e:
            write_log('monitor.log.wf', error='insert error', err_msg=str(e), sql=sql)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def delete_db(self, sql, param=()):
        """ 操作数据库数据删除 """
        self.cursor = self.db.cursor()
        try:
            # 执行sql
            self.cursor.execute(sql, param)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            write_log('monitor.log.wf', error='delete error', err_msg=str(e), sql=sql)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def update_db(self, sql, param=()):
        """ 更新数据库操作 """

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql, param)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except Exception as e:
            write_log('monitor.log.wf', error='update error', err_msg=str(e), sql=sql)
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def select_db(self, sql, param=()):
        """ 数据库查询 """
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        try:
            self.cursor.execute(sql, param)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchall()  # 返回所有记录列表

            for row in range(0, len(data)):
                for k, v in data[row].items():
                    if isinstance(v, (datetime, date)):
                        data[row][k] = data[row][k].isoformat()
            return data
        except Exception as e:
            write_log('monitor.log.wf', error='select error', err_msg=str(e), sql=sql)
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def select_one(self,sql, param=()):
        """ 数据库查询 """
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        try:
            self.cursor.execute(sql, param)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchone()  # 返回所有记录列表

            for row in range(0, len(data)):
                for k, v in data[row].items():
                    if isinstance(v, (datetime, date)):
                        data[row][k] = data[row][k].isoformat()
            return data
        except Exception as e:
            write_log('monitor.log.wf', error='select error', err_msg=str(e), sql=sql)
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def __del__(self):
        self.db.close()
