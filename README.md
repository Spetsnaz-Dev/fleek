# Async Media Generator (Fleek)

Queue-based async Text-to-Image generator using Replicate APIs, FastAPI, Dramatiq, PostgreSQL, and Redis.

---

## Features

- **Async API** for submitting text prompts and checking job status
- **Background job processing** with Dramatiq and Redis
- **PostgreSQL** for job persistence
- **Media storage** (local, extensible to S3/MinIO)
- **Dockerized** for easy deployment
- **Swagger UI** for easy testing of APIs and docs


Implemented everything that is asked in assignment except Alembic for migration(was not able to configure it properly)
---

## Quick Start (Docker)

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Spetsnaz-Dev/fleek.git
   cd fleek
   ```

2. **Set up environment variables:**

   - Copy the example below into a `.env` file (edit as needed):
     ```env
     DATABASE_URL=postgresql+asyncpg://ravindra:password@db:5432/fleek
     REDIS_URL=redis://redis:6379/0
     STORAGE_BACKEND=local
     LOCAL_MEDIA_PATH=media
     REPLICATE_API_TOKEN=your_replicate_api_token // currently using mock API
     ```

3. **Build and run everything:**

   ```sh
   docker compose up --build
   ```

   This will start:

   - PostgreSQL (db)
   - Redis (redis)
   - FastAPI backend (backend)
   - Dramatiq worker (worker)

4. **Access the API docs and Try out:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## API Endpoints

### 1. Generate Image

- **POST** `/generate`

  ```curl
    curl --location 'http://localhost:8000/generate' \
    --header 'Content-Type: application/json' \
    --data '{
        "prompt": "A futuristic city at dusk"
  }'
  ```

- **Request Body:**
  ```json
  {
    "prompt": "A cat riding a bicycle"
  }
  ```
- **Response:**
  ```json
  {
    "job_id": 1,
    "status": "queued",
    "result_url": null,
    "error_message": null,
    "retry_attempts": 0
  }
  ```

### 2. Check Job Status

- **GET** `/status/{job_id}`
- **Response:**
  ```json
  {
    "job_id": 1,
    "status": "completed",
    "result_url": "media/1_output.png",
    "error_message": null,
    "retry_attempts": 0
  }
  ```

  ```curl
  curl --location 'http://localhost:8000/status/2'
  ```

---

## Project Structure

```
app/
  api/endpoints.py      # API routes
  core/config.py        # Settings & env vars
  core/db.py            # DB engine/session
  models/job.py         # Job DB model
  schemas/job.py        # Pydantic schemas
  services/media.py     # Media storage logic
  tasks/job_tasks.py    # Background job logic
  main.py               # FastAPI app entrypoint
alembic/                # DB migrations
Dockerfile              # Docker build
requirements.txt        # Python dependencies
docker-compose.yml      # Multi-service orchestration
media/                  # Output images (local storage)
```

---

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `STORAGE_BACKEND` - Storage backend (default: `local`)
- `LOCAL_MEDIA_PATH` - Path for storing generated media (default: `./media`)
- `REPLICATE_API_TOKEN` - Your Replicate API token (dummy by default)

---

## Development

- **Local development:**
  - You can run the backend with `uvicorn app.main:app --reload` (requires PostgreSQL & Redis running)
  - Use Docker Compose for full stack
- **Migrations:**
  - Not Integrated - Could not configure Alembic

---

## Notes

- The current image generation is mocked; replace with real Replicate API calls as needed. Configure API calls inside `/app/tasks/job_tasks.py`
- Secrets and sensitive data were rejected by Git while commiting to git. Use `.env` sample provided in Readme.

---

## output_logs.log

`output_logs.log` contains some logs recorded during my development and testing phase. These logs demonstrate that if a task fails, it is automatically retries using exponential backoff.

## A concise summary of key logs, issues, and events encountered during the development of this assignment:

- Resolved **Pydantic v2 breaking changes** by replacing `BaseSettings` import with `pydantic_settings` and installing `pydantic-settings` package.
- Encountered multiple Alembic/SQLModel error:
  - SQLModel couldn't handle `Dict` type for the `parameters` field in the `Job` model. Fixed by using: `sa_column=Column(JSON, nullable=True)`  
    and importing SQLAlchemy's `JSON` type.
- Skipped Alembic migrations for now(Got too much frustrated regarding it's setup):
- Fixed issues with environment variables not loading.
- Resolved `asyncio`-related runtime errors.
