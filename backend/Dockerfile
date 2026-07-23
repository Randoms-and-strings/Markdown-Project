FROM python:3.14-alpine
WORKDIR /backend-markdownapp
COPY ./requirements.txt requirements.txt
RUN apk add --no-cache curl
RUN pip install -r requirements.txt
RUN pip install fastapi[standard]
COPY . .
EXPOSE 8001
CMD ["fastapi", "run", "./api.py", "--port", "8001"]