# python3.5
# -*- coding: utf-8 -*-

from app import application

urls = (
    ("/myblog/signup", "signup"),
)

wsgiapp = application(urls, globals())

class signup:
    def POST(self, *args):
        application.header("Content-type", "text/html")
        return "Thanks for signup!"

if __name__ == '__main__':
    main()
