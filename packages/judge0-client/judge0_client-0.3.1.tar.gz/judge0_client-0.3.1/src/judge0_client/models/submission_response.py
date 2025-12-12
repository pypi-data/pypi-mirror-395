from .base_response_model import BaseResponseModel


class SubmissionResponse(BaseResponseModel):
    """Response for non-waiting submission — contains only a token."""

    token: str
