"""
VeriskGO SDK – Public API
This exposes only the clean, stable functions you want users to import.
"""
# veriskgo/__init__.py
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("veriskgo")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Trace Manager
from .trace_manager import TraceManager

# Import the track_function decorator
from .trace_manager import track_function

# Export SQS sender
from .sqs import send_to_sqs

# User profile span helper
from .user import user_profile_span

# Models
from .models import UserProfile
from .llm import track_llm_call
from .langchain_tracker import track_langchain

__all__ = [
    "TraceManager",
    "track_function",
    "send_to_sqs",
    "user_profile_span",
    "UserProfile",
    "track_llm_call", 
    "track_langchain",
]
