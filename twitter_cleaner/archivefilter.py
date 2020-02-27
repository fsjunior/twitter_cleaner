import pandas as pd
from datetime import datetime


class ArchiveFilter:
	def __init__(self, file):
		self.tweet_data = pd.read_csv(file)

		# convert str to timestamp
		self.tweet_data.timestamp = pd.to_datetime(self.tweet_data.timestamp).dt.tz_localize(None)

	def filter_by_timestamp(self, older_than):
		return self.tweet_data[self.tweet_data.timestamp < older_than].tweet_id

