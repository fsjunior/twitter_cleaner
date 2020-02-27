import sys
from twitter_cleaner.app import App
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitter Cleaner (delete old tweets).')
    parser.add_argument('--consumer_key', help='Consumer Key', required=True)
    parser.add_argument('--consumer_secret', help='Consumer Secret', required=True)
    parser.add_argument('--access_token_key', help='Access Token Key', required=True)
    parser.add_argument('--access_token_secret', help='Access Token Secret', required=True)

    parser.add_argument('--older_than', help='Delete tweets older than (YYYY-MM-DD format)', required=True)
    parser.add_argument('--file', help='csv twitter archive file', required=True)
    args = parser.parse_args()

    app = App(args)

    sys.exit(app.run())