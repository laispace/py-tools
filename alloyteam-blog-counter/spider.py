__author__ = 'laispace.com'

# -*- coding: UTF-8 -*-

import urllib.request
import re
import db
import csv

class Spider:

    def __init__ (self) :

        self.baseUrl = 'http://alloyteam.com/page/'

        self.pageNum = 1

    def getPage (self, pageNum):
        url = self.baseUrl + str(pageNum)
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
        page = res.read().decode('utf8')
        code = res.getcode()
        print(pageNum, code)
        return page

    def getPost (self, pageNum):
        print('#'*10, 'start get page %s' % pageNum)
        page = self.getPage(pageNum)
        reStr1 = '<a href="(.*?)".*?class="blogTitle".*?>(.*?)</a>'
        reStr2 = '.*?<div class="blogPs">.*?on (.*?) by <a href="(.*?)".*?rel="author">(.*?)</a>.*?view: (.*?) </div>'
        pattern = re.compile(reStr1+reStr2,re.S)
        items = re.findall(pattern,page)

        list = [];
        for index, item in enumerate(items):
            print('%s-%s: %s' %(pageNum, index, item[1]))
            post = (
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5]
            )
            list.append(post)
        print('#'*10, 'end get page %s \n' % pageNum)

        return list

    def getPosts (self, pageStartNum, pageEndNum):
        list = [];
        for i in range(pageStartNum, pageEndNum + 1):
            _list = self.getPost(i)
            list += _list
        return list

    def savePosts (self, contents):
        pass

    def savePostsToCSV(self, fileName, posts):
        with open(fileName, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for post in posts:
                writer.writerow(post)

# save to database
# db.dropTable()
# db.createTable()

spider = Spider()
posts = spider.getPosts(1, 2)
spider.savePostsToCSV('alloyteam-blog-post.csv', posts)

# db.createPosts(posts)

# posts = db.readPosts()

# print('posts: %s' % len(posts))
