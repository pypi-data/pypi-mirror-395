from pydantic import BaseModel, Field
from .base_response_model import BaseResponseModel


class AboutResponse(BaseResponseModel):
    version: str
    homepage: str
    source_code: str
    maintainer: str
