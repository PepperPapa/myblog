# python3.5
# -*- coding: utf-8 -*-

def application(environ, start_response):
    # 使用uwsgi server，必须使用application作为方法名
    status = "200 OK"
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return ['Hello world!\n'.encode('utf-8')]
