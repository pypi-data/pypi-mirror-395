from pydantic import BaseModel
from ..types import SubmissionStatusId


class SubmissionStatus(BaseModel):
    id: SubmissionStatusId
    description: str
