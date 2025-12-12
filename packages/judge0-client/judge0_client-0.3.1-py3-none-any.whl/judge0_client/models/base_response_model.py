from typing import Self
from pydantic import BaseModel
import httpx


class BaseResponseModel(BaseModel):
    """Detailed information about submission execution."""

    @classmethod
    def from_response(cls, resp: httpx.Response) -> Self:
        return cls.model_validate(resp.json())

    @classmethod
    def from_response_list(cls, resp: httpx.Response) -> list[Self]:
        return [cls.model_validate(r) for r in resp.json()]
