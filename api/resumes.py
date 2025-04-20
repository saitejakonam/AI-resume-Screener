from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db
from cloudinary_utils import upload_to_cloudinary
from resume_parser import extract_resume_text
from llm_utils import extract_candidate_metadata
from models import CandidateMetadata, Job
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import logging
from opensearch_utils import index_candidate as opensearch_index_candidate
from opensearch_utils import search_candidates
from cloudinary.utils import cloudinary_url
from redis_cache import (
    get_cached_search_result,
    set_cached_search_result
)
from redis_cache import clear_all_search_cache
import os
from dotenv import load_dotenv
from opensearch_utils import search_resumes  # add this if not already


load_dotenv()

router = APIRouter(prefix="/resumes", tags=["Resumes"])

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_collection = mongo_client["resume_db"]["resumes"]


@router.post("/upload/{job_id}")
async def upload_resumes_for_job(
    job_id: int,
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    created_candidates = []

    for file in files:
        filename = file.filename or ""
        print("File received:", filename)

        # Validate extension
        if not filename.lower().endswith((".pdf", ".docx")):
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF or DOCX files are supported. Got: {filename}"
            )

        content = await file.read()

        # Upload to Cloudinary
        cloudinary_url = upload_to_cloudinary(filename, content)

        # Extract text
        text = extract_resume_text(file.content_type, content, file.filename)

        # Save raw resume in MongoDB
        raw_doc = {
            "job_id": job_id,
            "filename": filename,
            "url": cloudinary_url,
            "content_type": file.content_type,
            "uploaded_at": datetime.utcnow().isoformat() + "Z",
            "text": text
        }
        mongo_result = mongo_collection.insert_one(raw_doc)
        resume_id = str(mongo_result.inserted_id)
        cloud_url = upload_to_cloudinary(filename, content)  # This now returns the full secure URL

        # Extract structured metadata using Gemini
        metadata = extract_candidate_metadata(text)
        print("[LLM Metadata]", metadata)

        skills = metadata.get("Skills", [])
        skills_str = ", ".join(skills) if isinstance(skills, list) else ""

        candidate = CandidateMetadata(
            name=metadata.get("FullName"),
            email=metadata.get("Email Address"),
            skills=skills_str,
            experience=str(metadata.get("Years of Experience")),
            location=metadata.get("Location"),
            resume_id=cloud_url,
            job_id=job_id
        )
        db.add(candidate)
        await db.commit()
        await db.refresh(candidate)
        created_candidates.append(candidate)

        # Index to OpenSearch
        opensearch_index_candidate(
            candidate_id=str(candidate.id),
            
            candidate_dict={
            "name": candidate.name,
            "email": candidate.email,
            "skills": candidate.skills,
            "experience": candidate.experience,
            "location": candidate.location,
            "resume_id": candidate.resume_id,
            "job_id": candidate.job_id,
            "sql_id": candidate.id
        })

    clear_all_search_cache()

    return {"message": f"{len(created_candidates)} resumes uploaded and processed."}



@router.get("/job/{job_id}")
async def get_candidates_for_job(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateMetadata).where(CandidateMetadata.job_id == job_id))
    candidates = result.scalars().all()

    enriched = []
    for c in candidates:
        resume = mongo_collection.find_one({"_id": ObjectId(c.resume_id)})
        enriched.append({
            "name": c.name,
            "email": c.email,
            "skills": c.skills,
            "experience": c.experience,
            "location": c.location,
            "resume_url": resume.get("url") if resume else None,
            "uploaded_at": resume.get("uploaded_at") if resume else None
        })

    return {"job_id": job_id, "candidates": enriched}


@router.get("/rank_candidates")
async def rank_candidates(job_id: int, db: AsyncSession = Depends(get_db)):
    job_result = await db.execute(select(Job).where(Job.id == job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    response = search_candidates(job.description, job.id)
    if "hits" not in response or "hits" not in response["hits"]:
        raise HTTPException(status_code=500, detail="Failed to retrieve ranking from OpenSearch")

    ranked = sorted(
        [
            {
                "candidate_id": hit["_source"].get("sql_id"),
                "score": hit["_score"],
                "data": hit["_source"]
            }
            for hit in response["hits"]["hits"]
        ],
        key=lambda x: x["score"],
        reverse=True
    )

    print("🔍 OpenSearch Response Hits:", response["hits"]["hits"])


    return {"job_id": job_id, "ranked_candidates": ranked}


logger = logging.getLogger("search_logger")


@router.get("/search")
async def search_candidate(
    skills: str = "",
    experience: str = "",
    location: str = ""
):
    # 🔁 Try to fetch from Redis cache
    cached = get_cached_search_result(skills, experience, location)
    if cached:
        logger.info(f"✅ Redis HIT for skills={skills}, experience={experience}, location={location}")
        return cached

    logger.info(f"❌ Redis MISS for skills={skills}, experience={experience}, location={location}")

    # 🔍 Perform OpenSearch query
    response = search_resumes(skills, experience, location)

    if "hits" not in response or "hits" not in response["hits"]:
        raise HTTPException(status_code=500, detail="Search failed.")

    # 🔄 Remove duplicates based on email
    seen_emails = set()
    unique_results = []

    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        email = source.get("email")

        if email and email not in seen_emails:
            unique_results.append({
                "candidate_id": hit["_id"],
                "score": hit["_score"],
                "data": source
            })
            seen_emails.add(email)

    output = {"results": unique_results}

    # 💾 Cache the unique result for 10 minutes
    set_cached_search_result(skills, experience, location, output, ttl=600)

    return output


# v1/resumes.py or v1/view_resume.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import CandidateMetadata


@router.get("/view/{candidate_id}")
async def view_resume(candidate_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateMetadata).where(CandidateMetadata.id == candidate_id))
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {
        "resume_url": candidate.resume_id,  # Already stores full Cloudinary URL
        "metadata": {
            "name": candidate.name,
            "email": candidate.email,
            "skills": candidate.skills,
            "experience": candidate.experience,
            "location": candidate.location
        }
    }
