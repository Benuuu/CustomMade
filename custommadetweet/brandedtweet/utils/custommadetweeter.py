import twitter

api = twitter.Api(consumer_key='42rvRjeCaw7Rz2JLKe8VCA',
                consumer_secret='pwUR9LJZv9tKVtnRgBaBobGb8ArMZA9w9mkGQwDMu4',
                access_token_key='1152327174-m7ezmuH6rxJu3SqLT64k1W8GUIYUYTK0NtAFXzF',
                access_token_secret='biuUDoTh6Zpr5uZrKIH5crHtPxuQH3t3qvI0muvK4')

def send_tweet(content):
    return api.PostUpdate(content).id
    
def get_tweets():
    return api.GetUserTimeline()

def get_retweet_count(twit):
    return api.GetStatus(twit).GetRetweetCount()