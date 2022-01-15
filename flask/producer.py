import json
import pika,os


# params = pika.URLParameters('amqp://admin:mypass@rabbit:5672/%2f')

params = pika.ConnectionParameters(host='rabbit',port=5672,
credentials=pika.credentials.PlainCredentials('admin','mypass'),heartbeat=0)


connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='',routing_key='django',body=json.dumps(body),properties=properties)

print("Started Producing")