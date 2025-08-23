import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def write_log_to_supabase(timestamp):
    data = {
        "prediction_time": timestamp
    }
    supabase.table("prediction_time_log").insert(data).execute()