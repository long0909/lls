"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   4/20/21 8:09 PM
@desc:
"""


import conn


class Warning(object):
    def __init__(self):
        pass

    def Update(self,table: str, CO2:str, Temperature:str, Humidity:str, Bodytemperature:str):
        con, ccon = conn.MySqlconn().get_conn()
        print(f"update {table} set CO2='{CO2}',Temperature='{Temperature}',Humidity='{Humidity}',Bodytemperature='{Bodytemperature}'")
        con.execute(f"update {table} set CO2='{CO2}',Temperature='{Temperature}',Humidity='{Humidity}',Bodytemperature='{Bodytemperature}'")
        ccon.commit()
        return


    def Get(self,table: str):
        con, _ = conn.MySqlconn().get_conn()
        con.execute(f"select * from {table};")
        return con.fetchone()
