FROM python:3.14-alpine
WORKDIR /backend-markdownapp
COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./backend .
EXPOSE 8001
CMD ["uvicorn", "api:app", "--host 0.0.0.0", "--${API_PORT}"]