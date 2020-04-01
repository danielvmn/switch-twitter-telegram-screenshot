import tweepy
from decouple import config
from telegram import Bot

# Twitter authentication
twitter_api_key = config('twitter_api_key')
twitter_api_secret_key = config('twitter_api_secret_key')
twitter_access_token = config('twitter_access_token')
twitter_access_token_secret = config('twitter_access_token_secret')
twitter_filter = config('twitter_filter')

# Telegram authentication
telegram_api_token = config('telegram_api_token')
telegram_group = config('telegram_group')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, tweet):
        try:
            print ('Receiving tweet: ' + tweet.text)
            if 'media' in tweet.entities:
                if 'video' in tweet.extended_entities['media'][0]['type']:
                    print('Saving Video')
                    vid = tweet.extended_entities['media'][0]['video_info']['variants'][1]['url']
                    bot.send_video(chat_id=telegram_group, video=vid)
                else:
                    print('Saving Image')
                    img = tweet.entities['media'][0]['media_url_https']
                    bot.send_photo(chat_id=telegram_group, photo=f'{img}:large')
            else:
                print("Tweet doesn't contain an image")
        except Exception as e:
            print(e)

# Telegram bot startup
bot = Bot(token=telegram_api_token)

# Twitter stream startup
auth = tweepy.auth.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
stream = tweepy.Stream(auth, MyStreamListener(), timeout=None)
# Twitter account to filter
stream.filter(follow=[twitter_filter])
