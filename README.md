# Twitter Markov Chains
Feed in your favourite Twitter users as arguments and create a Markov chain to generate
new tweets in their same styles. If more than one user is specified, the results will
combine both Twitter users' tweets.

## Install
`git clone https://github.com/mjip/twitter-markov-chain && cd twitter-markov-chain`

## Requirements
Uses Python3.6. Install package requirements with `pip install -r requirements.txt`.
Does not need a Twitter development account or authentication keys.
Required packages:
- GetOldTweets3
- numpy
- pandas

## Usage
Running `python markovchain.py -h` gives the commandline arguments you can use:
```bash
usage: markovchain.py [-h] [--users USERS] [--limit LIMIT] [--gen GEN]

optional arguments:
  -h, --help     show this help message and exit
  --users USERS  twitter user handles to grab tweets from, comma-separated
  --limit LIMIT  limit of tweets to scrape, reduces runtime
  --gen GEN      specify number of tweets to generate
```
`--users` must be specified to create the Markov chain from. By default, when preprocessing 
tweet texts all links and twitter photo URLs are removed. The specified user(s) must have
tweets that don't contain just links or photos or the output will only generate blank lines. 

`--limit` specifies how many tweets to scrape off the specified user(s)'(s) profile(s). 
After running the first time, it will save the user(s) tweets in a csv file to reduce 
runtime, but the first execution can take significant time. Setting the `--limit` will 
reduce this initial cost. By default, `limit=100000`.

`--gen` specifies how many new tweets to generate. This is set to 10 by default, but can be 
changed as preferred.
