from mongoengine import connect, Document, StringField, ListField, ReferenceField
from models import Author, Quote

connect('mongodb-hw-8', host='localhost', port=27017)

def find_quotes_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(f"\"{quote.quote}\" - {author.fullname}")
    else:
        print("Author not found.")

def find_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(f"\"{quote.quote}\" - {quote.author.fullname}")

def find_quotes_by_tags(tags_list):
    quotes = Quote.objects(tags__in=tags_list)
    for quote in quotes:
        print(f"\"{quote.quote}\" - {quote.author.fullname}")



if __name__ == "__main__":
    while True:
        user_input = input("Enter command: ")
        if user_input.lower() == "exit":
            break
        try:
            command, value = user_input.split(":", 1)
            command = command.strip().lower()
            value = value.strip()
            if command == "name":
                find_quotes_by_author(value)
            elif command == "tag":
                find_quotes_by_tag(value)
            elif command == "tags":
                tags = value.split(",")
                find_quotes_by_tags(tags)
            else:
                print("Unknown command. Please use 'name:', 'tag:', or 'tags:' followed by your search query.")
        except ValueError:
            print("Invalid command format. Please use 'name:', 'tag:', or 'tags:' followed by your search query.")
