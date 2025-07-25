import asyncio
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.models.job import Job
from app.services.media import get_media_client
from datetime import datetime
import httpx
import random
from dotenv import load_dotenv
load_dotenv()
# Dramatiq instace
redis_broker = RedisBroker(url=settings.REDIS_URL)
dramatiq.set_broker(redis_broker)

# Exponential backoff settings
MAX_RETRIES = 5
BACKOFF_BASE = 2

# async def call_replicate(prompt: str) -> bytes:
#     headers = {"Authorization": f"Token {settings.REPLICATE_API_TOKEN}"}
#     async with httpx.AsyncClient(follow_redirects=True) as client:
#         response = await client.get(f"https://picsum.photos/seed/{prompt}/512/512")
#         response = await client.post(settings.REPLICATE_API_URL, headers=headers)
#         response.raise_for_status()
#         # return response.content
#         return b"Random dummy image - " + prompt.encode()

async def replicate_generate_image(prompt: str) -> bytes:
    """
    Dummy Replicate API call (replace with real call by uncommenting the code)
    """
    await asyncio.sleep(2)
    # headers = {"Authorization": f"Token {settings.REPLICATE_API_TOKEN}"}
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(f"https://picsum.photos/200")
        response.raise_for_status()
        # message = response.content + prompt
        return b"Random dummy image - " + prompt.encode()
        # response = await client.post(settings.REPLICATE_API_URL, headers=headers)
        # return response.content
        # print(f"response : {response.content}")

@dramatiq.actor(max_retries=MAX_RETRIES)
def process_job(job_id: int):
    """
    Dramatiq for async processing with exponential backoff.
    """
    asyncio.run(_process_job_async(job_id))

async def _process_job_async(job_id: int):
    # Start DB session
    async with AsyncSessionLocal() as session:
        job: Job = await session.get(Job, job_id)
        if not job:
            return

        job.status = "in_progress"
        job.started_at = datetime.utcnow()
        await session.commit()

        # start generation process
        try:
            # Call Replicate (currently -> mocked it)
            image_bytes = await replicate_generate_image(job.prompt)

            media_client = get_media_client()
            filename = f"{job_id}_output.png"
            result_path = await media_client.save(filename, image_bytes)
            job.status = "completed"
            job.result_url = result_path
            job.finished_at = datetime.utcnow()
        except Exception as e:
            # Automatic retry -> we record tthe retries for future debug
            job.retry_attempts += 1
            job.status = "failed"
            job.error_message = str(e)
        finally:
            await session.commit()
