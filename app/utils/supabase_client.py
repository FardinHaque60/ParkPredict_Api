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

def write_log_to_supabase(request_made, prediction_request):
    response = supabase.table("prediction_time_log").select("id", count="exact").execute()
    entry_count = response.count
    if entry_count >= 500:
        raise IndexError("Maximum number of entries (500) in prediction_time_log exceeded.")

    data = {
        "timestamp": request_made,
        "prediction_time": prediction_request
    }
    supabase.table("prediction_time_log").insert(data).execute()