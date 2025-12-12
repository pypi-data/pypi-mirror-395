# veriskgo/user.py
from typing import Dict, Any
from .sqs import send_to_sqs
from .models import UserProfile
import uuid

def user_profile_span(profile: UserProfile) -> dict:
    """Return a Langfuse span representing user profile creation/update."""
    
    return {
        "span_id": str(uuid.uuid4()).replace("-", ""),
        "name": "user_profile_update",
        "type": "span",
        "input": {
            "profile": profile.to_dict()
        },
        "output": {
            "status": "updated"
        },
        "metadata": {
            "span_type": "user_profile"
        }
    }