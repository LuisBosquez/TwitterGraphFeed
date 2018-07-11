from tweepy.streaming import StreamListener
from config import *
import json, sys, traceback

class CosmosDBGraphListener(StreamListener):
    count_objects = 0
    def __init__(self, client):
        self.client = client

    # Create a vertex for every tweet
    def create_tweet_vertex(self, tweet):
        # Construct Gremlin query with parameters. ID, lang and Twitter handles can't have special characters.
        query = "g.addV('tweet').property('id', '{0}').property('text', '{1}').property('lang', '{2}').property('handle', '{3}')".format(
            tweet["id_str"],
            tweet["text"].replace("'", r"\'"),
            tweet["lang"],
            tweet["user"]["screen_name"]
        )

        callback = self.client.submitAsync(query)

        if callback.result() is not None:
            self.count_objects += 1
            return True
        else:
            print("Something went wrong with this query: {0}".format(query))
            return False
    
    # Create a unique vertex for every hashtag
    def create_hashtag_vertex(self, hashtag_id, tweet_id):
        # Sanitize hashtag text
        hashtag_id = hashtag_id.lower()

        # Insert if doesn't exist using Gremlin coalesce
        query = "g.inject(0).coalesce(__.V('{0}'), addV('hashtag').property('id', '{0}'))".format(
            hashtag_id
        )

        callback = self.client.submitAsync(query)

        if callback.result() is not None:
            self.count_objects += 1
            return True
        else:
            print("Something went wrong with this query: {0}".format(query))
            return False

    # Create edge between Tweet and Hashtag vertices.
    def create_hashtag_tweet_edge(self, hashtag_id, tweet_id):
        # Create edge in Gremlin
        query = "g.V('{0}').addE('uses_hashtag').to(g.V('{1}'))".format(
            tweet_id,
            hashtag_id
        )

        callback = self.client.submitAsync(query)

        if callback.result() is not None:
            self.count_objects += 1
            return True
        else:
            print("Something went wrong with this query: {0}".format(query))
            return False

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            result = self.create_tweet_vertex(tweet)

            if len(tweet["entities"]["hashtags"]) > 0 and result is not False:
                for hashtag in tweet["entities"]["hashtags"]:
                    result = self.create_hashtag_vertex(hashtag["text"], tweet["id_str"])
                    if result is not None:
                        result = self.create_hashtag_tweet_edge(hashtag["text"], tweet["id_str"])

            print("Inserted graph objects: {0}".format(self.count_objects))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True