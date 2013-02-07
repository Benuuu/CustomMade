from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'custommadetweet.views.index'),
    url(r'^login/$', 'custommadetweet.views.login_view'),
    url(r'^auth/$', 'custommadetweet.views.auth_and_login'),
    
    url(r'^tweets/', include('brandedtweet.urls')),    

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
