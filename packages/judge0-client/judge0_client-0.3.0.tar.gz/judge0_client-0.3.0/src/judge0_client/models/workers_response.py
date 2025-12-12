from pydantic import BaseModel, Field
from .base_response_model import BaseResponseModel


class WorkersResponse(BaseResponseModel):
    queue: str = Field(description="Queue name")
    size: int = Field(description="Queue size, number of submissions that are currently waiting to be processed")
    available: int = Field(description="Available number of workers")
    idle: int = Field(description="How many workers are idle")
    working: int = Field(description="How many workers are currently working")
    paused: int = Field(description="How many workers are paused")
    failed: int = Field(description="How many jobs failed")
