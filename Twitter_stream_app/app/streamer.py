from slistener import SListener
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from urllib3.exceptions import ProtocolError
import os

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token= os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# set up the API with the authentication handler
api = API(auth)

#Tweets from new york city
LOCATIONS = [-74,40,-73,41]

# instantiate the SListener object
listen = SListener(api)

# instantiate the stream object
stream = Stream(auth, listen)

# # create a engine to the database
engine = create_engine("sqlite:///test.db")
# # if the database does not exist
if not database_exists(engine.url):
#   create a new database
    create_database(engine.url)

# begin collecting data
while True:
    # maintian connection unless interrupted
    try:
        stream.filter(locations=LOCATIONS)
    except (ProtocolError, AttributeError):
        continue