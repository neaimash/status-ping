from pydantic import BaseModel
from typing import Optional, Literal

class Target(BaseModel):
    name: str
    url: str
    critical: bool

class Status(BaseModel):
    name: str
    url: str
    status: Literal["UP", "DOWN"]
    latency: Optional[int]
    critical: bool
