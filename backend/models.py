import os
from dotenv import load_dotenv
import pymongo
from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
from bson import ObjectId
from typing import Annotated, Optional
#_______________________________________________________________________________________________________________________
# db for saving data, the schema
# listfield with dict inside
# the dict ield data will look like {"type": "<h1>", "position": 0, "content": "some content...."}
load_dotenv()
PyObjectId = Annotated[str, BeforeValidator(str)]
URL = os.getenv("MONGODB_URL")

class MarkdownPost(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=PyObjectId)
    email: EmailStr = Field(...)
    post: Optional[list]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


client = pymongo.AsyncMongoClient(URL,server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
try:

    client.admin.command("ping")
    print("successfully connected")
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

async def get_tables():
    db = client.get_database("cluster0")
    markdown_coll = db.get_collection(name="markdownpost")
    await markdown_coll.create_index("email")
    print(markdown_coll, "markdown?")
    return markdown_coll


