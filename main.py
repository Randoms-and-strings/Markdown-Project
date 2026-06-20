import os

from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from contextlib import asynccontextmanager
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, BeforeValidator
import asyncio
from models import *
from starlette.datastructures import FormData, UploadFile
import uuid
import boto3
from dotenv import load_dotenv
from os import getenv
load_dotenv()

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

    yield await main2()

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
def markdown_form(request:Request, user_email:str):
    return templates.TemplateResponse(request=request, name="input.html", context={"email": user_email})

#---------------------------------------------------------------------------------------------------------------------
# route to send form data to api, step 2 is build api to receive, step3 is to redirect to page
@app.post("/processing-page/{email}")
async def processing_page(request:Request, email:str):
    print(email)
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
                element_position = (key.split(":")[1]),
                element_content = form_data.get(key)

                full_post.append({
                    "type": element_type,
                    "position": element_position,
                    "content": element_content
                })

        # print(full_post)
        return {
            "h1": full_post
        }
    # don't know how this can happen, but incase it can....
    raise HTTPException(status_code=500, detail="something went wrong")

# ____________________________________________________________________________________________________________________

#api to save to db
@app.post("/students/",response_description="Add new student",response_model=MarkdownPost,status_code=201,
          response_model_by_alias=False)
async def create_markdown_user():
    # new_post = PostData.model_dump()
    pass

# api to get from db