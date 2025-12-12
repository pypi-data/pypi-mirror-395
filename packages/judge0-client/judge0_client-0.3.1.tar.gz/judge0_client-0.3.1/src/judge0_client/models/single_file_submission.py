from typing import Any, Mapping
from pydantic import BaseModel, Field
from .base_submission import BaseSubmission
from ..utils.base64_utils import base64_encode
from ..utils.zip_utils import create_encoded_zip


class SingleFileSubmission(BaseSubmission, BaseModel):
    """Request model for creating a single-file submission in Judge0."""

    source_code: str = Field(description="Program’s source code")
    language_id: int = Field(description="Programming language ID")
    additional_files: Mapping[str, str | bytes] | None = Field(
        default=None,
        description="Additional files that should be available alongside the source code (encoded zip)"
    )

    def to_body(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        fields_to_encode = ["source_code", "stdin", "expected_output"]
        for f in fields_to_encode:
            if f in data and data[f] is not None:
                data[f] = base64_encode(data[f])
        if "additional_files" in data:
            data["additional_files"] = create_encoded_zip(data["additional_files"])
        return data
