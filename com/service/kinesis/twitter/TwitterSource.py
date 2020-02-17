from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boto3
import json

#CONSTANTS
CONSUMER_KEY = '0gFJpitshfdNVG3tO8b9tJQtv'
CONSUMER_SECRET = 'gebAwM8gKTZ9ydXIfaeoHOdRbSxmAU5PpcqAuCStXRfKH2XseL'
ACCESS_TOKEN = '145640128-wDBnlhLdyXVhBKmFdPnao7cwCS6QMK9cRlxQzltI'
ACCESS_TOKEN_SECRET = 'F26FzI2gTXFqoSSrAVoYrLh6awDWVD6tXo7fDwPXM5A95'
partition_key='twitter-stream'
kinesisClient = boto3.client('kinesis', region_name='us-east-1')



class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            jsonData = json.loads(data)
            print(jsonData['text'])
            put_response = kinesisClient.put_record(StreamName='amazon-trainings-umartahir-twitter',
                                                    Data=json.dumps(jsonData['text']), PartitionKey=partition_key)
            print("Records have been put to stream")
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


class Twitter():
    def stream_tweets(self, hash_tag_list):
        listener = StdOutListener()
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)  # https://github.com/psf/requests/issues/3883
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


if __name__ == '__main__':
    hash_tag_list = ["#PakistanNeedsPMLN", "#coronavirusoutbreak"]
    twitter = Twitter()
    twitter.stream_tweets(hash_tag_list)
