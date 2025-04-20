from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas import JobCreate, JobOut
from models import Job
from utils import get_db  # direct import, not from utils

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobOut)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
):
    new_job = Job(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        experience=job.experience,
        location=job.location,
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

@router.get("/", response_model=list[JobOut])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    jobs = await db.execute(select(Job))
    return jobs.scalars().all()
