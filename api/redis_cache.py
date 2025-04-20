import redis
import json
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def generate_cache_key(skills: str, experience: str, location: str) -> str:
    key_raw = f"{skills.lower()}_{experience}_{location.lower()}"
    key_hashed = hashlib.sha256(key_raw.encode()).hexdigest()
    return f"search:{key_hashed}"

def get_cached_search_result(skills: str, experience: str, location: str):
    cache_key = generate_cache_key(skills, experience, location)
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

def set_cached_search_result(skills: str, experience: str, location: str, results: list, ttl: int = 3600):
    cache_key = generate_cache_key(skills, experience, location)
    redis_client.setex(cache_key, ttl, json.dumps({"results": results}))

def clear_all_search_cache():
    for key in redis_client.scan_iter("search:*"):
        redis_client.delete(key)
