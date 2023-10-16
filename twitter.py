import argparse
import csv
import json
import os
import random
import re
import time
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image
from wordcloud import STOPWORDS, ImageColorGenerator, WordCloud
from tweet_analysis import TwitterAnalysis

# All values stored here are constant, copy-pasted from the website
FEATURES_USER = '{"hidden_profile_likes_enabled":false,"hidden_profile_subscriptions_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":false,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}'
FEATURES_TWEETS = '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}'

AUTHORIZATION_TOKEN = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
HEADERS = {
        'authorization': 'Bearer %s' % AUTHORIZATION_TOKEN,
        # The Bearer value is a fixed value that is copy-pasted from the website
        # 'x-guest-token': None,
}

GET_USER_URL = 'https://twitter.com/i/api/graphql/SAMkL5y_N9pmahSw8yy6gw/UserByScreenName'
GET_TWEETS_URL = 'https://twitter.com/i/api/graphql/XicnWRbyQ3WgVY__VataBQ/UserTweets'
FIELDNAMES = ['id', 'tweet_url', 'name', 'user_id', 'username', 'published_at', 'content', 'views_count', 'retweet_count', 'likes', 'quote_count', 'reply_count', 'bookmarks_count', 'medias']

# SCrapping data from twitter
class TwitterScraper:

    def __init__(self):
        # We do initiate requests Session, and we get the `guest-token` from the HomePage
        resp = requests.get("https://twitter.com/")
        self.gt = resp.cookies.get_dict().get("gt") or "".join(re.findall(r'(?<=\"gt\=)[^;]+', resp.text))
        assert self.gt
        HEADERS['x-guest-token'] = getattr(self, 'gt')
        # assert self.guest_token
        self.HEADERS = HEADERS
        # assert username
        # self.username = username

    # GEt user details
    def get_user(self, username):
        # We recover the user_id required to go ahead
        arg = {"screen_name": username, "withSafetyModeUserFields": True}
        
        params = {
            'variables': json.dumps(arg),
            'features': FEATURES_USER,
        }

        response = requests.get(
            GET_USER_URL,
            params=params, 
            headers=self.HEADERS
        )

        try: 
            json_response = response.json()
        except requests.exceptions.JSONDecodeError: 
            print(response.status_code)
            print(response.text)
            raise

        result = json_response.get("data", {}).get("user", {}).get("result", {})
        legacy = result.get("legacy", {})

        return {
            "id": result.get("rest_id"), 
            "username": username, 
            "full_name": legacy.get("name")
        }

    def tweet_parser(self, username, user_id, full_name, tweet_id, item_result, legacy):

        # It's a static method to parse from a tweet
        medias = legacy.get("entities").get("media")
        medias = ", ".join(["%s (%s)" % (d.get("media_url_https"), d.get('type')) for d in legacy.get("entities").get("media")]) if medias else None

        return {
            "id": tweet_id,
            "tweet_url": f"https://twitter.com/{username}/status/{tweet_id}",
            "name": full_name,
            "user_id": user_id,
            "username": username,
            "published_at": legacy.get("created_at"),
            "content": legacy.get("full_text"),
            "views_count": item_result.get("views", {}).get("count"),
            "retweet_count": legacy.get("retweet_count"),
            "likes": legacy.get("favorite_count"),
            "quote_count": legacy.get("quote_count"),
            "reply_count": legacy.get("reply_count"),
            "bookmarks_count": legacy.get("bookmark_count"),
            "medias": medias
        }

    def iter_tweets(self, username, limit=120):
        # The main navigation method
        print(f"[+] scraping: {username}")
        _tweets = []
        _user = self.get_user(username)
        full_name = _user.get("full_name")
        user_id = _user.get("id")
        if not user_id:
            print("/!\\ error: no user id found")
            #raise NotImplementedError
            return _tweets
        cursor = None
        

        while True:
            var = {
                "userId": user_id, 
                "count": 100, 
                "cursor": cursor, 
                "includePromotedContent": True,
                "withQuickPromoteEligibilityTweetFields": True, 
                "withVoice": True,
                "withV2Timeline": True
            }

            params = {
                'variables': json.dumps(var),
                'features': FEATURES_TWEETS,
            }

            response = requests.get(
                GET_TWEETS_URL,
                params=params,
                headers=self.HEADERS,
            )

            json_response = response.json()

            result = json_response.get("data", {}).get("user", {}).get("result", {})
            timeline = result.get("timeline_v2", {}).get("timeline", {}).get("instructions", {})
            entries = [x.get("entries") for x in timeline if x.get("type") == "TimelineAddEntries"]
            entries = entries[0] if entries else []

            for entry in entries:
                content = entry.get("content")
                entry_type = content.get("entryType")
                tweet_id = entry.get("sortIndex")
                if entry_type == "TimelineTimelineItem":
                    item_result = content.get("itemContent", {}).get("tweet_results", {}).get("result", {})
                    legacy = item_result.get("legacy")

                    tweet_data = self.tweet_parser(username, user_id, full_name, tweet_id, item_result, legacy)
                    _tweets.append(tweet_data)

                if entry_type == "TimelineTimelineCursor" and content.get("cursorType") == "Bottom":
                    # NB: after 07/01 lock and unlock — no more cursor available if no login provided i.e. max. 100 tweets per username no more
                    cursor = content.get("value")


                if len(_tweets) >= limit:
                    # We do stop — once reached tweets limit provided by user
                    break

            print(f"[#] tweets scraped: {len(_tweets)}")


            if len(_tweets) >= limit or cursor is None or len(entries) == 2:
                break

        return _tweets

    def generate_csv(self, name, tweetlist=[], isUser = True):
        timestamp = int(datetime.datetime.now().timestamp())
        filename = '%s_%s.csv' % (name, timestamp)
        self.__create_dirs('output')
        completename = os.path.join('./output', filename)
        print('[+] writing %s' % filename)
        with open(completename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter='\t')
            writer.writeheader()

            if isUser:
                for tweet in tweetlist:
                    print(tweet['id'], tweet['published_at'])
                    writer.writerow(tweet)
            else:
                for tweets in tweetlist: 
                    for tweet in tweets:
                        print(tweet['id'], tweet['published_at'])
                        writer.writerow(tweet)
    
    # Create new folders
    def __create_dirs(self, root, subfolders=None):
        root = root if subfolders == None else f'{root}/{subfolders}/'
        if not os.path.exists(root):
            os.makedirs(f'{root}', exist_ok=True)
        
        return

