# api to save info in db
# api to get info from db
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request
from pymongo import ReturnDocument
from models import markdown_collection, get_tables
from contextlib import asynccontextmanager
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
from sqlmodel import Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class MarkdownPost(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default_factory=PyObjectId)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    post: Optional[list]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

@asynccontextmanager
async def lifespans(app:FastAPI):
    # yield main()
    get_tables()
    yield

app = FastAPI(lifespan=lifespans)



@app.post("/user/add_post/{email}", status_code=201,response_model_by_alias=False)                #
async def create_markdown_post(request: Request, email:str):                       #
    try:
        data = await request.json() #validate for if an idiot sends request not in json
    except Exception as error:
        print(error)
        return HTTPException(status_code=409, detail=f"expected json, received other data type")
    # print(data)
    # if (existing_user := await markdown_collection.find_one({"email": email})) is not None:
    #     # return HTTPException(status_code=409, detail=f"email already exists")
    #     print(existing_user, len(existing_user["post"]))
        # if len(existing_user["post"]) >0:
        #     return HTTPException(status_code=409, detail=f"email already exists")
        #{'status_code': 409, 'detail': 'email already exists, please use another.', 'headers': None}

    try:
        update_result = await markdown_collection.find_one_and_update(
            {"email": email},
            # {"$push": {"post": {"$each": data} }},
            {"$set": {"post":  data }},
            return_document=ReturnDocument.AFTER,
        )


        # print(update_result)
    except Exception as e:
        print(e)
        return HTTPException(status_code=409, detail="failed to insert package")
    else:
        if update_result is None:
            return HTTPException(status_code=404, detail=f"User with email: {email} not found")
        update_result["_id"] = str(update_result["_id"])
        # print("returning to processing api the data:", update_result)
        return {
            "detail": "success",
            "insert": update_result
        }


@app.get("/get-user-post/{user_id}/")
async def get_post(user_id:str):
    try:
        the_user = await markdown_collection.find_one({"email":user_id})
        # print(the_user)
    except Exception as error:
        print(error)
        return HTTPException(status_code=500, detail=f"something went wrong getting your post. please try at a later time")
    else:
        if the_user:
            if len(the_user["post"]) > 0:
                the_user["_id"] = str(the_user["_id"])
                return {
                    "status": "success",
                    "user_data": the_user
                }
            return HTTPException(status_code=409, detail="You dont have any post to display currently??")
        return HTTPException(status_code=409, detail=f"user with this email does not exist")



@app.get("/user/create_new", status_code=201,response_model_by_alias=False)                #
async def create_markdown_user(q: str):
    print(q)#
    if q:

        user = await markdown_collection.update_one({"email":q}, { "$setOnInsert": { "post": None} }, upsert=True)
        # user = await markdown_collection.find_one({"email": q})
        # if user is not None:
        #     return
        #
        # new_user = await markdown_collection.insert_one({"email": q, "post": []})
        print(user)
        return {
            "detail": "user created successfully"
        }


    return HTTPException(status_code=400, detail="missing email field. Please provide an email")
