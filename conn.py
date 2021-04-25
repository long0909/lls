"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   4/10/21 7:04 PM
@desc:
"""

import time
import threading
import pymysql
from DBUtils.PooledDB import PooledDB


class Singleton(object):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


class MySqlconn(Singleton):
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get("host")
        self.port = kwargs.get("port")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.maxcached = kwargs.get("maxcached")
        self.maxconnections = kwargs.get("maxconnections")
        self.mincached = kwargs.get("mincached")

    __pool = {}

    def get_conn(self):
        conn_pool = MySqlconn.__pool.get("default")
        conn = conn_pool.connection()
        conn._con._con.select_db("xiaolong")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor ,conn

    def init_conn(self):
        conn_pool = PooledDB(creator=pymysql, blocking=True, host=self.host, port=self.port, user=self.user,
                             mincached=self.mincached,
                             maxcached=self.maxcached, maxconnections=self.maxconnections, password=self.password,
                             charset="utf8")
        MySqlconn.__pool.setdefault("default", conn_pool)


def init_conn_pool():
    mysql = MySqlconn(host="47.102.131.18", port=3306, user="root", password="123456",mincached=10,maxcached=20,maxconnections=50)
    mysql.init_conn()


if __name__ == "__main__":
    init_conn_pool()
    aaa = MySqlconn()
    conn = aaa.get_conn()
    conn.execute("select * from user")
