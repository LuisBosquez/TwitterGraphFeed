# Azure Cosmos DB Gremlin API + Twitter API: Tweet and Hashtag aggregator

## What does it do? 
This application reads a Twitter stream based on the provided hashtags, configured under `config.py`. Then it creates a graph structure with unique Hashtag vertices that point to all the tweets that contain them.

## How do I run it?
1. First [create a Cosmos DB graph account](https://docs.microsoft.com/en-us/azure/cosmos-db/create-graph-python).
2. Create a [Twitter API account](http://apps.twitter.com/). You will be provided with a *consumer key*, *consumer secret*, *access token* and *access token secret*.
3. Install all the required packages using [pip](https://pip.pypa.io/en/stable/reference/pip_download/).
    ```
    pip install -r requirements.txt
    ```

4. Replace your configuration variables in `config.py` using the values from your Cosmos DB and Twitter API accounts.
5. Run the `driver.py` file.
    ```
    python .\driver.py
    ```

We use [Tweepy](http://tweepy.readthedocs.org/)'s Python-based client to access Twitter's service.

To extend the functionality, you can modify the `graphListener.py` file to parse the tweets and create custom graph objects using [the Gremlin language](https://docs.microsoft.com/en-us/azure/cosmos-db/tutorial-query-graph). A sample response from the Tweepy stream can be found under `./data/sample.json`.

