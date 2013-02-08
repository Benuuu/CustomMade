from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from django.core.context_processors import csrf

from brandedtweet.models import BrandedTweet
from brandedtweet.forms import BrandedTweetForm
from brandedtweet.utils.auth_helper import *
from brandedtweet.utils.custommadefilter import *
from brandedtweet.utils.custommadetweeter import *

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
    cmf = CustomMadeFilter()
    c = {}
    c.update(csrf(request))
    
    if request.method == 'POST':
        form = BrandedTweetForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data['content']
            
            # Dirty Tweets shouldn't be sent but saved for the editors to view
            if cmf.contains_dirty(content):
                bt = BrandedTweet(content=content, submit_date=timezone.now(),
                                  user=request.user, is_dirty=True)
                bt.save()
                return HttpResponse('Shame on you')
            
            # Content that doesn't need brand correcting can be tweeted
            new_content = cmf.brand_correct_text(content)
            if new_content == content:
                tweet_id = send_tweet(new_content)
                bt = BrandedTweet(content=new_content, submit_date=timezone.now(),
                                  user=request.user, publish_date=timezone.now(),
                                  twitter_id=tweet_id)
                bt.save()
                return HttpResponse('Good stuff')

            # Content that needs brand correcting should be sent back to the staff for validation
            form = BrandedTweetForm({'content':new_content})
    
    else:
        form = BrandedTweetForm()
    
    c['form'] = form
    return render_to_response('brandedtweet/create_tweet.html', c)


















