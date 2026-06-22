import os
import requests
import aiohttp
from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from contextlib import asynccontextmanager
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
from pymongo import ReturnDocument
import asyncio
from models import *
from starlette.datastructures import FormData, UploadFile
import uuid
import boto3
from dotenv import load_dotenv
from os import getenv
load_dotenv()

PyObjectId = Annotated[str, BeforeValidator(str)]
class PostData(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    type: str = Field(...)
    position: int = Field(...)
    content: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "type": "h1",
                "position": 1,
                "content": "TITLE OF A BLOGPOST OR CONTENT",
            }
        },
    )

class UpdatePostData(BaseModel):
    type: Optional[str] = None
    position: Optional[int] = None
    content: Optional[str] = None
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "type": "h1",
                "position": 1,
                "content": "TITLE OF A BLOGPOST OR CONTENT",
            }
        },
    )

class MarkdownPost(BaseModel):
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    post: Optional[list[PostData]]

class UpdateMarkdownPost(BaseModel):
    post: Optional[list[PostData]]

def parse_img_from_form(picture_object_key:str, form_object_iterable: FormData) -> tuple[str, int, UploadFile] | tuple[HTTPException, None, None]:
    element_type = picture_object_key.split(":")[0]
    element_position = int(picture_object_key.split(":")[1])
    raw_image_object: UploadFile = form_object_iterable.get(picture_object_key)

    if raw_image_object.filename.split(".")[-1] not in ["png", "jpg", "jpeg", "webp", "gif"]:
        return HTTPException(status_code=422, detail="Image type not supported"), None, None

    image_extension = raw_image_object.filename.split(".")[-1]
    new_filename = str(uuid.uuid4())
    raw_image_object.filename = f'{new_filename}.{image_extension}'
    # new_filename = raw_image_object.filename
    print(new_filename)

    image_max_size = 1024 * 1024 * 5  # 5mb max filesize upload
    if raw_image_object.size > image_max_size:
        return HTTPException(status_code=422, detail="Image item too large"), None, None

    return element_type, element_position, raw_image_object

def save_to_s3(cleaned_picture_object: UploadFile, element_name:str, element_position:int) -> dict[str, int]|HTTPException:
    obj = boto3.client("s3")
    try:
        with cleaned_picture_object.file as imageBytes:
            # contents:bytes =imageBytes.read()
            # print(contents, imageBytes)
            imageBytes.seek(0)
            obj.upload_fileobj(imageBytes,
                               os.getenv("AWS_BUCKET_NAME"),
                               f"{os.getenv("AWS_BUCKET_FOLDER")}/{cleaned_picture_object.filename}")
            print("done successfully")

    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong uploading your file")
    else:
        return {
            "type": element_name,
            "position": element_position,
            "content": cleaned_picture_object.filename
        }




@asynccontextmanager
async def lifespans(app:FastAPI):
    # yield main()
    get_tables()


    yield

app = FastAPI(lifespan=lifespans)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def create_db_client():
#     main()
# --------------------------------------------------------------------------------------------------------------------


# route to display form, email as id
#use email as userid when displaying form
@app.get("/markdown-form/{user_email}", response_class=HTMLResponse)
async def markdown_form(request:Request, user_email:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8000/user/create_new", params={"q": user_email}) as response:
                # print("here1")
                resp = await response.json()
                print("done new account", resp)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail="something went wrong from our end, please try again at a later time")
    # else:
        if not resp["detail"]:
            raise resp

    return templates.TemplateResponse(request=request, name="input.html", context={"email": user_email})

#---------------------------------------------------------------------------------------------------------------------
# route to send form data to api, step 2 is build api to receive, step3 is to redirect to page
@app.post("/processing-page/{email}")
async def processing_page(request:Request, email:str):
    # print(email)
    full_post = []
    form_data = await request.form()
    # print(form_data)
    # FormData([('h1:1', 'ffff'), ('img:2', UploadFile(filename='R.png', size=1802794, headers=Headers(
    #     {'content-disposition': 'form-data; name="img:2"; filename="R.png"', 'content-type': 'image/png'})))])

    if isinstance(form_data, FormData):
        for key in form_data:
            # print(form_data.get(items))
            if isinstance(form_data.get(key), UploadFile):
                element_type, position, picture_object = parse_img_from_form(key, form_data)

                if isinstance(element_type, HTTPException):
                    raise element_type

                resp:dict|HTTPException = save_to_s3(picture_object, element_type, position)

                if isinstance(resp, HTTPException):
                    raise resp

                full_post.append(resp)


            else:
                element_type = key.split(":")[0]
                element_position = int(key.split(":")[1])
                element_content = form_data.get(key)
                # print(element_type, element_position)

                full_post.append({
                    "type": element_type,
                    "position": element_position,
                    "content": element_content
                })

        # print(full_post)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"http://127.0.0.1:8000/user/add_post/{email}", json=full_post) as response:
                    # print("here1")
                    resp = await response.json()
                    print("done")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="something went wrong from our end, please try again at a later time")
        else:
            if resp.detail != "success":
                raise HTTPException(status_code=400, detail="something went wrong with your upload")
            return {
                "h1": full_post
            }
    # don't know how this can happen, but incase it can....
    raise HTTPException(status_code=500, detail="something went wrong")

# ____________________________________________________________________________________________________________________

#api to save to db
# @app.post("/user-post/add", response_description="Add new post and user", status_code=201,
#           response_model_by_alias=False, response_model=PostData)                #
# async def create_markdown_user(array_of_postdata: list[PostData]):                       #
#     markdown_post = []
#     for post_data in array_of_postdata:
#         markdown_post.append(post_data.model_dump(by_alias=True, exclude=["id"]))
#     # markdown_collection
#     print("done")
#
#     return {
#         "detail": "success"
#     }
@app.post("/user/add_post/{email}", status_code=201,response_model_by_alias=False)                #
async def create_markdown_post(request: Request, email:str):                       #
    data = await request.json()
    print(data)
    if (existing_user := await markdown_collection.find_one({"email": email})) is not None:
        # return HTTPException(status_code=409, detail=f"email already exists")
        print(existing_user, len(existing_user["post"]))
        if len(existing_user["post"]) >0:
            return HTTPException(status_code=409, detail=f"email already exists")
        #{'status_code': 409, 'detail': 'email already exists, please use another.', 'headers': None}

    try:
        update_result = await markdown_collection.find_one_and_update(
            {"email": email},
            {"post": data},
            return_document=ReturnDocument.AFTER,
        )
    except Exception as e:
        print(e)
        return HTTPException(status_code=409, detail="failed to insert package")
    else:
        if update_result is None:
            raise HTTPException(status_code=404, detail=f"User with email: {email} not found")

        return {
            "detail": "success",
            "insert": update_result
        }



@app.get("/user/create_new", status_code=201,response_model_by_alias=False)                #
async def create_markdown_user(q: str):
    print(q)#
    if q:
        user = await markdown_collection.find_one({"email": q})
        if user is not None:
            return HTTPException(status_code=409, detail="email already exists, please use another.")

        new_user = await markdown_collection.insert_one({"email": q, "post": None})
        print(new_user)
        return {
            "detail": "user created successfully"
        }


    return HTTPException(status_code=400, detail="missing email field. Please provide an email")
# why not create email for user on loadpage, then on submit, add the post
# api to get from db