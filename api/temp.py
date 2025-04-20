from sqlalchemy.future import select
from models import CandidateMetadata
from database import SessionLocal
import asyncio

async def check_candidates():
    async with SessionLocal() as session:
        result = await session.execute(select(CandidateMetadata))
        candidates = result.scalars().all()
        for c in candidates:
            print({
                "name": c.name,
                "email": c.email,
                "skills": c.skills,
                "experience": c.experience,
                "location": c.location,
                "resume_id": c.resume_id,
                "job_id": c.job_id,
            })

asyncio.run(check_candidates())
