import tweepy
from . import archivefilter
from datetime import datetime
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import logging


class App(object):
    def __init__(self, args):
        self.args = args

        print("Logging to output.log.")
        logging.basicConfig(filename="output.log", level=logging.INFO)

        print("Opening file...")
        self.ar = archivefilter.ArchiveFilter.fromfile(args.file)

    def _delete_tweet(self, tweet_id, progress_bar):
        progress_bar.update()
        try:
            auth = tweepy.OAuthHandler(self.args.consumer_key, self.args.consumer_secret)
            auth.set_access_token(self.args.access_token_key, self.args.access_token_secret)
            logging.info("Tweet with id {} already deleted, skipping.".format(tweet_id))
            self.api = tweepy.API(auth)
            self.api.destroy_status(id=tweet_id)
        except tweepy.error.TweepError as e:
            if e.api_code == 144:
                logging.info("Tweet with id {} already deleted, skipping.".format(tweet_id))
            elif e.api_code in [88, 185]:
                logging.warning("Rate limit reached. Waiting for 5 minutes until trying again...")
                for _ in tqdm(range(60)):
                    time.sleep(1)
            else:
                logging.warning("Tweet with id {} unavailable (error {}), skipping.".format(tweet_id, str(e)))

    def run(self):
        print("Filtering tweets...")
        older_filter = datetime.strptime(self.args.older_than, "%Y-%m-%d")
        filtered_ar = self.ar.filter_older_than(older_filter)
        if self.args.newer_than:
            newer_filter = datetime.strptime(self.args.newer_than, "%Y-%m-%d")
            filtered_ar = filtered_ar.filter_newer_than(newer_filter)

        list_of_ids = filtered_ar.get_tweet_id_data()

        print("{} matched tweets!".format(len(list_of_ids)))

        print("The process will continue in 10 seconds. Hit CTRL+C if you want to stop...")
        time.sleep(10)
        print("Cleaning tweets... This operation will take some time.")

        with ThreadPoolExecutor(max_workers=self.args.workers) as executor:
            print("Using {} workers to access the Twitter API".format(self.args.workers))
            progress_bar = tqdm(total=len(list_of_ids))
            for tweet_id in list_of_ids:
                executor.submit(self._delete_tweet, tweet_id, progress_bar)

            executor.shutdown(wait=True)
            progress_bar.close()

        print("Finished!")
        return 0
