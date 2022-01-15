from itertools import product
import json
from math import prod
import os,django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product
import pika


# params = pika.URLParameters('amqp://admin:mypass@rabbit:5672/%2f')
params = pika.ConnectionParameters(host='rabbit',port=5672,
credentials=pika.credentials.PlainCredentials('admin','mypass'),heartbeat=0)
# pika.ConnectionParameters(heartbeat_interval=0)
connection = pika.BlockingConnection(params)

channel = connection.channel()




channel.queue_declare(queue='django')


def callback(ch,method,properties,body):
    print("Received in Django")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=data)
        product.likes = product.likes + 1
        product.save()
        print("product like increasesd")
    
    else:
        product = Product.objects.get(id=data)
        product.comment=properties.content_type
        product.save()
        print("product comment saved")

channel.basic_consume(queue='django',on_message_callback=callback,auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()