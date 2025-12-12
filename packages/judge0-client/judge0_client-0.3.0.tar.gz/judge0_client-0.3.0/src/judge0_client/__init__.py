"""Judge0 client package.

Provides `Judge0Client` for interacting with the Judge0 API
and Pydantic models for requests and responses.
"""

from .client import Judge0Client
from .utils.exceptions import Judge0Error
from .models.base_submission import BaseSubmission
from .models.single_file_submission import SingleFileSubmission
from .models.multi_file_submission import MultiFileSubmission
from .models.submission_response import SubmissionResponse
from .models.submission_detail import SubmissionDetail
from .models.workers_response import WorkersResponse
from .models.about_response import AboutResponse
from .types import SubmissionStatusId

__all__ = [
    "Judge0Client",
    "Judge0Error",
    "BaseSubmission",
    "SingleFileSubmission",
    "MultiFileSubmission",
    "SubmissionResponse",
    "SubmissionDetail",
    "SubmissionStatusId",
    "WorkersResponse",
    "AboutResponse",
]