# Main function
def main():
    os.system('clear')
    print('start\n')
    s = time.perf_counter()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-u', '--username', type=str, required=False, help='user to scrape tweets from')
    argparser.add_argument('-f', '--filename', type=str, required=False, help='filename contain user list to scrape tweets from')
    argparser.add_argument('-l', '--limit', type=int, required=False, help='max tweets to scrape', default=10)
    argparser.add_argument('-w', '--wordcloud', type=str, required=False, help='csv file for word cloud', default=10)

    args = argparser.parse_args()
    
    filename = str(args.filename).strip()
    username = str(args.username).strip()
    csvfile = str(args.wordcloud).strip()
    limit = args.limit

    assert all([username, limit])
    tweetlist = []

    if  args.filename:
        twitter_scraper = TwitterScraper()
        for line in open(filename, 'r'):
            handle = line.strip()
            time.sleep(random.randint(1, 5)) 
            tweets = twitter_scraper.iter_tweets(handle, limit=limit)   
            tweetlist.append(tweets)
        twitter_scraper.generate_csv(filename, tweetlist, isUser=False)
        print('elapsed %s' % (time.perf_counter()-s))
        print('\nTweet scrap successfully from {} file!'.format(filename))

    elif args.username: 
        twitter_scraper = TwitterScraper()
        tweets = twitter_scraper.iter_tweets(username, limit=limit)   
        if tweets:
            tweetlist.append(tweets)
            assert tweets
            twitter_scraper.generate_csv(username, tweets, isUser=True)
            print('elapsed %s' % (time.perf_counter()-s))
            print('\n{} Tweet scrap successfully done!'.format(username))

    elif args.wordcloud:
        analysis = TwitterAnalysis()
        analysis.read_data("./output/" + csvfile)
    
    elif args.version:
        print("\nPython Tool: Twitter data analysis\nby: alien.c00de ver:1.0.0\n")

    else:
        print("usage: python twitter.py [--username @twiitername] [--filename userinfo.txt] [--wordcount data.csv] [--limit 10] [-V]")

if __name__ == '__main__':
    main()