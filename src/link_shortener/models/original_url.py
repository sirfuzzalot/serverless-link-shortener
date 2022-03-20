"""
Original URL request body
"""
from pydantic import BaseModel, HttpUrl


class OriginalUrl(BaseModel):
    """The original long URL"""

    url: HttpUrl
