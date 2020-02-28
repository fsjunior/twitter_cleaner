import sys
import pandas as pd
import json
from datetime import datetime


class ArchiveFilter(object):
	def __init__(self, tweet_data: pd.DataFrame):
		self.tweet_data = tweet_data

	@classmethod
	def fromfile(cls, file: str):
		if file.endswith(".csv"):
			tweet_data = pd.read_csv(file)
		elif file.endswith(".js"):
			with open(file) as f:
				json_data = json.loads(f.read()[24:])
				tuple_data = [(i['tweet']['id'], i['tweet']['created_at']) for i in json_data]
				tweet_data = pd.DataFrame(tuple_data, columns=['tweet_id', 'timestamp'])
		else:
			print("Unsuported file extension.")
			sys.exit(1)

		# convert str to timestamp and set timezone to None to get naive timestamp
		tweet_data.timestamp = pd.to_datetime(tweet_data.timestamp).dt.tz_localize(None)
		return ArchiveFilter(tweet_data)

	def filter_older_than(self, older_than):
		return ArchiveFilter(self.tweet_data[self.tweet_data.timestamp < older_than])

	def filter_newer_than(self, newer_than):
		return ArchiveFilter(self.tweet_data[self.tweet_data.timestamp > newer_than])

	def get_tweet_id_data(self):
		return self.tweet_data.tweet_id
