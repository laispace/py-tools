__author__ = 'laispace.com'

import sqlite3

dbname = 'alloyteam.db'

def createTable():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                (url text primary key,
                 title text,
                 date text,
                 authorLink text,
                 authorName text,
                 view text)
              ''')
    conn.commit()
    conn.close()

def createPosts(posts):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for post in posts:
        c.execute('INSERT OR REPLACE INTO posts VALUES (?,?,?,?,?,?)', post)
    # c.executemany('INSERT OR REPLACE INTO posts VALUES (?,?,?,?,?,?)', posts)
    conn.commit()
    conn.close()

def readPosts():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.commit()
    conn.close()
    return posts

def dropTable():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('DROP table IF EXISTS posts')
    conn.commit()
    conn.close()
