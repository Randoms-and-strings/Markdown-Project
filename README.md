# Markdown App 

Async FastAPI backend and Next.js frontend for a modular Markdown editor. The backend stores posts in MongoDB, uploads images to AWS S3, and exposes async endpoints consumed by the frontend. The frontend handles the user form, image uploads, rate limiting, and rendering. Both services are containerized and runnable from the repository root using docker compose.  

---

## Tech Stack
- **Language / Framework:** Python, FastAPI (async)  
- **Database:** MongoDB (async pymongo)  
- **Cache / Rate limiting:** Redis  
- **Storage:** AWS S3 (aioboto3)  
- **Concurrency / HTTP client:** asyncio, aiohttp  
- **Deployment:** Render (backend and fontend) 
- **Containerization:** Docker / docker-compose

---

Repository Structure
/backend — FastAPI service (models, DB calls, API endpoints).

/frontend — FastAPI frontend service (form UI, rate limiter, S3 helpers) or Next.js frontend depending on your repo layout; contains S3 upload helpers, image parsing, and client routes.

docker-compose.yml (root) — orchestrates backend, frontend, mongodb, redis, and other services.

.env — environment variables (not committed).

README.md — this file.

---

Quickstart from Repository Root
1. **Create env files** 
   - `/backend/.env` and `/frontend/.env` — see **Environment variables** below.

2. **Build and run all services**
   ```bash
   docker compose up --build
3. **Verify health**

Backend health (example):

bash
curl http://localhost:${API_PORT:-8001}/availability
Expected: {"status":"ok"}

Frontend health (example):

bash
curl http://localhost:${APP_PORT:-8000}/availability
4. **Stop**

bash
docker compose down


Services
- frontend
Build context: ./frontend

Exposes port ${APP_PORT}:8000 (set APP_PORT in .env or use default 8000).

Uses ./frontend/.env and environment variables for AWS credentials and S3 region.

Depends on backend and redis (waits for healthy services).

- backend (markdown-app-backend)
Build context: ./backend

Exposes port ${API_PORT}:8001 (set API_PORT in .env or use default 8001).

Uses ./backend/.env.

Healthcheck: http://markdown-app-backend:8001/user/create_new?q=tobi@gmail.com (container internal check).

Depends on mongodb.

- redis (markdown-app-redis)
Image: redis:alpine

Exposes ${REDIS_PORT}:${REDIS_PORT} (set REDIS_PORT in .env).

- mongodb (markdown-app-mongodb)
Image: mongodb/mongodb-community-server:latest

Exposes 27017:27017

Initializes with mongo-init.js and environment variables for root user and DB.

Environment variables
Create /backend/.env and /frontend/.env with the variables below. Do not commit .env files.

- Backend (/backend/.env)
Code
API_PORT=8001
API_HOST=localhost
API_URL=localhost:8001
MONGODB_URL=mongodb://<user>:<pass>@mongodb:27017/<db>
MONGODB_USERNAME=<root-user>
MONGODB_PASSWORD=<root-pass>
MONGODB_DB=<db>
MONGODB_CUSTOM_USERNAME=<app-user>
MONGODB_PASSWORD=<app-user-pass>
REDIS_HOST=redis
REDIS_PORT=6379

- Frontend (/frontend/.env)
Code
APP_PORT=8000
API_URL=http://localhost:8001
REDIS_HOST=redis
REDIS_PORT=6379
S3_MARKDOWNAPP_BUCKETNAME=<bucket-name>
S3_MARKDOWNAPP_REGION=<region>
S3_MARKDOWNAPP_FOLDER=<folder-prefix>
ACCESS_KEY=<aws-access-key>
SECRET_KEY=<aws-secret-key>

- Root / Compose environment (optional)
Code
API_PORT=8001
APP_PORT=8000
REDIS_PORT=6379
MONGODB_USERNAME=<root-user>
MONGODB_PASSWORD=<root-pass>
MONGODB_DB=<db>
MONGODB_CUSTOM_USERNAME=<app-user>
MONGODB_PASSWORD=<app-user-pass>


Key endpoints (local)
- Backend
GET /availability — healthcheck

GET /user/create_new?q=<email> — create/upsert user record

POST /user/add_post/{email} — save a user’s post (expects JSON array of blocks)

GET /get-user-post/{user_id} — fetch stored post by email

- Frontend
GET /markdown-form/{user_email} — render input form (frontend route)

POST /processing-page/{email} — process form, upload images to S3, call backend /user/add_post/{email}

(Optional) GET /availability — frontend health 

Data model (posts)
Posts are ordered lists of block objects:

json
{
  "type": "h1" | "h2" | "p" | "ul" | "img",
  "position": 0,
  "content": "..."
}
Images: validated extensions (png, jpg, jpeg, webp, gif), max size 5 MB, filenames replaced with UUIDs before upload.

S3 URL: https://{BUCKET}.s3.{REGION}.amazonaws.com/{FOLDER}/{filename}

