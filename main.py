import aiohttp
from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.datastructures import FormData, UploadFile
from image_parser import parse_img_from_form, save_to_s3
from dotenv import load_dotenv
load_dotenv()


API_PORT = 8001
API_HOST = "http://127.0.0.1"

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
            async with session.get(F"{API_HOST}:{API_PORT}/user/create_new", params={"q": user_email}) as response:
                # print("here1")
                resp = await response.json()
                # print("done new account", resp)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail="something went wrong from our end, please try again at a later time")
        # return "<h1>something went wrong from our end, please try again at a later time</h1>"
    else:
        if not resp.get("detail"):
            raise resp
            # return f"<h1>{resp.get("detail")}</h1>"

    return templates.TemplateResponse(request=request, name="input.html", context={"email": user_email})


# route to send form data to api, step 2 is build api to receive, step3 is to redirect to page
@app.post("/processing-page/{email}")
async def processing_page(request:Request, email:str):
    # print(email)
    full_post = []
    form_data:FormData = await request.form()
    last_element_position_in_form:int = int(list(form_data.items())[-1][0].split(":")[1])
    print(form_data)
    # FormData([('h1:1', 'ffff'), ('img:2', UploadFile(filename='R.png', size=1802794, headers=Headers(
    #     {'content-disposition': 'form-data; name="img:2"; filename="R.png"', 'content-type': 'image/png'})))])

    if len(form_data) != last_element_position_in_form:
        raise HTTPException(status_code=400, detail="invalid request")

    if isinstance(form_data, FormData):
        for key in form_data:
            # print(form_data.get(items))
            if isinstance(form_data.get(key), UploadFile):
                element_type, position, picture_object = parse_img_from_form(key, form_data)

                if isinstance(element_type, HTTPException):
                    raise element_type
                    # return f"<h1>{element_type.get("detail")}</h1>"

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
                async with session.post(f"{API_HOST}:{API_PORT}/user/add_post/{email}", json=full_post) as response:
                    # print("here1")
                    resp = await response.json()
                    # print("the resp:", resp)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="something went wrong from our end, please try again at a later time")
            # return "<h1>something went wrong from our end, please try at a later time</h1>"
        else:
            if resp.get("detail") != "success":
                raise HTTPException(status_code=400, detail="something went wrong with your upload")
                # return "<h1>something went wrong with your upload</h1>"
            return {
                "h1": full_post
            }
    # don't know how this can happen, but incase it can....
    raise HTTPException(status_code=500, detail="something went wrong")
    # return "<h1>something went wrong</h1>"

@app.get("/post/{user_email}")
async def get_markdown(user_email:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_HOST}:{API_PORT}/get-user-post/{user_email}") as response:
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