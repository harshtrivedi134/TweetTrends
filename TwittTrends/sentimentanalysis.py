from multiprocessing.dummy import Pool as ThreadPool
import json
import boto3
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from geocoder import location
from textblob import TextBlob



sqs = boto3.resource('sqs', region_name="us-east-2")
q = sqs.get_queue_by_name(QueueName='harsh-test')

snsClient = boto3.client('sns', region_name="us-east-2")

host = "enter elastic search domain "
port = 443

#create ElasticSearch object
es = Elasticsearch(
        hosts=[{'host': host, 'port': port}],
        use_ssl=True,
        # http_auth=awsauth,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )


def getSQSQueue(n):
    try:
    # code to get data from sqs
      for message in q.receive_messages(MessageAttributeNames=['location']):
        text = message.body
        print (text)
        print (text)
        blob = TextBlob(text)

        print("Sentiment of Tweet is: ",blob.sentiment.polarity)

        loc = message.message_attributes.get('location')
        doc = dict()

        doc["text"] = text
        doc["location"] = loc
        doc["sentiment"] = text(blob.sentiment.polarity)


        response = snsClient.publish(TopicArn='topic arn',
                                     Message= json.dumps(doc),
                                     MessageAttributes = {

                                     },

                                     )
        return text
    except:
        print("unable to fetch location or sentiment failed")








def calculateParallel(numbers, threads):
    # configure the worker pool

    pool = ThreadPool(processes= 1)
    results = pool.map(getSQSQueue,numbers)
    pool.close()
    pool.join()
    return results




if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6]

    for n in range(50):
        tweet_text = calculateParallel(numbers, 10)

        print(n)

