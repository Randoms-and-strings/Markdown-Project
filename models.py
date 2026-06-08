from pydantic import BaseModel
from mongoengine import *
# db for saving data, the schema
# listfield with dict inside
# the dict ield data will look like {"type": "<h1>", "position": 0, "data": "some content...."}


client = connect(host="mongodb+srv://randoms_and_strings:randoms&str1ngs@cluster0.6yeazny.mongodb.net/?appName=Cluster0")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class User(Document):
    email:str = EmailField(required=True, primary_key=True)
    user_writeup:list[dict] = ListField(DictField(required=True))
    # image_location = StringField()
