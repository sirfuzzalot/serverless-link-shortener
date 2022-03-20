"""
DynamoDB Database for production
"""
import logging
import os
import time
from typing import Union

import boto3
from pydantic import HttpUrl

from ..models import ShortId
from ..utils import call_with_backoff


log = logging.getLogger("url_shortener")


EXPIRATION = 172800  # seconds (2 days)


class DuplicateKeyError(Exception):
    """Key value already exists in Table"""


class DynamoDBStore:
    def __init__(self):
        self.dynamodb_client = boto3.resource("dynamodb")
        self.table = self.dynamodb_client.Table(os.environ["URL_TABLE"])

    def save_url(self, url: HttpUrl) -> ShortId:
        """Save the URL to the URL Table and produce its id"""
        key = boto3.dynamodb.conditions.Key("url")
        response = self.table.query(
            IndexName="urls", KeyConditionExpression=key.eq(url)
        )

        if items := response.get("Items"):
            url_id: str = items[0]["id"]
            log.info("Item exists id='%s'. Updating expiration.", url_id)
            self.table.put_item(
                Item={"url": url, "id": url_id, "expiration": make_record_expiration()}
            )
            return url_id

        try:
            url_id = call_with_backoff(self._get_new_url_id)
        except RuntimeError:
            raise RuntimeError(
                "After 3 attempts the Shortener did not generate a unique ID."
                + "or there was a connection issue"
            ) from None

        log.info("Creating new Item with id='%s'", url_id)
        self.table.put_item(
            Item={"url": url, "id": url_id, "expiration": make_record_expiration()}
        )
        return url_id

    def _get_new_url_id(self) -> ShortId:
        """Produce an unused Id for the URL"""
        url_id = ShortId.new()
        response = self.table.get_item(Key={"id": url_id})
        if response.get("Item"):
            raise DuplicateKeyError("URL ID Already Exists")
        return url_id

    def get_url(self, url_id: ShortId) -> Union[HttpUrl, None]:
        """Produce the original URL for a valid id"""
        response = self.table.get_item(Key={"id": url_id})
        return response.get("Item", {}).get("url")


def make_record_expiration() -> int:
    """Produce an expiration date from now"""
    return int(time.time()) + EXPIRATION
