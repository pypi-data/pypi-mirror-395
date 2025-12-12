# veriskgo/models.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class UserProfile:
    user_id: str  # REQUIRED

    # Optional fields
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
 
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a clean dict (ignoring None fields)."""
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "location": self.location,
            "metadata": self.metadata,
        }
 
        return {k: v for k, v in data.items() if v is not None}
