import GetOldTweets3 as got
import pandas as pd
from datetime import datetime
import argparse, os


parser = argparse.ArgumentParser()
parser.add_argument("--users", help="twitter user handles to grab tweets from, comma-separated", default="")
parser.add_argument("--limit", help="limit of tweets to scrape, reduces runtime", default=100000)
args = parser.parse_args()

usernames = args.users.split(",")
for user in usernames:

	# Check if tweets have already been downloaded today
	timestamp = datetime.today().strftime('%Y-%m-%d')
	if os.path.exists(user+timestamp+".csv"):
		df = pd.read_csv(user+timestamp+".csv")
		print(df)
	else:
		tweetCriteria = got.manager.TweetCriteria().setUsername(user)\
												   .setMaxTweets(args.limit)
		tweets = pd.DataFrame(got.manager.TweetManager.getTweets(tweetCriteria))

		if not tweets:
			raise Exception("Twitter user must exist: {}".format(user))

		# Output tweets to csv following convention username_YYYY-mm-DD.csv
		tweets.to_csv(user+timestamp+".csv")
