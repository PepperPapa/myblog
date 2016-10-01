# python3.5
# -*- coding: utf-8 -*-
import re
import time
import urllib.parse
import json

if __name__ == '__main__':
    import db
else:
    from cgi import db

POST_TEMPLATE = """
    <article>
        <h2><a href="{link}">{subject}</a></h2>
        <div>{date}</div>
        <div>{content}</div>
    </article>
"""

def post_as_dict(post):
    return {
        "id": post[0],
        "subject": post[1],
        "content": post[2],
        "created": post[3],
        "last_modified": post[4]
    }

class BlogFront:
    def get(self, app, *args):
        # app为application对象
        # wsgi server会以根目录寻找文件，而不是app.py所在的目录寻找
        all_posts = db.blog.getAllPosts()
        if all_posts:
            if app.format == "html":
                post_html = []
                for post in all_posts:
                    # id, subject, content, created, last_modified
                    post_info = {"subject": post[1],
                                 "date": post[4],
                                 "content": post[2],
                                 "link": "/myblog/%s" % post[0]}
                    post_block = POST_TEMPLATE.format(**post_info)
                    post_html.append(post_block)
                post_html = "\n".join(post_html)
                f = open("index.html")
                index_html = f.read()
                f.close()
                index_html = index_html.replace("{{posts}}", post_html)
                app.header('Content-type', 'text/html; charset=UTF-8')
                return index_html.encode("utf-8")
            else:
                json_all_post = []
                for post in all_posts:
                    json_all_post.append(post_as_dict(post))
                json_all_post = json.dumps(json_all_post)
                app.header('Content-type', 'application/json; charset=UF-8')
                return json_all_post.encode("utf-8")

class PostPage:
    def get(self, app, *args):
        post = db.blog.getPostById(args[0])
        if post:
            if app.format == "html":
                f = open("post.html")
                post_html = f.read()
                f.close()
                # id, subject, content, created, last_modified
                post_info = {"subject": post[1],
                             "date": post[4],
                             "content": post[2],
                             "link": "#"}
                post_block = POST_TEMPLATE.format(**post_info)

                post_html = post_html.format(**{"subject": post[1],
                                                "post": post_block})
                app.header('Content-type', 'text/html; charset=UTF-8')
                return post_html.encode("utf-8")
            else:
                print(post)
                json_post = json.dumps(post_as_dict(post))
                app.header('Content-type', 'application/json; charset=UF-8')
                print(json_post)
                return json_post.encode("utf-8")
        else:
            return app.notfound()

class NewPost:
    def __init__(self):
        self.id = db.blog.newpostID()

    def get(self, app, *args):
        f = open("newpost.html")
        content = f.read()
        f.close()
        app.header('Content-type', 'text/html; charset=UTF-8')
        return content.encode("utf-8")

    def post(self, app, *args):
        new_post = app.getBody()
        new_post_list = self.newpost_list(new_post)
        app.header('Content-type', 'text/html; charset=UTF-8')
        if db.blog.newpost(new_post_list):
            return app.redirect("/myblog/%s" % new_post_list[0])
        else:
            return app.serverError()

    def newpost_list(self, new_post):
        # id, subject, content, created, last_modified
        rule = r'.+=(.+)&.+=(.+)'
        match = re.match(rule, new_post)
        new_post = []
        new_post.append(self.id)
        self.id += 1    # self.id始终记录最新的post id
        subject = urllib.parse.unquote(match.groups()[0])
        subject = subject.replace("+", " ").replace("\r\n", "<br>")
        new_post.append(subject)
        content = urllib.parse.unquote(match.groups()[1])
        content = content.replace("+", " ").replace("\r\n", "<br>")
        new_post.append(content)
        day = time.strftime("%b %d, %Y", time.localtime())
        new_post.append(day)
        new_post.append(day)
        return new_post

blogFront = BlogFront()
newPost = NewPost()
postPage = PostPage()

if __name__ == '__main__':
    pass
