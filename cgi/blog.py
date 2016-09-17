# python3.5
# -*- coding: utf-8 -*-
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
        new_blog = app.getBody()
        print(new_blog)
        app.header('Content-type', 'text/html')
        return new_blog.encode("utf-8")

blogFront = BlogFront()
newPost = NewPost()
