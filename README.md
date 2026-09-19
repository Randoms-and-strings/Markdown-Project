# Markdown App Backend

Async FastAPI backend for a modular Markdown editor. The service stores user posts in MongoDB, uploads images to AWS S3, and exposes async endpoints consumed by a frontend. It includes Redis‑backed rate limiting, image validation (5 MB max), and a healthcheck at `/availability`. Deployed on Render with Docker support for local development.

---

## Tech Stack
- **Language / Framework:** Python, FastAPI (async)  
- **Database:** MongoDB (async pymongo)  
- **Cache / Rate limiting:** Redis  
- **Storage:** AWS S3 (aioboto3)  
- **Concurrency / HTTP client:** asyncio, aiohttp  
- **Deployment:** Render (backend), Vercel (frontend)  
- **Containerization:** Docker / docker-compose

---

## One‑line summary
Async FastAPI backend for a modular Markdown editor — stores posts in MongoDB, uploads images to S3, and serves async endpoints for a Next.js frontend. Deployed on Render.

---

## Quickstart (Local)

1. Clone the repo and create a `.env` file with the variables listed below.  
2. Build and run with Docker Compose:
   ```bash
   docker compose up --build
3. Verify service health:
  bash
  curl http://localhost:8001/availability
  Response: {"status":"ok"}

Required environment variables
env
MONGODB_URL=<mongodb-connection-string>
API_PORT=8001
API_HOST=localhost
API_URL=localhost:8001
REDIS_HOST=<redis-host>
REDIS_PORT=<redis-port>
S3_MARKDOWNAPP_BUCKETNAME=<bucket-name>
S3_MARKDOWNAPP_REGION=<region>
S3_MARKDOWNAPP_FOLDER=<folder-prefix>
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
Key Endpoints
GET /availability — healthcheck

GET /user/create_new?q=<email> — create user record (upsert)

POST /user/add_post/{email} — save a user’s post (expects JSON array of blocks)

GET /get-user-post/{user_id} — fetch stored post by email

GET /markdown-form/{user_email} — frontend form route (renders input form)

POST /processing-page/{email} — frontend processing route (handles file uploads, S3 upload, and calls /user/add_post/{email})

Data model
Posts are stored as ordered lists of block objects:

json
{
  "type": "h1" | "h2" | "p" | "ul" | "img",
  "position": 0,
  "content": "some content..."
}
Image uploads: validated extensions (png, jpg, jpeg, webp, gif), max size 5 MB, filenames replaced with UUIDs before upload.

S3 URL format: https://{BUCKET}.s3.{REGION}.amazonaws.com/{FOLDER}/{filename} — get_img_s3() builds public links.

Rate limiting
Redis‑backed limiter keyed by email.

Default window: 60 seconds.

Soft limit: 5 requests per window (configurable).

Behavior & important notes
Async design: backend uses async endpoints and async MongoDB client for concurrency and responsiveness.

Non‑atomic image deletion: old images are removed from S3 after new uploads; consider moving deletions to a background queue (Celery + RabbitMQ) to avoid partial failures.

Validation: server validates file types and sizes; additional input sanitization is recommended before rendering HTML.

Healthchecks: docker-compose includes healthchecks; Render should use /availability for readiness.

Testing & CI (recommended)
Add pytest tests for core flows: create_new, add_post, get-user-post, image parsing, and rate limiting.

Suggested test command:

bash
pytest tests/
Add a GitHub Actions workflow to run tests and lint on push/PR (run pytest, flake8/black).

Observability & reliability (recommended)
Add structured logging (request id, endpoint, duration, status).

Convert printed timing info to structured logs/metrics.

Add retry/backoff for external calls (S3, MongoDB) and idempotency keys for repeated requests.

Consider moving heavy or non‑critical work (image deletion, large uploads) to background workers.

Security
Use least‑privilege IAM credentials for S3 and prefer pre‑signed URLs if moving uploads to clients.

Keep server‑side validation for file types and sizes.

Sanitize user content before rendering to prevent XSS.

Protect sensitive endpoints with authentication if required.

Deployment notes
Render: configure healthcheck to /availability. Use environment variables for secrets.

Frontend: deployed on Vercel; static loading page is used to mitigate backend cold starts. Document this in the frontend README.

Contributing
Fork the repo.

Create a feature branch.

Add tests for new functionality.

Open a pull request.

License
Add a LICENSE file (MIT recommended for personal projects).
