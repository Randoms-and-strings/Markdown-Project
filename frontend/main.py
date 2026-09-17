import asyncio
import time
import aiohttp
import os
from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.datastructures import FormData, UploadFile
import starlette.status as status
from .image_parser import parse_img_from_form, save_to_s3, get_img_s3, remove_image_from_post
from dotenv import load_dotenv
from fastapi.params import Depends
from .rate_limiter import RateLimiter
from contextlib import asynccontextmanager
from markupsafe import Markup
load_dotenv()


API_PORT:int = os.getenv("API_PORT")
API_HOST:str = os.getenv("API_HOST")
API_FULL_URL:str = os.getenv("API_URL")
REDIS_HOST:str = os.getenv("REDIS_HOST")
REDIS_PORT:int = os.getenv("REDIS_PORT")
MAX_POST_LENGTH:int = 10000


# rate_limiter = RateLimiter(username=os.getenv("REDIS_USERNAME"),password=os.getenv("REDIS_PASSWORD"),
#                 host=os.getenv("REDIS_HOST"),port=os.getenv("REDIS_PORT"))
rate_limiter = RateLimiter(host=REDIS_HOST,port=REDIS_PORT)

@asynccontextmanager
async def lifespans(app:FastAPI):

    print("redis connected successfully")
    yield

    await rate_limiter.close_redis()

origins = ["*"]
app = FastAPI(lifespan=lifespans)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# ---------------------------------------------model and app config above-----------------------------------------------------------------------

# this is to test render is ready
@app.get("/availability", status_code=200)
def test_render_ready():
    return {
        "status": "ok"
    }
# route to display form, email as id
#use email as userid when displaying form
@app.get("/markdown-form/{user_email}", response_class=HTMLResponse)
async def markdown_form(request:Request, user_email:str):
    print("markdown func")
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(f"https://{API_FULL_URL}/user/create_new", params={"q": user_email}) as response:
            # async with session.get(f"http://{API_HOST}:{API_PORT}/user/create_new", params={"q": user_email}) as response:
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
# but there is also a rate limiter on the route.
@app.post("/processing-page/{email}", response_class=RedirectResponse)
async def processing_page(request:Request, email:dict = Depends(rate_limiter.main)):
    # print(email)
    # print(type(email))
    start_time = time.time()
    if isinstance(email, HTTPException):
        # print("returning error")
        raise email


    full_post:list[dict[str, int]] = []
    char_length:int = 0
    form_data:FormData = await request.form()
    last_element_position_in_form:int = int(list(form_data.items())[-1][0].split(":")[1])
    # print(form_data)
    # FormData([('h1:1', 'ffff'), ('img:2', UploadFile(filename='R.png', size=1802794, headers=Headers(
    #     {'content-disposition': 'form-data; name="img:2"; filename="R.png"', 'content-type': 'image/png'})))])

    if len(form_data) != last_element_position_in_form:
        raise HTTPException(status_code=400, detail="invalid request")

    if isinstance(form_data, FormData):
        for key in form_data:
            # print(form_data.get(items))
            if not isinstance(form_data.get(key), UploadFile):

                element_type: str = key.split(":")[0]
                element_position: int = int(key.split(":")[1])
                element_content: str = form_data.get(key)
                char_length += len(element_content)
                # print(element_type, element_position)

                if char_length > MAX_POST_LENGTH:
                    raise HTTPException(status_code=413, detail="exceeded allowed character limit for an article")

                full_post.append({
                    "type": element_type,
                    "position": element_position,
                    "content": element_content
                })

        start_img_parsing_time = time.time()
        images_to_parse:list[tuple[UploadFile, str, int]] = []
        for key in form_data:
            # print(form_data.get(items))
            if isinstance(form_data.get(key), UploadFile):
                element_type, position, picture_object = parse_img_from_form(key, form_data)

                if isinstance(element_type, HTTPException):
                    raise element_type
                    # return f"<h1>{element_type.get("detail")}</h1>"

                images_to_parse.append((picture_object, element_type, position))

                # full_post.append(s3_resp)
        group_save_img = await asyncio.gather(*[save_to_s3(items) for items in images_to_parse], return_exceptions=True)
        # print(group_save_img)
        for results in group_save_img:
            if isinstance(results, HTTPException):
                raise results #todo: saving method was non-atomic. later update for if some don't delete froms3
            elif isinstance(results, dict):
                full_post.append(results)
        print(f"took {time.time() - start_img_parsing_time}secs to add img")
        # print(full_post)
        try:
            api_start_time = time.time()
            full_post.sort(key=lambda item: item.get("position"))
            async with aiohttp.ClientSession() as session:
                # async with session.post(f"http://{API_HOST}:{API_PORT}/user/add_post/{email}",
                #                         json=full_post) as response:
                async with session.post(f"https://{API_FULL_URL}/user/add_post/{email}",
                                        json=full_post) as response:
                    # print("here1")
                    resp = await response.json()

                    # print("the resp:", resp)
            print(f"the addposttodb api function took {time.time() - api_start_time} secs to complete")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="something went wrong from our end, please try again at a later time")
            # return "<h1>something went wrong from our end, please try at a later time</h1>"
        else:
            if resp.get("detail") != "success":

                return resp

            # todo: no need to remove old post from s3 here, it can be pushed to queue to save time
            rmv_img_time = time.time()
            post_body:list = resp.get("former_post").get("post")
            remove_old_pics_from_s3:bool = await remove_image_from_post(post_body)
            if isinstance(remove_old_pics_from_s3, HTTPException):
                print("failed to delete former img from s3. log this and find out why")
            print(f"took {time.time() - rmv_img_time}secs to remove img")
            print(f"the function took {time.time() - start_time } secs to complete")
            return RedirectResponse(url=f"/post/{email}", status_code=status.HTTP_302_FOUND)
    # don't know how this can happen, but incase it can....
    raise HTTPException(status_code=500, detail="something went wrong")
    # return "<h1>something went wrong</h1>"

