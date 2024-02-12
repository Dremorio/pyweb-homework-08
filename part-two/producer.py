import pika
import json
from mongoengine import connect
from models import Contact
from faker import Faker
from db import *

fake = Faker()


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

for _ in range(10):
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        email_send=False
    )
    contact.save()
    
    channel.basic_publish(exchange='',
                          routing_key='email_queue',
                          body=json.dumps(str(contact.id)))

    print(f"Sent contact ID {contact.id} to the queue")

connection.close()
