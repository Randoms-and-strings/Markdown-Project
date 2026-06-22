from pydantic import BaseModel
from mongoengine import *
import pymongo
import asyncio
from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends
from typing import Annotated, Optional
from bson import ObjectId
import mongoengine
#_______________________________________________________________________________________________________________________
# db for saving data, the schema
# listfield with dict inside
# the dict ield data will look like {"type": "<h1>", "position": 0, "data": "some content...."}
url = "mongodb+srv://randoms_and_strings:randoms&str1ngs@cluster0.6yeazny.mongodb.net/?appName=Cluster0"

# def main():
#
#     client = mongoengine.connect(host=url)
#     try:
#
#         client.admin.command("ping")
#         print("successfully connected")
#
#
#     except Exception as e:
#         raise Exception("Unable to find the document due to the following error: ", e)
#
#     class PostData(mongoengine.EmbeddedDocument):
#         type:str = mongoengine.StringField(required=True)
#         position:int = mongoengine.IntField(required=True)
#         content:str = mongoengine.StringField(required=True)
#
#
#
#     class MarkdownPost(mongoengine.Document):
#         email: str = mongoengine.StringField(required=True, unique=True)
#         post: list[PostData] = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PostData))
#         meta = {
#             'indexes': [
#                 'email',
#             ]
#         }

# ________________________________________________above works, below testing____________________________________________________________________

# PyObjectId = Annotated[str, BeforeValidator(str)]
#
# class PostData(SQLModel, table=True):
#     # id: int | None = Field(default=None, primary_key=True)
#     id: Optional[PyObjectId] = Field(alias="_id", default=None, primary_key=True)
#     type:str
#     position:int
#     content:str
#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,)
#
# class MarkdownPost(SQLModel, table=True):
#     email: str = Field(index=True)
#     post: list[PostData]
#
# url = "mongodb+srv://randoms_and_strings:randoms&str1ngs@cluster0.6yeazny.mongodb.net/?appName=Cluster0"
# # connect_args = {"check_same_thread": False}
# # engine = create_engine(url, connect_args=connect_args)
#
# # def create_db_and_tables():
# #     SQLModel.metadata.create_all(engine)
# #
# # def get_session():
# #     with Session(engine) as session:
# #         yield session
# #
# #
# # SessionDep = Annotated[Session, Depends(get_session)]
#
# PyObjectId = Annotated[str, BeforeValidator(str)]
# class PostData(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     type: str = Field(...)
#     position: int = Field(...)
#     content: str = Field(...)
#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#         json_schema_extra={
#             "example": {
#                 "type": "h1",
#                 "position": 1,
#                 "content": "TITLE OF A BLOGPOST OR CONTENT",
#             }
#         },
#     )
# class UpdatePostData(BaseModel):
#     type: Optional[str] = None
#     position: Optional[int] = None
#     content: Optional[str] = None
#     model_config = ConfigDict(
#         json_encoders={ObjectId: str},
#         arbitrary_types_allowed=True,
#         json_schema_extra={
#             "example": {
#                 "type": "h1",
#                 "position": 1,
#                 "content": "TITLE OF A BLOGPOST OR CONTENT",
#             }
#         },
#     )
#
# class MarkdownPost(BaseModel):
#     email: EmailStr = Field(nullable=False, unique=True)
#     post: list[PostData]




client = pymongo.AsyncMongoClient(url,server_api=pymongo.server_api.ServerApi(version="1", strict=True,deprecation_errors=True))
try:
    client.admin.command("ping")
    print("successfully connected")
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)






# class UpdateMarkdownPost(BaseModel):
#     email: Optional[EmailStr] = None
#     post: Optional[list[PostData]] = None



def get_tables():
    db = client.get_database("cluster0")
    markdown_coll = db.get_collection(name="markdownpost")
    print(markdown_coll, "markdown?")
    return markdown_coll

markdown_collection = get_tables()