@app.get("/post/{user_email}")
async def get_markdown(request:Request, user_email:str):
    api_start_time = time.time()
    user_post = None
    # todo: could implement redis for faster post lookup
    try:
        async with aiohttp.ClientSession() as session:
            # async with session.get(f"http://{API_HOST}:{API_PORT}/get-user-post/{user_email}") as response:
            async with session.get(f"https://{API_FULL_URL}/get-user-post/{user_email}") as response:
                resp = await response.json()
                # print("the resp from getting the post:", resp)
    except Exception as err:
        print(err)
        return "<h1>something went wrong, we couldn't get your post</h1>"
    else:
        if not resp.get("status"):
            raise HTTPException(status_code=400, detail="something went wrong with your upload")

        user_post = resp.get("user_data").get("post")
        print(user_post)
    print(f"view markdown api took {time.time() - api_start_time} secs to complete")
    elements_present:list[Markup] = []

    for items in user_post:
        if items.get("type") == "h1":
            elements_present.append(Markup(f"<h1 class='gelasio-head center-elements'>{items.get('content')}</h1>"))
        elif items.get("type") == "h2":
            elements_present.append(Markup(f"<h2 class='gelasio-head center-elements'>{items.get('content')}</h2>"))
        elif items.get("type") == "p":
            elements_present.append(Markup(f"<p class='gelasio-body center-elements'>{items.get('content')}</p>"))
        elif items.get("type") == "ul":
            all_li_items:list[str] = items.get("content").split("/<newlinechar>")
            # print(all_li_items)
            arrangement:str = ""
            for li in all_li_items[:-1]:  #the split added "" at the end of the list, so had to exclude that
                arrangement += f"<li class='gelasio-body'>{li}</li>\n"
            # print(arrangement)
            elements_present.append(Markup(f"<ul class=''>"
                                           f"{arrangement}"
                                           f"</ul>"))
        elif items.get("type") == "img":
            img_name:str = items.get("content")
            img_link:str = get_img_s3(img_name)
            elements_present.append(Markup(f"<img class='img-styling' src={img_link} alt=''/>"))
            # get from s3
    print(f"view markdown function took {time.time() - api_start_time} secs to complete")
    return templates.TemplateResponse(request=request, name="markdown.html",
                                      context={"allowed_elements":elements_present,
                                               "user_data": user_post})


