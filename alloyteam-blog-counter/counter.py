__author__ = 'laispace.com'

# -*- coding: UTF-8 -*-

import urllib.request
import re

class Spider:

    def __init__ (self, pageStartNum, pageEndNum, year, monthStart, monthEnd, sortOutput) :
        self.baseUrl = 'http://alloyteam.com/page/'
        self.pageStartNum = pageStartNum
        self.pageEndNum = pageEndNum
        self.year = year
        self.monthStart = monthStart
        self.monthEnd = monthEnd
        self.sortOutput = sortOutput

    def getPage (self, pageNum):
        url = self.baseUrl + str(pageNum)
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
        page = res.read().decode('utf8')
        code = res.getcode()
        print(url, code)
        return page

    def getPost (self, pageNum):
        page = self.getPage(pageNum)
        reStr1 = '<a href="(.*?)".*?class="blogTitle".*?>(.*?)</a>'
        reStr2 = '.*?<div class="blogPs">.*?on (.*?) by <a href="(.*?)".*?rel="author">(.*?)</a>.*?view: (.*?) </div>'
        pattern = re.compile(reStr1+reStr2, re.S)
        items = re.findall(pattern, page)
        list = []
        for index, item in enumerate(items):
            post = (
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5]
            )
            list.append(post)
        return list

    def getPosts (self):
        list = []
        for i in range(self.pageStartNum, self.pageEndNum + 1):
            _list = self.getPost(i)
            list += _list
        return list


pageStartNum = 1
pageEndNum = 10
year = 2015
monthStart = 6
monthEnd = 11
sortOutput = True

spider = Spider(pageStartNum, pageEndNum, year, monthStart, monthEnd, sortOutput)
posts = spider.getPosts()

for month in range(monthStart, monthEnd):
    list = [];
    year = str(year)
    month = str(month)
    if (len(month) == 1):
        month = '0' + month
    yearMonthStr = year + '年' + month + '月'
    for post in posts:
        if (re.search(yearMonthStr, post[2])):
            list.append(post)
    list = sorted(list, key=lambda item: int(item[5].replace(',', '')), reverse=True)

    formatStr = '{:<5} {:<10} {:<15} {:<15} {:<50}'
    print(year + '年' + month + '月写的文章有：')
    print(formatStr.format('排名', '阅读量', '时间', '作者', '标题'))
    for index, post in enumerate(list):
        print(formatStr.format(index+1, post[5], post[2], post[4],post[1]))