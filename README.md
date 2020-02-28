# Twitter Cleaner

A small python script that allows you to delete your old tweets. 

## Installation

Just clone this repo and install the requirements.txt packages. Python3 is required.

```bash
git clone https://github.com/fsjunior/twitter_cleaner.git
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## How to use

1. [Apply for a Twitter Developer Account](https://developer.twitter.com/en/apply).
2. While you wait for Twitter to review and approve your Developer Account, [download your Twitter archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive). Twitter limits the access of the tweets by the API, so the only way to retrieve your old tweets is using the Twitter archive. 
3. When you receive your archive, you should look for a JS file with contains all your tweets (tweet.js).
4. After the approval of your Twitter Developer Account, [create an app](https://developer.twitter.com/en/apps). 
**Don't forget**: you should set **Read and Write** in the *Access Permissions* settings.
5. Open the *details* page of the app that you created. Go for the *Keys and Tokens* tab. You will need the consumer and access token keys to use Twitter Cleaner.
6. Run: 

``` bash
python main.py --consumer_key <consumer-key> \\
       --consumer_secret <consumer-secret>   \\
       --access_token_key <access-token-key> \\
       --access_token_secret <access-token-secret> \\
       --older_than <date in YYYY-MM-DD format> \\
       --file <path/to/tweet.js>
```


### Filters


There are two filters available: filter tweets older than a date AND filter tweets newer than a date. If you need more filtering options, like filter tweets with less (or more) than a specific amount of engagement, please ask.
 
