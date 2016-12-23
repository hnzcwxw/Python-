# -*- coding:utf-8 -*-
import urllib2
import re
import os

class MNTP:
    def __init__(self, mvCode, max):
        self.contents = []
        self.mvCode = str(mvCode)
        self.max = int(max)
        self.endurl = True

    # 取得当前页面内容
    def getPage(self, pageNum, mvCode):
        try:
            url = "http://www.27270.com/ent/meinvtupian/2016/" + mvCode + "_" + str(pageNum) + ".html"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                return None
    # 取得美女编号的名字
    def getName(self, mvCode):
        try:
            url = "http://www.27270.com/ent/meinvtupian/2016/" + mvCode + ".html"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read().decode('gbk')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                pass
        pattern = re.compile('<div class="articleV2Title">.*?<h1>(.*?)</h1>.*?</div>', re.S)
        items = re.findall(pattern, content)
        return items[0]

    # 取得下一个美女的编号
    def getNextCode(self, mvCode):
        try:
            url = "http://www.27270.com/ent/meinvtupian/2016/" + mvCode + ".html"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                pass
        pattern = re.compile('<dl class="articleV2Tag">.*?</dl>.*?<div class="hr10"></div>.*?' +
                             '<script.*?</script>.*? <div class="hr101"></div>.*?<div class="l">.*?</div>' +
                             '.*?<div class="r">.*?<a href=\'(.*?)\'>.*?</div>', re.S)
        items = re.findall(pattern, content)
        if len(items) == 0:
            return None
        else:
            pat1 = re.compile('http://www.27270.com/ent/meinvtupian/2016/(.*?).html', re.S)
            item = re.findall(pat1, items[0])
            return item[0]

    # 取得美女图片的地址
    def getConten(self, page):
        pattern = re.compile('(<strong|div)+ id=\'mouse\'.*?src="(.*?)".*?', re.S)
        items = re.findall(pattern, page)

        self.contents.append(items[0][1])
        if items[0][0] == 'div':
            self.endurl = False

    # 保存美女图片
    def saveImg(self, imageURL, fileName):
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    # 创建美女主题的目录
    def mkdri(self, path):
        path = "tupian/" + path
        isExists = os.path.exists(path)
        if not isExists:
            print "创建新的文件夹：", path, "的文件夹"
            os.mkdir(path)
        else:
            print path, "文件夹已经存在"
        return path + "/"



    def start(self):
        for i in range(self.max):
            j = 1
            path = self.mkdri(self.getName(self.mvCode))
            self.endurl = True
            while self.endurl:
                self.getConten(self.getPage(j, self.mvCode))
#                print self.contents
                j += 1

            for k in range(len(self.contents)):
                print "保存第", k + 1, "张照片..."
                self.saveImg(self.contents[k], path + str(k))

            nextCode = self.getNextCode(self.mvCode)
            if nextCode > 0:
                self.mvCode = str(nextCode)
                self.contents = []
            else:
                print "没有下一个主题了～"
                break

mvCode = int(input("输入美女代码： "))
max = int(input("输入你想要几个美女： "))
mvtp = MNTP(mvCode, max)
mvtp.start()


