from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# from jinja2 import render
from models import User
# this page for getting data from the form, parsing the logic, and calling api to save it to the db
# another route for calling api to get data from form and display as markdown

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# route to display form, email as id
#use email as userid when displaying form
@app.get("/markdown-form/{user_email}", response_class=HTMLResponse)
def markdown_form(request:Request, user_email:str):
    return templates.TemplateResponse(request=request, name="input.html", context={"email": user_email})


# route to save form data to db then redirect to a third route that'll render an html
@app.post("/markdown-page/{user_email}/{post_id}", response_class=HTMLResponse)
async def markdown_page(request:Request, user_email:str, post_id:str):
    return "<h1>Hiiiiiii</h1>"



#api to save to db


# api to get from db