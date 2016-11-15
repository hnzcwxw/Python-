import urllib2
import re


class Qsbk:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64)"
        self.headers = {"User-Agent" : self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = "http://www.qiushibaike.com/text/page/" + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Link Error, Reasion:", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "load failed..."
            return None
        pattern = re.compile('<div.*?clearfix">.*?<img.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>' +
                             '.*?<i.*?number">(.*?)</i>.*?<i.*?number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            replaceBr = re.compile('<br/>')
            text = re.sub(replaceBr, "\n", item[1])
            pageStories.append([item[0], text, item[2], item[3]])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStores, page):
        for story in pageStores:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print "Page:%s\tName:%s\tContent:%s\tPrase:%s\tComment:%s\n" % (page, story[0], story[1], story[2], story[3])

    def start(self):
        print "Reading, Q Quit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStory = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStory, nowPage)

spider = Qsbk()
spider.start()


