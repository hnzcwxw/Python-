import urllib
import urllib2
import re

url = "http://www.qiushibaike.com/text/"
try:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64)"
    headers = {"User-Agent": user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
#    print response.read()
#    pattern = re.compile('<div.*?clearfix">.*?<img.*?<h2(.*?)</h2>.*?<span>(.*?)</span>', re.S)
    pattern = re.compile('<div.*?clearfix">.*?<img.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>' +
                         '.*?<i.*?number">(.*?)</i>.*?<i.*?number">(.*?)</i>', re.S)
#                         '<span>(.*?)</span>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print item[0]
        print item[1]
        print item[2], item[3]

except urllib2.URLError, e:
    if hasattr(e, 'code'):
        print e.code
    if hasattr(e, 'reason'):
        print e.reason
