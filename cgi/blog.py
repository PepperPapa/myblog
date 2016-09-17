# python3.5
# -*- coding: utf-8 -*-
import re
import time

if __name__ == '__main__':
    import db
else:
    from cgi import db

class BlogFront:
    def get(self, app, *args):
        # app为application对象
        # wsgi server会以根目录寻找文件，而不是app.py所在的目录寻找
        f = open("index.html")
        content = f.read()
        f.close()
        app.header('Content-type', 'text/html')
        return content.encode("utf-8")

class NewPost:
    def get(self, app, *args):
        f = open("newpost.html")
        content = f.read()
        f.close()
        app.header('Content-type', 'text/html')
        return content.encode("utf-8")

    def post(self, app, *args):
        new_post = app.getBody()
        new_post_dict = self.newpost_dict(new_post)
        app.header('Content-type', 'text/html')
        return "success".encode("utf-8")

    def newpost_dict(self, new_post):
        rule = r'.+=(.+)&.+=(.+)'
        match = re.match(rule, new_post)
        new_post = {}
        new_post["subject"] = match.groups()[0]
        new_post["conntent"] = match.groups()[1]
        day = time.strftime("%b %m, %Y", time.localtime())
        new_post["created"] = day
        new_post["last_modified"] = day
        return new_post

blogFront = BlogFront()
newPost = NewPost()
