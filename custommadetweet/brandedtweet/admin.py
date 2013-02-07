from brandedtweet.models import BrandedTweet
from django.contrib import admin

class BrandedTweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['content','user']}),
        ('Date Information',    {'fields': ['publish_date','submit_date']}),
    ]
    
    list_display = ('content','user','publish_date','submit_date')
    search_fields = ['content','user']


admin.site.register(BrandedTweet, BrandedTweetAdmin)