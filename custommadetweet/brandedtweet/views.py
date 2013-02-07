from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from brandedtweet.models import BrandedTweet

def index(request):
    tweet_list = BrandedTweet.objects.all().order_by('-submit_date')
    paginator = Paginator(tweet_list, 10)
    
    page = request.GET.get('page')
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    
    c = {'tweet_list': tweets}
    if request.user.is_authenticated():
        c['user'] = request.user
        
    return render_to_response('brandedtweet/index.html', c)
