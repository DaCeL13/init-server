from pydantic import BaseModel
from typing import Optional, Any

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
