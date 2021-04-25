"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   4/20/21 8:09 PM
@desc:
"""

import conn


class Feed(object):
    def __init__(self):
        pass

    def List(self):
        con, _ = conn.MySqlconn().get_conn()
        con.execute(f"select * from feed")
        return con.fetchall()

    def Add(self, project: str, time: str, animal: str, feed: float, close_status: int):
        con, ccon = conn.MySqlconn().get_conn()
        try:
            con.execute(
                f"insert into feed(project,time,animal,feed,close_status) values('{project}','{time}','{animal}',{feed},{close_status});")
        except Exception as e:
            print(e)
            ccon.rollback()
        return ccon.commit()

    def Update(self, update_info: dict, feed_id: int):
        con, ccon = conn.MySqlconn().get_conn()
        if len(update_info) == 0:
            return
        update_list = []
        for k in update_info:
            update_list.append(f"{k} = '{update_info[k]}'")
        update_str = ",".join(update_list)
        con.execute(
            f"update feed set {update_str} where id = {feed_id};")
        return ccon.commit()

    def Delete(self, id: int):
        con, ccon = conn.MySqlconn().get_conn()
        try:
            con.execute(f"delete from feed where id = {id};")
        except:
            ccon.rollback()
        return ccon.commit()
