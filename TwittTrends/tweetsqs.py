import boto3
import geocoder
from geocoder import location
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import time
import json


con_key = "j6vAL8V7bVU72dVHX9DgFfUQt"
con_secret = "ZKOYpM2vbetPaxNckdVl5dVZug9jeO9HJ1Mh23VOGvEldWQ0aF"
acess_token = "114146024-GkTsqVFirnoIuY18WrAhbBt1ibkVSqvHuGT3Hnqw"
acess_secret = "DloDTQ80ABWdQS2SJfWMqgDwTrWSWrWZC2FS15EsQ7ocU"

sqs = boto3.resource('sqs', region_name="us-east-2")

#queue = sqs.create_queue(QueueName ='harsh-test-new', Attributes={'DelaySeconds':'5'})
q = sqs.get_queue_by_name(QueueName='harsh-test')
print (q.url)
print(q.attributes.get('DelaySeconds'))



class listener(StreamListener):
    def on_data(self, raw_data):
        print(raw_data)
        all_data = json.loads(raw_data)
        loc_en = all_data["user"]["geo_enabled"]
        lang = all_data["user"]["lang"]

        if 'text' in all_data and loc_en and lang == "en":
            tweets = all_data["retweeted_status"]["text"]

            username = all_data["user"]["screen_name"]
            location = all_data["user"]["location"]

            response = q.send_message(MessageBody=tweets,
                                      MessageAttributes={
                                          'language': {
                                              'DataType': 'String',
                                              'StringValue': lang
                                          },
                                          'location': {
                                              'DataType': 'Number',
                                              'StringValue': location
                                          },
                                      })



    def on_error(self, status_code):
        print (status_code)

    

auth = OAuthHandler(con_key, con_secret)
auth.set_access_token(acess_token, acess_secret)

twitterStream = Stream(auth, listener())
terms = [
        'elections',  'new york', 'new year'
        ,'india','usa','dhoni','microsoft','sony', 'china', 'kohli', 'modi'
        ,'hollywood','bollywood', 'trump', 'them', 'this', 'india'
        ]

while True:
    try:
        twitterStream.filter(track=terms)
    except:
        continue