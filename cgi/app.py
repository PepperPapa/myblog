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
        ("/myblog/signup(.*)", "signup"),
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

    def POST_signup(self, *args):
        user = self.getBody()
        user = re.match(r'(.*)=(.*)&(.*)=(.*)&(.*)=(.*)', user).groups()
        user = dict([user[0:2], user[2:4], user[4::]])
        new_user = db.user.createUser(user["username"],
                                      user["password"],
                                      user["verify"])

        self.header('Content-type', 'text/html')
        if new_user:
            self.status = "301 OK"
            self.header('Location', '/myblog/index.html?username=%s'
                                            % new_user["username"])
            return "".encode("utf-8")
        else:
            # TODO:
            self.status = "401 Bad Request"
            return "user already exits.".encode("utf-8")

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

    def getBody(self):
        content_length = int(self.environ['CONTENT_LENGTH'])
        content = self.environ['wsgi.input'].read(content_length).decode('utf-8')
        return content
