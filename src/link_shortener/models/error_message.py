"""
Generic Error Message
"""
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """Error Message"""

    detail: str
