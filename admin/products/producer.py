import json
import pika,os

params = pika.ConnectionParameters(host='rabbit',port=5672,
credentials=pika.credentials.PlainCredentials('admin','mypass'),heartbeat=0)

connection = pika.BlockingConnection(params)
# ,heartbeat=600,                         blocked_connection_timeout=300

# pika.ConnectionParameters(heartbeat_interval=600)
channel = connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)

    channel.basic_publish(exchange='',routing_key='flask',body=json.dumps(body),properties=properties)

print("Started Producing")