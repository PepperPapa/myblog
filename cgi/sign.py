# python3.5
# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    import db
else:
    from cgi import db

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
        user = app.getBody()
        user = re.match(r'(.*)=(.*)&(.*)=(.*)&(.*)=(.*)', user).groups()
        user = dict([user[0:2], user[2:4], user[4::]])
        new_user = db.user.createUser(user["username"],
                                      user["password"],
                                      user["verify"])

        app.header('Content-type', 'text/html')
        if new_user:
            # 注册成功通过url传递用户名信息
            return app.redirect('/myblog?username=%s' % new_user["username"])
        else:
            # 注册失败通过url传递错误信息
            return app.redirect('/myblog/signup?error=' +
                    'user %s already exits.' % user["username"])


register = Signup()
