from django.conf.urls import patterns, include, url

urlpatterns = patterns('brandedtweet.views',
    url(r'^$', 'index'),
)
