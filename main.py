import os
import aiohttp
from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.datastructures import FormData, UploadFile
import uuid
import boto3
from dotenv import load_dotenv
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

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# ---------------------------------------------model and app config above-----------------------------------------------------------------------
# route to display form, email as id
#use email as userid when displaying form
@app.get("/markdown-form/{user_email}", response_class=HTMLResponse)
async def markdown_form(request:Request, user_email:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8001/user/create_new", params={"q": user_email}) as response:
                # print("here1")
                resp = await response.json()
                # print("done new account", resp)
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=500,
        #                     detail="something went wrong from our end, please try again at a later time")
        return "<h1>something went wrong from our end, please try again at a later time</h1>"
    else:
        if not resp.get("detail"):
            # raise resp
            return f"<h1>{resp.get("detail")}</h1>"

    return templates.TemplateResponse(request=request, name="input.html", context={"email": user_email})



# route to send form data to api, step 2 is build api to receive, step3 is to redirect to page
@app.post("/processing-page/{email}")
async def processing_page(request:Request, email:str):
    # print(email)
    full_post = []
    form_data = await request.form()
    print(form_data, len(form_data))
    # FormData([('h1:1', 'ffff'), ('img:2', UploadFile(filename='R.png', size=1802794, headers=Headers(
    #     {'content-disposition': 'form-data; name="img:2"; filename="R.png"', 'content-type': 'image/png'})))])

    if isinstance(form_data, FormData):
        for key in form_data:
            # print(form_data.get(items))
            if isinstance(form_data.get(key), UploadFile):
                element_type, position, picture_object = parse_img_from_form(key, form_data)

                if isinstance(element_type, HTTPException):
                    # raise element_type
                    return f"<h1>{element_type.get("detail")}</h1>"

                resp:dict|HTTPException = save_to_s3(picture_object, element_type, position)

                if isinstance(resp, HTTPException):
                    # raise resp
                    return f"<h1>{resp.get("detail")}</h1>"

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
                async with session.post(f"http://127.0.0.1:8001/user/add_post/{email}", json=full_post) as response:
                    # print("here1")
                    resp = await response.json()
                    # print("the resp:", resp)
        except Exception as e:
            print(e)
            # raise HTTPException(status_code=500, detail="something went wrong from our end, please try again at a later time")
            return "<h1>something went wrong from our end, please try at a later time</h1>"
        else:
            if resp.get("detail") != "success":
                # raise HTTPException(status_code=400, detail="something went wrong with your upload")
                return "<h1>something went wrong with your upload</h1>"
            return {
                "h1": full_post
            }
    # don't know how this can happen, but incase it can....
    # raise HTTPException(status_code=500, detail="something went wrong")
    return "<h1>something went wrong</h1>"

@app.get("/post/{user_email}")
async def get_markdown(user_email:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:8001/get-user-post/{user_email}") as response:
                resp = await response.json()
                # print("the resp from getting the post:", resp)
    except Exception as err:
        print(err)
        return "<h1>something went wrong, we couldn't get your post</h1>"
    else:
        if not resp.get("status"):
            # raise HTTPException(status_code=400, detail="something went wrong with your upload")
            return f"<h1>{resp.get("detail")}</h1>"
        return {
            "the_post": resp.get("user_data")
        }

# figure out numbering solution for element.