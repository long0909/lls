"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   4/20/21 8:09 PM
@desc:
"""

import conn


class User(object):
    def __init__(self):
        pass

    def Get(self, username: str, password: str):
        con,_ = conn.MySqlconn().get_conn()
        con.execute(f"select * from user where username='{username}' and password='{password}'")
        return con.fetchone()


    def List(self, username: str):
        con,_ = conn.MySqlconn().get_conn()
        con.execute(f"select * from user where username='{username}'")
        return con.fetchall()


    def Add(self, username: str, password: str, email: str, age: int, phone: str, introduction: str):
        con,ccon = conn.MySqlconn().get_conn()
        try:
            print(f"insert into user(username,password,email,age,phone,introduction) values('{username}','{password}','{email}',{age},'{phone}','{introduction}');")
            con.execute(f"insert into user(username,password,email,age,phone,introduction) values('{username}','{password}','{email}',{age},'{phone}','{introduction}');")
        except:
            ccon.rollback()
        return ccon.commit()