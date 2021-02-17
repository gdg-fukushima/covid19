import os
import json
import base64
import twitter
import requests


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.environ.get('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        pubsub_dict = json.loads(pubsub_message)
        status = pubsub_dict['status'] if 'status' in pubsub_dict else None
        media = pubsub_dict['media'] if 'media' in pubsub_dict else None
        api.PostUpdate(status, media)
    except Exception as e:
        print(e)
