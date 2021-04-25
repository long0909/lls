"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   4/20/21 8:09 PM
@desc:
"""

import conn


class Farm(object):
    def __init__(self):
        pass

    def List(self, animal: str):
        con, _ = conn.MySqlconn().get_conn()
        where_list = []
        where = ""
        if animal != "":
            where_list.append(f"animal = '{animal}'")
        if len(where_list) > 0:
            where = "where " + " and ".join(where_list)
        con.execute(f"select * from farm {where}")
        return con.fetchall()

    def Add(self, animal: str, gender: str, quantity: float, area: float, density: float):
        con, ccon = conn.MySqlconn().get_conn()
        try:
            con.execute(
                f"insert into farm(animal,gender,quantity,area,density) values('{animal}','{gender}',{quantity},{area},{density});")
        except:
            ccon.rollback()
        return ccon.commit()

    def Update(self, update_info: dict, farm_id: int):
        con, ccon = conn.MySqlconn().get_conn()
        if len(update_info) == 0:
            return
        update_list = []
        for k in update_info:
            update_list.append(f"{k} = '{update_info[k]}'")
        update_str = ",".join(update_list)
        con.execute(
            f"update farm set {update_str} where id = {farm_id};")
        return ccon.commit()

    def Delete(self, id: int):
        con, ccon = conn.MySqlconn().get_conn()
        try:
            con.execute(f"delete from farm where id = {id};")
        except:
            ccon.rollback()
        return ccon.commit()
