from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required,user_passes_test

from brandedtweet.models import BrandedTweet
from brandedtweet.utils.auth_helper import *

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
@user_passes_test(is_editor)
def editor_view(request):
    return render_to_response('brandedtweet/editor.html')

@login_required(login_url='/login/')
@user_passes_test(is_editor)
def blocked_tweets_view(request):
    tweets = paginated_tweets(request, is_dirty=True)

    c = {'tweet_list': tweets, 'is_dirty': True, 'type_tweets': 'Blocked'}
    if request.user.is_authenticated():
        c['user'] = request.user
        
    return render_to_response('brandedtweet/list.html', c)


@login_required(login_url='/login/')
@user_passes_test(is_editor)
def published_tweets_view(request):
    tweets = paginated_tweets(request, is_dirty=False)

    c = {'tweet_list': tweets, 'is_dirty': False, 'type_tweets': 'Published'}
    if request.user.is_authenticated():
        c['user'] = request.user

    return render_to_response('brandedtweet/list.html', c)

@user_passes_test(is_editor)
def paginated_tweets(request, tweets_per_page=10, is_dirty=False):
    tweet_list = BrandedTweet.objects.filter(is_dirty=is_dirty).order_by('-submit_date')
    paginator = Paginator(tweet_list, tweets_per_page)
    
    page = request.GET.get('page')
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    
    return tweets
    
@login_required(login_url='/login/')
@user_passes_test(is_staff)
def staff_view(request):
    return HttpResponse("Hello staff")