import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent

print("Current working directory:", os.getcwd())
print("Base directory:", BASE_DIR)

# Load .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

print("Supabase URL:", url) 
print("Supabase Key:", key[:5] + "..." if key else "missing")  # Shows first 5 chars of key if exists

supabase: Client = create_client(url, key)