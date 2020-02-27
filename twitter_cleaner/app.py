import tweepy
from . import archivefilter
from datetime import datetime
import time
from tqdm import tqdm




class App:
    def __init__(self, args):
        auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
        auth.set_access_token(args.access_token_key, args.access_token_secret)

        self.api = tweepy.API(auth)

        self.ar = archivefilter.ArchiveFilter(args.file)
        self.args = args

    def run(self):
        timestamp_filter = datetime.strptime(self.args.older_than, "%Y-%m-%d")

        print("Filtering tweets...")

        list_of_ids = self.ar.filter_by_timestamp(timestamp_filter)

        print("Tweets that matches the date filter: {}".format(len(list_of_ids)))

        print("Deleting tweets...")
        for id in tqdm(list_of_ids):
            try:
                self.api.destroy_status(id=id)
            except tweepy.error.TweepError as e:
                if e.api_code == 144:
                    print("Tweet with id {} already deleted, skipping.".format(id))
                elif e.api_code in [88, 185]:
                    print("Rate limit reached. Waiting for 5 minutes until trying again...")
                    for _ in tqdm(range(60)):
                        time.sleep(1)
                else:
                    print("Unknown error. Exiting.")
                    print(e)




