import tweepy
from tweepy import OAuthHandler
from config import *
from tweepy import Stream
from gremlin_python.driver import client, serializer
from graphListener import CosmosDBGraphListener


import datetime

if __name__ == '__main__':
    # Initialize tweepy connection and auth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # Initialize Cosmos DB Gremlin client
    client = client.Client(
        'wss://{0}:443/'.format(graphHost),'g', 
        username="/dbs/{0}/colls/{1}".format(databaseId, collectionId), 
        password=masterKey,
        message_serializer=serializer.GraphSONSerializersV2d0()
    )

    print("Starting stream")
    twitter_stream = Stream(auth, CosmosDBGraphListener(client))
    twitter_stream.filter(track=hashtags, async=True)