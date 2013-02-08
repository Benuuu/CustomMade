from django.contrib.auth.models import User
from django.db import models

class BrandedTweet(models.Model):
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True,blank=True)
    submit_date = models.DateTimeField()
    user = models.ForeignKey(User)
    twitter_id = models.IntegerField(null=True,blank=True)
    is_dirty = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content

