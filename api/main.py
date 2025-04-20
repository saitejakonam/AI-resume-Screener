from fastapi import FastAPI
from jobs import router as jobs_router
from resumes import router as resume_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(jobs_router)
app.include_router(resume_router)

from opensearch_utils import ensure_resumes_index
ensure_resumes_index()

import logging

logging.basicConfig(level=logging.INFO)
