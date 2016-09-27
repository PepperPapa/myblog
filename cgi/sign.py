# python3.5
# -*- coding: utf-8 -*-
import re
import hashlib
import hmac
import json
import random
import string

if __name__ == '__main__':
    import db
else:
    from cgi import db

SECRECT = "Think Big, Start Small!".encode("utf-8")

def checkUserName(username):
    rule = r'[a-zA-Z_][a-zA-Z0-9_]{5,15}'
    return re.match(rule, username)

def checkPassword(password):
    rule = r'\S{6,26}'
    return re.match(rule, password)

def checkVerify(password, verify):
    return password == verify

def make_secure_val(val):
    return "{}|{}".format(val,
                          hmac.new(SECRECT, val.encode("utf-8")).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    return secure_val == make_secure_val(val)

def make_salt(length = 5):
    return "".join(random.choice(string.ascii_letters) for x in range(length))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256((name + pw + salt).encode("utf-8")).hexdigest()
    return "{},{}".format(salt, h)

def valid_pw(name, password, h):
    salt = h.split(",")[0]
    return h == make_pw_hash(name, password, salt)

class Signup:
    def get(self, app, *args):
        f = open("signup.html")
        content = f.read()
        f.close()
        app.header('Content-type', 'text/html')
        return content.encode("utf-8")

        # # test code
        # html = "<table>\n"
        # for k, v in app.environ.items():
        #     html += "<tr><td>{}</td><td>{}</td></tr>\n".format(k, v)
        # html += "</table>\n"
        #
        # return html.encode("utf-8")

    def post(self, app, *args):
        have_error = False
        # get username, password, verify from the request body
        user = app.getBody()
        user = re.match(r'(.*)=(.*)&(.*)=(.*)&(.*)=(.*)', user).groups()
        user = dict([user[0:2], user[2:4], user[4::]])

        # validate username, password, verify
        if (not checkUserName(user["username"]) or
           not checkPassword(user["password"]) or
           not checkVerify(user["password"], user["verify"])):
           have_error = True

        if have_error:
            # 注册失败通过url传递错误信息
            return app.redirect('/myblog/signup?error=' +
                    'username or password have some error.')
        else:
            user["password"] = make_pw_hash(user["username"], user["password"])
            user["verify"] = make_pw_hash(user["username"], user["verify"])
            new_user = db.user.createUser(user["username"],
                                          user["password"],
                                          user["verify"])

            app.header('Content-type', 'text/html')
            if new_user:
                # 注册成功通过url传递用户名信息
                return app.redirect('/myblog?username=%s' % new_user["username"])
            else:
                # user already exists.
                return app.redirect('/myblog/signup?error=' +
                        'user %s already exits.' % user["username"])
register = Signup()

if __name__ == '__main__':
    print(make_secure_val("zhongxin"))
    print(check_secure_val("zhongxin|78b62f165cc329585eeea6e57ac885ff"))
    print(make_salt())
    print(make_pw_hash("zx", "zx1234"))
    print(valid_pw("zx", "zx1234", "wfYlW,7d7bd2335220dc5d70b9db6a683c0ec5881e287d7fca4f5c7c3ce1cd1462876d"))
