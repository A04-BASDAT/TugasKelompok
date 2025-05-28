import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Print all environment variables (excluding sensitive values)
print("All environment variables:", [k for k in os.environ.keys()])

# Try to load from .env file as fallback for local development
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

print("Current working directory:", os.getcwd())
print("Base directory:", BASE_DIR)

# Try getting variables directly and from specific sources
url: str = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY") or os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

print("Supabase URL exists:", url is not None)
print("Supabase Key exists:", key is not None)
print("Supabase URL length:", len(url) if url else 0)
print("Supabase Key length:", len(key) if key else 0)

if not url or not key:
    raise Exception("Missing Supabase credentials. Please check your environment variables.")

supabase: Client = create_client(url, key)