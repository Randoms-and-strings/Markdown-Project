FROM python:3.14-alpine
WORKDIR /frontend-markdownapp
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install fastapi[standard]
COPY . .
EXPOSE 8000
CMD ["fastapi", "run", "./main.py", "--port", "8000"]