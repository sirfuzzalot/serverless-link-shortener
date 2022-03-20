"""
Shortened URL containing Id
"""
from pydantic import BaseModel, HttpUrl


class ShortUrl(BaseModel):
    """The shortened URL"""

    url: HttpUrl
