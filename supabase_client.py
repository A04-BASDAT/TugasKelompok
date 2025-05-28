import os
from supabase import create_client, Client
from dotenv import load_dotenv

print("Current working directory:", os.getcwd())

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

print("Supabase URL:", url) 
print("Supabase Key:", key[:5] + "..." if key else "missing")  # Shows first 5 chars of key if exists

supabase: Client = create_client(url, key)