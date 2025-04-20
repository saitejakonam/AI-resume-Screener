from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
import time
from opensearchpy.exceptions import ConnectionError

load_dotenv()

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost").replace("http://", "").replace("https://", "")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASS = os.getenv("OPENSEARCH_PASS", "admin")

INDEX_NAME = "candidates"

def get_opensearch_client():
    return OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASS),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )

def ensure_resumes_index():
    retries = 100
    delay = 10

    for i in range(retries):
        try:
            client = get_opensearch_client()
            if not client.indices.exists(INDEX_NAME):
                client.indices.create(index=INDEX_NAME, body={
                    "mappings": {
                        "properties": {
                            "name": {"type": "text"},
                            "email": {"type": "keyword"},
                            "skills": {"type": "text"},
                            "experience": {"type": "text"},
                            "location": {"type": "text"},
                            "job_id": {"type": "integer"},
                            "resume_id": {"type": "keyword"}
                        }
                    }
                })
            return
        except ConnectionError as e:
            print(f"🔁 OpenSearch not ready, retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

    raise Exception("❌ OpenSearch is not ready after multiple retries")

def index_candidate(candidate_id: str, candidate_dict: dict):
    client = get_opensearch_client()
    client.index(index=INDEX_NAME, id=candidate_id, body=candidate_dict)

def search_candidates(job_description: str, job_id: int):
    client = get_opensearch_client()
    return client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": job_description,
                                "fields": ["skills", "experience", "location"]
                            }
                        },
                        {
                            "term": {"job_id": job_id}
                        }
                    ]
                }
            },
            "sort": [
                {"_score": {"order": "desc"}}
            ]
        }
    )



def search_resumes(skills: str = "", experience: str = "", location: str = ""):
    client = get_opensearch_client()

    must_clauses = []

    if skills:
        must_clauses.append({"match": {"skills": skills}})
    if experience:
        must_clauses.append({"match": {"experience": experience}})
    if location:
        must_clauses.append({"match": {"location": location}})

    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    return client.search(index=INDEX_NAME, body=query)
