import json
from main import Product,db
import pika
params = pika.ConnectionParameters(host='rabbit',port=5672,
credentials=pika.credentials.PlainCredentials('admin','mypass'),heartbeat=0)

connection = pika.BlockingConnection(params)

pika.ConnectionParameters(heartbeat=0)

channel = connection.channel()

channel.queue_declare(queue='flask')


def callback(ch,method,properties,body):
    print("Received in Flask")
    data = json.loads(body)
    print(data)
    print('Hello')
    print(properties.content_type)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'],title=data['title'],image=data['image'],comment=data['comment'])
        db.session.add(product)
        db.session.commit()
        print('commited')

    elif properties.content_type == 'product_update':
        product = Product.query.get(data['id'])
        product.title=data['title']
        product.image=data['image']
        product.comment = data['comment']
        db.session.commit()

    elif properties.content_type=='product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()

channel.basic_consume(queue='flask',on_message_callback=callback,auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()