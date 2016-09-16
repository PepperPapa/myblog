# python3.5
# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    import db
else:
    from cgi import db

# 使用uwsgi server，必须使用application作为方法名或类名
class application:
    urls = (
        ("/myblog/?(\?.*)?", "index"),
        ("/myblog/newpost/?", "newpost"),
        ("/myblog/signup/?(\?.*)?", "signup"),
    )

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.status = "200 OK"
        self._headers = []

    def __iter__(self):
        result = self.delegate()
        self.start_response(self.status, self._headers)

        # 将返回值result(字符串或字符串列表)转换为迭代对象
        if isinstance(result, bytes):
            return iter([result])
        else:
            return iter(result)

    def delegate(self):
        # path format: /myblog/*
        path = self.environ['PATH_INFO']
        print("\n\n"+path+"\n\n")
        method = self.environ['REQUEST_METHOD']

        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + '_' + name
                if hasattr(self, funcname):
                    func = getattr(self, funcname)
                    return func(*args)

        return self.notfound()

    def header(self, name, value):
        self._headers.append((name, value))

    def GET_index(self, *args):
        # wsgi server会以根目录寻找文件，而不是app.py所在的目录寻找
        f = open("index.html")
        content = f.read()
        f.close()
        self.header('Content-type', 'text/html')
        return content.encode("utf-8")

    def GET_newpost(self, *args):
        f = open("newpost.html")
        content = f.read()
        f.close()
        self.header('Content-type', 'text/html')
        return content.encode("utf-8")

    def POST_newpost(self, *args):
        new_blog = self.getBody()
        print(new_blog)

    def GET_signup(self, *args):
        f = open("sign.html")
        content = f.read()
        f.close()
        self.header('Content-type', 'text/html')
        return content.encode("utf-8")

    def POST_signup(self, *args):
        user = self.getBody()
        user = re.match(r'(.*)=(.*)&(.*)=(.*)&(.*)=(.*)', user).groups()
        user = dict([user[0:2], user[2:4], user[4::]])
        new_user = db.user.createUser(user["username"],
                                      user["password"],
                                      user["verify"])

        self.header('Content-type', 'text/html')
        if new_user:
            # 注册成功通过url传递用户名信息
            return self.redirect('/myblog?username=%s' % new_user["username"])
        else:
            # 注册失败通过url传递错误信息
            return self.redirect('/myblog/signup?error=' +
                    'user %s already exits.' % user["username"])

        # test code
        # html = "<table>\n"
        # for k, v in self.environ.items():
        #     html += "<tr><td>{}</td><td>{}</td></tr>\n".format(k, v)
        # html += "</table>\n"
        #
        # return html

    def notfound(self):
        self.status = "404 Not Found"
        self.header('Content-type', 'text/html')
        return "Not Found\n".encode('utf-8')

    def redirect(self, path):
        self.status = "301 OK"
        self.header('Location', path)
        return "".encode("utf-8")

    def getBody(self):
        content_length = int(self.environ['CONTENT_LENGTH'])
        content = self.environ['wsgi.input'].read(content_length).decode('utf-8')
        return content
