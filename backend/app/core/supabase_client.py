from supabase import create_client, Client
from app.core.config import settings

# Supabase client used for Storage uploads (server-side, uses service_role key)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
