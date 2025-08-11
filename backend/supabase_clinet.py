from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_verified_ngo(name, reg_id, wallet_address):
    return supabase.table("ngos").insert({
        "name": name,
        "registration_id": reg_id,
        "blockchain_address": wallet_address,
        "verified": True
    }).execute()
