import requests

# Placeholder: Use NGO Darpan or any government API
def verify_ngo_darpan(reg_id):
    # For demo, assume if reg_id starts with "NGO", it's valid
    if reg_id.startswith("NGO"):
        return {
            "name": "Demo NGO Foundation",
            "valid": True
        }
    else:
        return {
            "name": None,
            "valid": False
        }
