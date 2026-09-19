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
Create .env files for root, /backend/.env, and /frontend/.env with the variables listed below.

Build and run all services:

bash
docker compose up --build
Verify health (example):

bash
curl http://localhost:8001/availability   # backend health
curl http://localhost:8000/availability   # frontend health 

---

Backend Setup
Start locally
Ensure /backend/.env contains required variables (see Environment Variables).

From repo root:

bash
docker compose up backend
or to run only backend with uvicorn (dev):

bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
Key backend endpoints
GET /availability — readiness probe.

GET /user/create_new?q=<email> — upsert user record.

POST /user/add_post/{email} — save user post (JSON array of blocks).

GET /get-user-post/{user_id} — fetch stored post by email.

Notes
Backend uses an async MongoDB client and creates an index on email.

Keep DB migrations and index creation idempotent for container restarts.

Frontend Setup
Start locally
Ensure /frontend/.env contains required variables (see Environment Variables).

From repo root:

bash
docker compose up frontend
or run the frontend dev server (if Next.js):

bash
cd frontend
npm install
npm run dev
Frontend responsibilities
Presents the markdown form and handles file uploads.

Validates images and enforces 5 MB max size and allowed extensions.

Uses Redis for rate limiting (per email).

Calls backend endpoints (/user/create_new, /user/add_post/{email}, /get-user-post/{email}) and renders the compiled HTML.

Notes
Rate limiter and S3 helpers live in the frontend directory; ensure frontend has access to S3 credentials and Redis host.

Environment Variables and Secrets
Create .env files (root or per-service). Example variables:

Common

Code
API_PORT=8001
API_HOST=localhost
API_URL=localhost:8001
MongoDB

Code
MONGODB_URL=mongodb://<user>:<pass>@mongodb:27017/<db>
MONGODB_USERNAME=<user>
MONGODB_PASSWORD=<pass>
MONGODB_DB=<db>
Redis

Code
REDIS_HOST=redis
REDIS_PORT=6379
S3

Code
S3_MARKDOWNAPP_BUCKETNAME=<bucket-name>
S3_MARKDOWNAPP_REGION=<region>
S3_MARKDOWNAPP_FOLDER=<folder-prefix>
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
Other

Code
ELASTIC_URL=<if using Elasticsearch>
API_PORT_FRONTEND=8000
Security: never commit .env to the repo. Use Render/Vercel environment variable settings for production.

Healthchecks, Testing, CI, and Deployment
Healthchecks: use /availability for readiness probes in Render and container healthchecks in docker-compose.

