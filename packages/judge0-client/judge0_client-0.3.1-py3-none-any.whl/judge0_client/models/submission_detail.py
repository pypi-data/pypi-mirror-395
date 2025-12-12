from typing import Self
from .base_response_model import BaseResponseModel
from .submission_status import SubmissionStatus
from ..utils.base64_utils import base64_decode


class SubmissionDetail(BaseResponseModel):
    """Detailed information about submission execution."""

    token: str
    status: SubmissionStatus
    stdout: str | None = None
    stderr: str | None = None
    compile_output: str | None = None
    message: str | None = None
    time: float | None = None
    memory: int | None = None
    exit_code: int | None = None
    language_id: int | None = None

    def decode_base64(self) -> Self:
        return self.model_copy(update={
            "stdout": base64_decode(self.stdout) if self.stdout else self.stdout,
            "stderr": base64_decode(self.stderr) if self.stderr else self.stderr,
            "compile_output": base64_decode(self.compile_output) if self.compile_output else self.compile_output,
            "message": base64_decode(self.message) if self.message else self.message,
        })
