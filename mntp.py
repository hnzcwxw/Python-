import urllib2
import re
import os

class MNTP:
    def __init__(self):
        self.contents = []
        self.endurl = True

    def getPage(self, pageNum):
        try:
            url = "http://www.27270.com/ent/meinvtupian/2016/168651_" + str(pageNum) + ".html"

            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                return None

    def getConten(self, page):
        pattern = re.compile('(<strong|div)+ id=\'mouse\'.*?src="(.*?)".*?', re.S)
        items = re.findall(pattern, page)

        self.contents.append(items[0][1])
        if items[0][0] == 'div':
            self.endurl = False

    def saveImg(self, imageURL, fileName):
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    def mkdri(self, path):
        isExists = os.path.exists(path)
        if not isExists:
            os.mkdir(path)
            return True
        else:
            return False


    def start(self):
        i = 1
        while self.endurl:
            self.getConten(self.getPage(i))

            i += 1
        for j in range(len(self.contents)):
            self.saveImg(self.contents[j], "tupian/zhuying/" + str(j))

mvtp = MNTP()
mvtp.start()


