from brandedtweet.models import BrandedTweet
import django_tables2 as tables

class BrandedTweetTable(tables.Table):
    content = tables.Column()
    class Meta:
        model = BrandedTweet
