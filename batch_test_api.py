"""
@author: wangzhenqiang
@email:  wangzhenqiang@ishumei.com
@data:   2020-12-23 20:44
@desc:
"""

import tornado.ioloop
import tornado.web
import json
import subprocess
import uuid
import os
import conn
from model import farm
from model import user
from model import feed
from model import warning
import datetime
import re



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.timedelta):
            return str(obj)
        else:
            return json.JSONEncoder.default(self,obj)


class BaseHandler(tornado.web.RequestHandler):
    #  允许跨域访问的地址
    def allowMyOrigin(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名也可以是*
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def returnJson(self, body):
        return_info = {
            "content": body,
        }
        self.write(return_info)

    def returnError(self, message):
        self.send_error(500, reason=message)


class MainHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def get(self):
        self.write("Hello, world")

    def post(self, *args, **kwargs):
        self.write(self.get_body_argument("type", ""))


class LoginHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        r = json.loads(self.request.body)
        username = r.get("username", "")  # 获取用户名
        password = r.get("password", "")  # 获取密码
        u = user.User()
        r = u.Get(username, password)
        if r == None:
            self.set_status(500)
            self.write(
                {
                    "content": {"message": "登陆失败"},
                }
            )

        else:
            self.returnJson({"message": "登陆成功", "user_id": r.get("id", 0)})


class RegisterHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        r = json.loads(self.request.body)
        print(self.request.body)
        username = r.get("username", "")  # 获取用户名
        password = r.get("password", "")  # 获取密码
        email = r.get("email", "")  # 获取密码
        age = r.get("age", 0)  # 获取密码
        phone = r.get("phone", "")  # 获取密码
        introduction = r.get("introduction", "")  # 获取密码

        u = user.User()
        try:
            if len(u.List(username)) > 0:
                self.set_status(500)
                self.write(
                    {
                        "content": {"message": "注册失败用户名已存在"},
                    }
                )
                return
            u.Add(username, password, email, age, phone, introduction)
            self.returnJson({"message": "注册成功请移步登陆界面登陆"})
        except Exception as e:
            print(e)
            self.set_status(500)
            self.write(
                {
                    "content": {"message": "注册失败"},
                }
            )

class FarmAddHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        animal = rb.get("animal", "")
        gender = rb.get("gender", "")
        quantity = rb.get("quantity", 0)
        area = rb.get("area", 0)
        density = rb.get("density", 0)

        f = farm.Farm()
        f.Add(animal, gender, quantity, area, density)
        return



class FarmDeleteHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        farm_id = rb.get("farm_id", "")

        f = farm.Farm()
        f.Delete(farm_id)
        return



class FarmUpdateHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        farm_id = rb.get("id", "")
        update_info = rb.get("info", {})


        f = farm.Farm()
        f.Update(update_info, farm_id)
        return


class FarmListHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        try:
            rb = json.loads(self.request.body)
        except:
            rb = {}

        animal = rb.get("animal", "")
        f = farm.Farm()
        info_list = f.List(animal)
        self.returnJson({"info_list": info_list})



class FeedAddHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        project = rb.get("project", "")
        time = rb.get("time", "")
        animal = rb.get("animal", "")
        feed1 = rb.get("feed", 0)
        close_status = rb.get("close_status", 0)

        f = feed.Feed()
        f.Add(project, time, animal, feed1, close_status)
        return



class FeedDeleteHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        feed_id = rb.get("feed_id", "")

        f = feed.Feed()
        f.Delete(feed_id)
        return



class FeedUpdateHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        feed_id = rb.get("feed_id", "")
        update_info = rb.get("info", {})


        f = feed.Feed()
        f.Update(update_info, feed_id)
        return


class FeedListHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):

        f = feed.Feed()
        info_list = f.List()
        for info in info_list :
            info["time"] = str(info["time"])
        self.returnJson({"info_list": info_list})



class WarningUpdateHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        table = rb.get("table", "")
        CO2 = rb.get("CO2", "")
        Temperature = rb.get("Temperature", "")
        Humidity = rb.get("Humidity", "")
        Bodytemperature = rb.get("Bodytemperature", "")


        w = warning.Warning()
        w.Update(table, CO2, Temperature, Humidity, Bodytemperature)
        return


class WarningGetHandler(BaseHandler):
    def set_default_headers(self):
        self.allowMyOrigin()

    def options(self):
        pass

    def post(self, *args, **kwargs):
        rb = json.loads(self.request.body)

        table = rb.get("table", "")
        w = warning.Warning()
        w_info = w.Get(table)
        self.returnJson({"warning_info":w_info})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/user/login", LoginHandler),
        (r"/api/user/register", RegisterHandler),
        (r"/api/farm/add", FarmAddHandler),
        (r"/api/farm/delete", FarmDeleteHandler),
        (r"/api/farm/update", FarmUpdateHandler),
        (r"/api/farm/list",   FarmListHandler),
        (r"/api/feed/add", FeedAddHandler),
        (r"/api/feed/delete", FeedDeleteHandler),
        (r"/api/feed/update", FeedUpdateHandler),
        (r"/api/feed/list", FeedListHandler),
        (r"/api/warning/update", WarningUpdateHandler),
        (r"/api/warning/get", WarningGetHandler),

    ])


if __name__ == "__main__":
    conn.init_conn_pool()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()