#coding=utf-8
# Create your views here.
from BeautifulSoup import *
from django.http import HttpResponse
from django.utils import simplejson
from models import RSS,Entry,Check
from sae.mail import send_mail
import chardet
import re
import sys
import time
import urllib
import urllib2
import weiboLogin

reload(sys)
sys.setdefaultencoding( "utf-8" )

def hello(request):
    return HttpResponse("Hello world")
def syncWeibo(request):

    WBLogin = weiboLogin.weiboLogin()
    if WBLogin.login('idrinkmilkeveryday@gmail.com','1234qwer')==1:
        urlContent = urllib2.urlopen('http://game.weibo.com/club/forum-315-1').read()
        soup = BeautifulSoup(urlContent)
        ul = soup.find('ul',{'class':'top_topics'})
        lis = ul.findAll('li',{'class':''})

        for li in lis:
            item = {
            'user':li.find('div',{'class':'col1'}).find('img')['alt'],
            'link':li.find('div',{'class':'no_rep_line'}).findAll('a')[1]['href'],
            'tag':li.find('a',{'class':'navy_tag'}).string,
            'title':li.find('div',{'class':'no_rep_line'}).findAll('a')[1].string,
            'time':li.find('div',{'class':'col2'}).find('span').string
            }
            title = "[%s][%s]%s%s"%(item['time'],item['user'],item['tag'],item['title'])
            link = item['link']
            result = Entry.objects.filter(title=title)
            if len(result) == 0:
                entry = Entry(title=title,link=link,content='',feedid=0)
                entry.save()
                send_mail("huangdi@9173.com", title, link,
          ("smtp.163.com", 25, "weisanguo2mail@163.com", "1234qwer", False))
                pass                
            pass

        return HttpResponse("Login success!") 
    else:
        return HttpResponse("Login error!") 
    pass
def syncFeed(request):
    feedList = RSS.objects.all();
    for feedobj in feedList:
        targetURL = feedobj.url
        urlContent = urllib.urlopen(targetURL).read();

        feed = {
        'id':feedobj.id,
        'title':feedobj.title,
        'global_search_pattern':feedobj.global_search_pattern,
        'item_search_pattern':feedobj.item_search_pattern,
        'item_title':feedobj.item_title,
        'item_link':feedobj.item_link,
        'item_content':feedobj.item_content,
        'encoding':feedobj.encoding,
        'mail_address':feedobj.mail_address
        }
       
        generateFeedEntry(urlContent,feed)
    mytime = time.strftime('%m-%d %X',time.localtime(time.time()))
    check = Check(time=mytime)
    check.save()
    return HttpResponse("Success")
def getURLContent(request,url):
    urlContent = urllib2.urlopen(url).read()
    encoding = chardet.detect(urlContent)['encoding']
    urlContent = urlContent.decode(encoding).encode("utf-8")
    # result = {
    #     "content":urlContent,
    #     "encoding":encoding 
    # }
    # return HttpResponse(simplejson.dumps( result ))
    return HttpResponse(urlContent)

def checkCron(request):
    mytime = time.strftime('%m-%d %X',time.localtime(time.time()))
    pass
    return HttpResponse('checkCron!!!!')
def generateFeedEntry(urlContent,feed):
    encodeType = feed['encoding']
    urlContent = urlContent.decode(encodeType).encode('utf-8')
    global_pattern = re.compile(feed['global_search_pattern'].replace('{%}','(.*?)').replace('{*}','.*?'),re.I|re.S|re.M)
    item_pattern = re.compile(feed['item_search_pattern'].replace('{%}','(.*?)').replace('{*}','.*?'),re.I|re.S|re.M)
    sub_pattern = re.compile(r'{%(.*?)}',re.I|re.S|re.M)
    globalMatch = global_pattern.search(urlContent)
    globalContent = globalMatch.group()
    globalContent = globalContent[0:len(globalContent)/4]
    itemList = item_pattern.findall(globalContent)
    print len(itemList)
    for i in xrange(len(itemList)-1,-1,-1):
        item = itemList[i]
        link = feed['item_link']
        title = feed['item_title']
        content = feed['item_content']
        link = sub_pattern.sub(lambda m: str(item[int(m.group(1))-1]),link)
        content = sub_pattern.sub(lambda m: str(item[int(m.group(1))-1]),content)
        title = sub_pattern.sub(lambda m: str(item[int(m.group(1))-1]),title)
        result = Entry.objects.filter(title=title)
        if len(result) == 0:
            entry = Entry(title=title,link=link,content=content,feedid=feed['id'])
            entry.save()
            if feed['mail_address']!='':
                send_mail(feed['mail_address'], title, link,
          ("smtp.163.com", 25, "weisanguo2mail@163.com", "1234qwer", False))
            pass                
        pass
    pass

def extractFeedEntry(request):

    global_pattern = request.POST.get("global_pattern");
    item_pattern = request.POST.get("item_pattern");
    urlContent = request.POST.get("urlContent");


    global_pattern = re.compile(global_pattern.replace('{%}','(.*?)').replace('{*}','.*?'),re.I|re.S|re.M)
    item_pattern = re.compile(item_pattern.replace('{%}','(.*?)').replace('{*}','.*?'),re.I|re.S|re.M)
  
    globalMatch = global_pattern.search(urlContent)
    globalContent = globalMatch.group()
    itemList = item_pattern.findall(globalContent)
    print len(itemList)
    json = simplejson.dumps( itemList )
    return HttpResponse(json)
def insertRSS(request):
    #     title = models.CharField(max_length = 100)
    # url = models.CharField(max_length=300)
    # encoding = models.CharField(max_length=10)
    # global_search_pattern = models.CharField(max_length=100)
    # item_search_pattern = models.CharField(max_length=100)
    # item_title = models.CharField(max_length=100)
    # item_link = models.CharField(max_length=100)
    # item_content = models.CharField(max_length=300)

    # item_title = request.POST.get("itemTitle");
    # item_link = request.POST.get("itemLink");
    # item_content = request.POST.get("itemContent");
    return HttpResponse("")