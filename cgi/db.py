# -*- coding: utf-8 -*-
#!usr/bin/python3
# ubuntu16.04LTS

import sqlite3
import time
import re

def connectDatabase():
    conn = sqlite3.connect("myblog.db")
    return (conn, conn.cursor())

"""
用户注册、登录等相关
"""
class User:
    def createUserTable(self):
        self.conn, self.cursor = connectDatabase()
        # get all table name in database
        self.cursor.execute("SELECT NAME FROM sqlite_master WHERE TYPE='table'")
        table_list = [name[0] for name in self.cursor.fetchall()]

        if not 'users' in table_list:
            self.cursor.execute("""CREATE TABLE users
                     (ID INTEGER PRIMARY KEY NOT NULL,
                      NAME TEXT NOT NULL,
                      PASSWORD TEXT NOT NULL);""")
        return (self.conn, self.cursor)

    def createUser(self, name, pwd, verify):
        # 如果users不存在则首先创建表users
        self.conn, self.cursor = self.createUserTable()

        # 检查name是否已经存在，不存在才能插入值
        self.cursor.execute("SELECT NAME FROM users WHERE NAME='{}'"
                                .format(name))
        if (not self.cursor.fetchall()):
            id = time.time() * 10000000
            self.cursor.execute("""INSERT INTO users (ID, NAME, PASSWORD)
                           VALUES (?, ?, ?)""", (id, name, pwd))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM users WHERE NAME='{}'"
                                    .format(name))
            user = self.cursor.fetchone()
            self.conn.close()
            # s_: 表示已经加密处理
            return {'id': user[0], 'username': user[1], 'password': user[2]}

    def userByName(self, name):
        self.conn, self.cursor = self.createUserTable()
        self.cursor.execute("SELECT * FROM users WHERE NAME='{}'"
                                .format(name))
        return self.cursor.fetchone()

class Blog:
    def createBlogTable(self):
        self.conn, self.cursor = connectDatabase()
        # get all table name in database
        self.cursor.execute("SELECT NAME FROM sqlite_master WHERE TYPE='table'")
        table_list = [name[0] for name in self.cursor.fetchall()]

        if not 'posts' in table_list:
            self.cursor.execute("""CREATE TABLE posts
                     (ID INTEGER PRIMARY KEY NOT NULL,
                      SUBJECT TEXT NOT NULL,
                      CONETNT TEXT NOT NULL,
                      CREATED TEXT NOT NULL,
                      LAST_MODIFIED TEXT NOT NULL);""")
        return (self.conn, self.cursor)

    def newpost(self, args):
        # 如果posts不存在则首先创建表posts
        self.conn, self.cursor = self.createBlogTable()
        self.cursor.execute("""INSERT INTO posts (ID, SUBJECT, CONETNT, CREATED, LAST_MODIFIED)
                       VALUES (?, ?, ?, ?, ?)""", tuple(args))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM posts WHERE id={}"
                                .format(args[0]))
        query_post = self.cursor.fetchone()
        self.conn.close()
        return query_post

    def getPostById(self, id):
        # 如果posts不存在则首先创建表posts
        self.conn, self.cursor = self.createBlogTable()
        self.cursor.execute("SELECT * FROM posts WHERE id={}"
                                .format(id))
        query_post = self.cursor.fetchone()
        self.conn.close()
        return query_post

    def getAllPosts(self):
        # 如果posts不存在则首先创建表posts
        self.conn, self.cursor = self.createBlogTable()
        self.cursor.execute("SELECT * FROM posts ORDER BY ID DESC LIMIT 15")
        query_posts = self.cursor.fetchall()
        self.conn.close()
        return query_posts

    def newpostID(self):
        # 如果posts不存在则首先创建表posts
        self.conn, self.cursor = self.createBlogTable()
        self.cursor.execute("SELECT * FROM posts ORDER BY ID DESC")
        latest_post = self.cursor.fetchone()
        if latest_post:
            newpost_id = latest_post[0] + 1
            self.conn.close()
        else:
            newpost_id = 1
        return newpost_id


user = User()
blog = Blog()

if __name__ == '__main__':
    user = User()
    print(user.createUser("zhongxin", "zx1234", "zx1234"))
    blog.newpost((1, "test", "test", "2016", "2016"))
