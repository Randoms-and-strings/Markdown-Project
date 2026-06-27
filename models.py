import pymongo
#_______________________________________________________________________________________________________________________
# db for saving data, the schema
# listfield with dict inside
# the dict ield data will look like {"type": "<h1>", "position": 0, "data": "some content...."}
url = "mongodb+srv://randoms_and_strings:randoms&str1ngs@cluster0.6yeazny.mongodb.net/?appName=Cluster0"

client = pymongo.AsyncMongoClient(url,server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
try:
    client.admin.command("ping")
    print("successfully connected")
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

def get_tables():
    db = client.get_database("cluster0")
    markdown_coll = db.get_collection(name="markdownpost")
    print(markdown_coll, "markdown?")
    return markdown_coll

markdown_collection = get_tables()

