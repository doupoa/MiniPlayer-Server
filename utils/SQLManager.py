# python mysql 操作类

import pymysql
import config
import logging


class DB:

    def __init__(self, host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_pwd, database=config.db_database):  # 构造函数        
        try:
            self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.error(e)

    # 返回执行execute()方法后影响的行数

    def execute(self, sql):
        self.cursor.execute(sql)
        rowcount = self.cursor.rowcount
        return rowcount

    # 删除并返回影响行数
    def delete(self, **kwargs):
        table = kwargs['table']

        where = kwargs['where']
        try:
            # 执行SQL语句
            self.cursor.execute('DELETE FROM %s where %s',(table, where))
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
        except:
            # 发生错误时回滚
            self.conn.rollback()
        return rowcount

    # 新增并返回新增ID
    def insert(self, **kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs.items():
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ")values(" + values + ")"
        logging.debug(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 获取自增id
            res = self.cursor.lastrowid 
            return res
        except Exception as e:
            # 发生错误时回滚
            logging.error(e)
            self.conn.rollback()
       

    # 修改数据并返回影响的行数
    def update(self, **kwargs):
        table = kwargs['table']
        # del kwargs['table']
        kwargs.pop('table')
        where = kwargs['where']
        kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs.items():
            sql += "%s='%s'," % (k, v)
        sql = sql.rstrip(',')
        sql += ' where %s' % where
        logging.debug(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            # 影响的行数
            rowcount = self.cursor.rowcount
            return rowcount
        except Exception as e:
            # 发生错误时回滚
            logging.error("SQL error: %s" % e)
            self.conn.rollback()
        

    # 查一条条数据
    def selectTopone(self, field:str="*",table:str=" ",where:str=" ",order:str=" "):
        if where!= " ": 
                where = "where " + where
        try:
            sql = "select {} from {} {} {} limit 1".format(field, table, where, order,)
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            # 发生错误时回滚
            logging.error("SQL error: %s" % e)
            self.conn.rollback()
        

    # 查所有数据
    def selectAll(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        limit = 'limit' in kwargs and 'limit ' + kwargs['limit'] or ''
        try:
            sql = "select {} from {} {} {} {}".format(field, table, where, order,limit)
            logging.debug(sql)
            # 执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            # 发生错误时回滚
            logging.error("SQL error: %s" % e)
            self.conn.rollback()
       


# insert测试
# cs = conn.insert(table="T1", Name="Python测试2", Sex="男")
# print(cs)
 
# delete 测试
# cs = conn.delete(table="T1", where="Id = 2")
# print(cs)
 
# update 测试
# cs = conn.update(table="T1", Name="Python测试3", Sex="man", where="Id in(1,2)")
# print(cs)
 
# select 测试
# cs = conn.selectAll(table="T1", where="Name = 'Python测试3'")