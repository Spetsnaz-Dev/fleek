from fastapi import APIRouter, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.job import JobCreate, JobStatusResponse
from app.models.job import Job
from app.core.db import AsyncSessionLocal
from app.tasks.job_tasks import process_job

router = APIRouter()

@router.post("/generate", response_model=JobStatusResponse)
async def create_job(job_in: JobCreate):
    async with AsyncSessionLocal() as session:
        job = Job(
            prompt=job_in.prompt,
            status='queued'
        )
        session.add(job)
        await session.commit()
        await session.refresh(job)
        # Enqueue background job
        process_job.send(job.id)
        return JobStatusResponse(
            job_id=job.id, status=job.status, result_url=None, error_message=None, retry_attempts=0
        )

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def check_status(job_id: int):
    async with AsyncSessionLocal() as session:
        job: Job = await session.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return JobStatusResponse(
            job_id=job.id,
            status=job.status,
            result_url=job.result_url,
            error_message=job.error_message,
            retry_attempts=job.retry_attempts,
        )
