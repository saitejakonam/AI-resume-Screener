from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# -----------------------
# Job Schemas
# -----------------------

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: str
    experience: Optional[str] = None
    location: Optional[str] = None


class JobOut(JobCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Use this instead of orm_mode in Pydantic v2


# -----------------------
# Candidate (optional)
# -----------------------

class CandidateMetadata(BaseModel):
    name: Optional[str]
    email: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    location: Optional[str]
    job_id: int
    resume_id: str

# -----------------------
# Resume Upload Response
# -----------------------

class ResumeUploadResponse(BaseModel):
    message: str
    id: str
    url: str
