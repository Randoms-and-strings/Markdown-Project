# api to save info in db
# api to get info from db
# uvicorn api:app --host 0.0.0.0 --port 8001 --reload
from fastapi import FastAPI, HTTPException, Request
# import collections
# from collections import abc
# collections.MutableMapping = abc.MutableMapping
from pymongo import ReturnDocument
from .models import get_tables, client
from contextlib import asynccontextmanager
from dotenv import load_dotenv


load_dotenv()

markdown_collection = None
# rate_limiter = RateLimiter(username=os.getenv("REDIS_USERNAME"),password=os.getenv("REDIS_PASSWORD"),
#                 host=os.getenv("REDIS_HOST"),port=os.getenv("REDIS_PORT"))


@asynccontextmanager
async def lifespans(app:FastAPI):
    global markdown_collection
    markdown_collection = await get_tables()
    yield


    # await rate_limiter.close_redis()
    await client.close()


app = FastAPI(lifespan=lifespans)




@app.post("/user/add_post/{email}", status_code=201,response_model_by_alias=False)
async def create_markdown_post(request: Request, email:str):
    # print(type(email))
    # if isinstance(email, HTTPException):
    #     print("returning error")
    #     return email
    try:
        data = await request.json() #validate for if an idiot sends request not in json
    except Exception as error:
        print(error)
        return HTTPException(status_code=409, detail=f"expected json, received other data type")
    # else:
    #     data.sort(key= lambda item: item.get("position"))
        # print(data)


    try:
        # returns the old document that has been changed
        update_result = await markdown_collection.find_one_and_update(
            {"email": email},
            {"$set": {"post":  data }},
            return_document=ReturnDocument.BEFORE,
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
            "former_post": update_result
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
    # print(q)#
    if q:

        user = await markdown_collection.update_one({"email":q}, { "$setOnInsert": { "post": None} }, upsert=True)
        print(user)
        return {
            "detail": "user created successfully"
        }


    return HTTPException(status_code=400, detail="missing email field. Please provide an email")
