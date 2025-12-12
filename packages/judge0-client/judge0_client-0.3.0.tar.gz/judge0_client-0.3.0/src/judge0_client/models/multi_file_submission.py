from typing import Any, Literal, Mapping
from pydantic import BaseModel, Field
from .base_submission import BaseSubmission
from ..utils.base64_utils import base64_encode
from ..utils.zip_utils import create_encoded_zip


class MultiFileSubmission(BaseSubmission, BaseModel):
    """Request model for creating a multi-file submission in Judge0."""

    language_id: Literal[89] = Field(default=89, description="Programming language ID")
    additional_files: Mapping[str, str | bytes] = Field(
        description="Scripts to run and compile and additional files"
    )

    def to_body(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        fields_to_encode = ["stdin", "expected_output"]
        for f in fields_to_encode:
            if f in data and data[f] is not None:
                data[f] = base64_encode(data[f])
        if "additional_files" in data:
            data["additional_files"] = create_encoded_zip(data["additional_files"])
        return data
