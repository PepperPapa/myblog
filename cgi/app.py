# python3.5
# -*- coding: utf-8 -*-

# 使用uwsgi server，必须使用application作为方法名或类名
class application:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        # path format: /myblog/*d
        path = self.environ['PATH_INFO'].split("/")[2]
        if path == "hello":
            return self.GET_hello()
        else:
            return self.notfound()

    def GET_hello(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/html')]
        self.start_response(status, response_headers)
        yield "Hello world!\n".encode("utf-8")

    def notfound(self):
        status = "404 Not Found"
        response_headers = [('Content-type', 'text/html')]
        self.start_response(status, response_headers)
        yield "Not Found\n".encode("utf-8")
