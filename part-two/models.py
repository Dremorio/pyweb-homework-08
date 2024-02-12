from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    email_send = BooleanField(default=False)
