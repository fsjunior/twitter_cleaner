import sys
import pandas as pd
import json
from datetime import datetime


class ArchiveFilter(object):
	def __init__(self, file: str):

		if file.endswith(".csv"):
			self.tweet_data = pd.read_csv(file)
		elif file.endswith(".js"):
			with open(file) as f:
				json_data = json.loads(f.read()[24:])
				tuple_data = [(i['tweet']['id'], i['tweet']['created_at']) for i in json_data]
				self.tweet_data = pd.DataFrame(tuple_data, columns=['tweet_id', 'timestamp'])
		else:
			print("Unsuported file extension.")
			sys.exit(1)

		# convert str to timestamp and set timezone to None to get naive timestamp
		self.tweet_data.timestamp = pd.to_datetime(self.tweet_data.timestamp).dt.tz_localize(None)

	def filter(self, older_than):
		return self.tweet_data[self.tweet_data.timestamp < older_than].tweet_id

