"""
Short identifier of a URL
"""

from __future__ import annotations

import random
import string


class ShortId(str):
    """A 7 character ID"""

    ID_LENGTH = 7

    @classmethod
    def new(cls) -> ShortId:
        new_id = ""
        for _ in range(cls.ID_LENGTH):
            new_id += random.choice(string.ascii_letters)
        return ShortId(new_id)
