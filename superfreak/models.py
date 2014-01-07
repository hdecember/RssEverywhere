#coding=utf-8
from django.db import models

class RSS(models.Model):
    title = models.CharField(max_length = 100)
    url = models.CharField(max_length=300)
    encoding = models.CharField(max_length=10)
    global_search_pattern = models.CharField(max_length=200)
    item_search_pattern = models.CharField(max_length=500)
    item_title = models.CharField(max_length=300)
    item_link = models.CharField(max_length=800)
    item_content = models.CharField(max_length=300)
    mail_address = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.url

class Entry(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    content = models.CharField(max_length=300)
    feedid = models.IntegerField()
    def __unicode__(self):
        return self.title
class Check(models.Model):
    time = models.CharField(max_length=16)