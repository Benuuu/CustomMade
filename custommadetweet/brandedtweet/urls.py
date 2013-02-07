from django.conf.urls import patterns, include, url

urlpatterns = patterns('brandedtweet.views',
    url(r'^$', 'index'),
    url(r'^editor/$', 'editor_view', name='editor_view'),
    url(r'^editor/blocked$', 'blocked_tweets_view', name='blocked_tweets_view'),
    url(r'^editor/published$', 'published_tweets_view', name='published_tweets_view'),
    url(r'^staff/$', 'staff_view'),
)
