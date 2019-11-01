import GetOldTweets3 as got
import pandas as pd
import numpy as np
from datetime import datetime
import argparse, os, re

# Start CLI work 
parser = argparse.ArgumentParser()
parser.add_argument("--users", help="twitter user handles to grab tweets from, comma-separated", default="")
parser.add_argument("--limit", help="limit of tweets to scrape, reduces runtime", default=100000)
parser.add_argument("--gen", help="specify number of tweets to generate", default=10)
args = parser.parse_args()

if not args.users:
	raise Exception("Specify user to create Markov chain from")

tweets_df = pd.DataFrame([])
usernames = args.users.split(",")
for user in usernames:

	# Check if tweets have already been downloaded today
	timestamp = datetime.today().strftime('%Y-%m-%d')
	if os.path.exists(user+timestamp+".csv"):
		tweets = pd.read_csv(user+timestamp+".csv", index_col=False)
	else:
		tweetCriteria = got.manager.TweetCriteria().setUsername(user)\
												   .setMaxTweets(args.limit)
		tweets = pd.DataFrame([tweet.text for tweet in got.manager.TweetManager.getTweets(tweetCriteria)])

		if tweets.empty:
			raise Exception("Twitter user must exist and have tweets that aren't links: {}".format(user))

		# Output tweets to csv following convention username_YYYY-MM-DD.csv
		tweets.to_csv(user+timestamp+".csv", index=False)

	# Append tweet texts to master dataframe of tweet texts
	tweets_df = tweets_df.append(tweets, sort=False)

# Calculate probabilites
GEN_SPACE_SYMBOLS = re.compile(r"[,“”\"-_.?!]")
GEN_BLANK_SYMBOLS = re.compile(r"['()`]")

lookup = {}
for idx, row in tweets_df.iterrows():
	linkless_tweet = re.sub(r"http[s]?://\S+", "", row[0])
	linkless_tweet = re.sub(r"pic.twitter.com\S+", "", linkless_tweet)
	linkless_tweet = re.sub(r"@\S+", "", linkless_tweet)
	tweet = re.sub(GEN_SPACE_SYMBOLS, ' ', re.sub(GEN_BLANK_SYMBOLS, '', linkless_tweet.lower())).strip()	
	words = re.split(r'\s+', tweet)

	# Thanks David
	for i in range(len(words)):
		key = words[i]
		if i == len(words) - 1:
			if key in lookup:
				lookup[key]['TOTAL'] += 1
				lookup[key]['TERM'] = lookup[key].get('TERM', 0) + 1.0
			else:
				lookup[key] = {'TERM': 1.0, 'TOTAL': 1}
		else:
			nxt = words[i + 1]
			if key in lookup:
				lookup[key]['TOTAL'] += 1
				lookup[key][nxt] = lookup[key].get(nxt, 0) + 1.0
			else:
				lookup[key] = {nxt: 1.0, 'TOTAL': 1}

for word in lookup:
	total = lookup[word]['TOTAL']
	del lookup[word]['TOTAL']
	for option in lookup[word]:
		lookup[word][option] = lookup[word][option] / total

# Generate new tweet
for j in range(int(args.gen)):
	seed = np.random.choice(list(lookup.keys()))
	longest_sentence = []
	retries = 0

	while len(longest_sentence) < 1 and retries < 200:
		current_word = seed
		sentence = [current_word]

		while True:
			choices = [(w, lookup[current_word][w]) for w in lookup[current_word]]
			c_words, p_dist = zip(*choices)

			old_word = current_word
			current_word = np.random.choice(c_words, p=p_dist)

			while current_word == 'TERM' and len(sentence) < 1 and len(lookup[old_word].keys()) > 1:
				current_word = np.random.choice(c_words, p=p_dist)
			while len(sentence) >= 3 and (current_word == sentence[-1] == sentence[-2] == sentence[-3]):
				current_word = np.random.choice(c_words, p=p_dist)

			if current_word == 'TERM' or len(sentence) >= 1000:
				break
			sentence.append(current_word)

		if len(longest_sentence) < len(sentence) and len(' '.join(sentence)) <= 2000:
			longest_sentence = sentence[:]
	
		retries += 1

	print(str(j)+ ": " + ' '.join(longest_sentence))
