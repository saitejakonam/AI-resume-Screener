from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

from sqlalchemy import Column, Integer, String, Text
from database import Base
from sqlalchemy import DateTime, func


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)  # Add index for faster searches
    description = Column(Text, nullable=False)
    required_skills = Column(String, nullable=False)  # ✅ Add this line
    experience = Column(String(50))
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅



class CandidateMetadata(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    skills = Column(Text)  # ✅ switch from String(500) to Text to allow long skill lists
    experience = Column(String(50), nullable=False)
    location = Column(String(100), nullable=True)

    resume_id = Column(String, nullable=False)  # ✅ MongoDB ObjectId (string)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)  # ✅ track which job this applies to

