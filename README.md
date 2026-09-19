# Markdown Editor Monorepo

This repository contains two services that run together via the root `docker compose` configuration:

- `/backend` — Async FastAPI backend (models, DB calls, API endpoints).  
- `/frontend` — Frontend service (form UI, rate limiter, S3 helpers) or Next.js app (UI, image parsing, S3 uploads).  

Use the root `docker compose` to build and run both services plus Redis and MongoDB for local development.

---

## One‑line summary
Async FastAPI backend + frontend for a modular Markdown editor. Backend stores posts in MongoDB and exposes async endpoints; frontend handles the user form, image parsing, S3 uploads, and Redis‑backed rate limiting. Both services are containerized and orchestrated from the repository root.

---

## Quickstart (run everything from repo root)

1. **Create env files**
   - Root: optional (you can set envs in service `.env` files).  
   - `/backend/.env` and `/frontend/.env` — see **Environment variables** below.

2. **Build and run all services**
   ```bash
   docker compose up --build
   ```

3. **Verify health**
   - Backend health (example):
     ```bash
     curl http://localhost:${API_PORT:-8001}/availability
     ```
     Expected: `{"status":"ok"}`
   - Frontend health (if frontend exposes `/availability`):
     ```bash
     curl http://localhost:${APP_PORT:-8000}/availability
     ```

4. **Stop**
   ```bash
   docker compose down
   ```

---

## Services (as defined in root docker compose)
- **frontend** (`markdown-app-frontend`)  
  - Build context: `./frontend`  
  - Exposes port `${APP_PORT}:8000` (set `APP_PORT` in `.env` or use default 8000).  
  - Uses `./frontend/.env` and environment variables for AWS credentials and S3 region.  
  - Depends on `backend` and `redis` (waits for healthy services).

- **backend** (`markdown-app-backend`)  
  - Build context: `./backend`  
  - Exposes port `${API_PORT}:8001` (set `API_PORT` in `.env` or use default 8001).  
  - Uses `./backend/.env`.  
  - Healthcheck: `http://markdown-app-backend:8001/user/create_new?q=tobi@gmail.com` (container internal check).  
  - Depends on `mongodb`.

- **redis** (`markdown-app-redis`)  
  - Image: `redis:alpine`  
  - Exposes `${REDIS_PORT}:${REDIS_PORT}` (set `REDIS_PORT` in `.env`).

- **mongodb** (`markdown-app-mongodb`)  
  - Image: `mongodb/mongodb-community-server:latest`  
  - Exposes `27017:27017`  
  - Initializes with `mongo-init.js` and environment variables for root user and DB.

---

## Environment variables

Create `/backend/.env` and `/frontend/.env` with the variables below. Do **not** commit `.env` files.

**Backend (`/backend/.env`)**
```
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
```

**Frontend (`/frontend/.env`)**
```
APP_PORT=8000
API_URL=http://localhost:8001
REDIS_HOST=redis
REDIS_PORT=6379
S3_MARKDOWNAPP_BUCKETNAME=<bucket-name>
S3_MARKDOWNAPP_REGION=<region>
S3_MARKDOWNAPP_FOLDER=<folder-prefix>
ACCESS_KEY=<aws-access-key>
SECRET_KEY=<aws-secret-key>
```

**Root / Compose environment (optional)**
```
API_PORT=8001
APP_PORT=8000
REDIS_PORT=6379
MONGODB_USERNAME=<root-user>
MONGODB_PASSWORD=<root-pass>
MONGODB_DB=<db>
MONGODB_CUSTOM_USERNAME=<app-user>
MONGODB_PASSWORD=<app-user-pass>
```

---

## Key endpoints (local)
- **Backend**
  - `GET /availability` — healthcheck  
  - `GET /user/create_new?q=<email>` — create/upsert user record  
  - `POST /user/add_post/{email}` — save a user’s post (expects JSON array of blocks)  
  - `GET /get-user-post/{user_id}` — fetch stored post by email

- **Frontend**
  - `GET /markdown-form/{user_email}` — render input form (frontend route)  
  - `POST /processing-page/{email}` — process form, upload images to S3, call backend `/user/add_post/{email}`  
  - (Optional) `GET /availability` — frontend health (if implemented)

---

## Data model (posts)
Posts are ordered lists of block objects:
```json
{
  "type": "h1" | "h2" | "p" | "ul" | "img",
  "position": 0,
  "content": "..."
}
```
- **Images**: validated extensions (`png`, `jpg`, `jpeg`, `webp`, `gif`), max size **5 MB**, filenames replaced with UUIDs before upload.  
- **S3 URL**: `https://{BUCKET}.s3.{REGION}.amazonaws.com/{FOLDER}/{filename}`

---

## Operational notes & recommended fixes
- **Non‑atomic S3 deletion**: current flow deletes old images after new upload; consider moving deletions to a background worker (Celery + RabbitMQ) or queue to avoid partial failures.  
- **Rate limiting**: implemented in frontend using Redis; adjust window/limit for local testing.  
- **Logging & metrics**: replace `print()` timing with structured logs and expose request duration metrics.  
- **Retries & idempotency**: add retry/backoff for S3 and DB calls and idempotency keys for repeated requests.  
- **Security**: use least‑privilege IAM credentials for S3; prefer pre‑signed URLs if moving uploads to clients.

---

## Troubleshooting
- **Service logs**
  ```bash
  docker compose logs backend
  docker compose logs frontend
  docker compose logs redis
  docker compose logs mongodb
  ```
- **Common issues**
  - Mongo connection errors: verify `MONGODB_URL` and that `mongodb` container is healthy.  
  - Redis errors: verify `REDIS_HOST`/`REDIS_PORT` and container health.  
  - S3 upload failures: verify AWS credentials, bucket name, and region.  
  - Rate limiter blocking during dev: reduce limits or clear Redis keys.

---

## Contributing & license
- Fork → feature branch → add tests → open PR.  
- Add `CONTRIBUTING.md` and `LICENSE` (MIT recommended).

---

