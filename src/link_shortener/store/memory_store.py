"""
In memory datastore for development
"""
from typing import Dict, Union

from pydantic import HttpUrl

from ..models import ShortId


class MemoryStore:
    def __init__(self):
        self.db: Dict[ShortId, HttpUrl] = {}

    def save_url(self, url: HttpUrl) -> ShortId:
        """Save URL in memory and return its Id"""
        for key, value in self.db.items():
            if value == url:
                return key
        for _ in range(3):
            url_id = ShortId.new()
            if not self.db.get(url_id):
                self.db[url_id] = url
                return url_id

        raise RuntimeError(
            "After 3 attempts the Shortener did not generate a unique ID"
        )

    def get_url(self, url_id: ShortId) -> Union[HttpUrl, None]:
        """Produce the original URL for the id if it exists"""
        url = self.db.get(url_id)
        return url
