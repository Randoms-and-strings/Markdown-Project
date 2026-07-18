FROM python:3.14-alpine
WORKDIR /frontend-markdownapp
COPY ./frontend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./frontend .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host 0.0.0.0", "--${APP_PORT}"]