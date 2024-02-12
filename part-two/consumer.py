import pika
from mongoengine import connect
from models import Contact
import json
from db import *

def callback(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    
    if contact:
        print(f"Sending email to {contact.email}")
        contact.email_send = True
        contact.save()
        print(f"Email sent to {contact.fullname}, email_send set to {contact.email_send}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue',
                      on_message_callback=callback,
                      auto_ack=True)


try:
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        channel.stop_consuming()
    except Exception as e:
        print(f"Error while trying to stop consuming: {e}")
    connection.close()
    print('Consumer stopped.')
