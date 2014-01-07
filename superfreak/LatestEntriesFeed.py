#coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from models import Entry, RSS

class LatestEntriesByCategory(Feed):
    def get_object(self,request, beat_id):
        if len(beat_id) != 1:
            raise ObjectDoesNotExist
        return RSS.objects.filter(id=beat_id[0])[0]

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.url

    def description(self, obj):
        return obj.title

    def items(self, obj):
        entries = Entry.objects.filter(feedid=obj.id)
        return entries.order_by('-id')[:30]

    def item_link(self,item):
        return item.link

    def get_absolute_url(self,item):
        return item.link

class Weibo(Feed):
    title = '微三国2论坛'
    link = 'http://game.weibo.com/club/forum-315-1'
    description = '论坛专用订阅'

    def items(self, obj):
        entries = Entry.objects.filter(feedid=0)
        return entries.order_by('-id')[:30]
    def get_absolute_url(self,item):
        return item.link
    def item_link(self,item):
        return item.link