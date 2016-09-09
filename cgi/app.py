# python3.5
# -*- coding: utf-8 -*-
import re

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
        result = self.delegate().encode("utf-8")
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
        self.status = "301 OK"
        self.header('Content-type', 'text/html')
        self.header('Location', '/myblog/sign.html')

        content_length = int(self.environ['CONTENT_LENGTH'])
        content = self.environ['wsgi.input'].read(content_length).decode('utf-8')
        print("\n %s \n" % content)

        # test code
        html = "<table>\n"
        for k, v in self.environ.items():
            html += "<tr><td>{}</td><td>{}</td></tr>\n".format(k, v)
        html += "</table>\n"

        return html

    def notfound(self):
        self.status = "404 Not Found"
        self.header('Content-type', 'text/html')
        return "Not Found\n"
