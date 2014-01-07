#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings
from LatestEntriesFeed import LatestEntriesByCategory,Weibo
from views import syncFeed,syncWeibo,checkCron,getURLContent,extractFeedEntry
from views import hello

# urlpatterns = patterns('',
#     ('^syncFeed/$', hello),
# )

feeds = {
    'categories': LatestEntriesByCategory
}
urlpatterns = patterns('',
        (r'^feeds/(?P<beat_id>.*)/$', LatestEntriesByCategory()),
        (r'^weibofeeds/$', Weibo()),
        # (r'^feeds/(.*?)/$', LatestEntriesByCategory()),
        (r'^syncFeed/$', syncFeed),
        (r'^syncWeibo/$', syncWeibo),
        (r'^checkCron/$', checkCron),
        (r'^extractFeedEntry/$', extractFeedEntry),
        (r'^hello/$', hello),
        (r'^getURLContent/(.*)$', getURLContent),
        # (r'^site_file/(?P<path>.*)$','django.views.static.serve',
        # {'document_root':settings.STATICFILES_DIRS, 'show_indexes': True})
        (r'^site_file/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.STATICFILES_DIRS, 'show_indexes': True})
        )