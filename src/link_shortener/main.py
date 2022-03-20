"""
Entrypoint for API
"""
import logging
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse

from mangum import Mangum

from .store import make_store
from .utils import build_url
from .models import ShortId, ShortUrl, OriginalUrl, ErrorMessage


log = logging.getLogger("link_shortener")
log.propagate = False
log.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(message)s"))
log.addHandler(stream_handler)

prefix = ""
stage = os.environ.get("STAGE")
if os.environ.get("AWS_EXECUTION_ENV") and stage and not os.environ.get("DOMAIN_NAME"):
    prefix = f"/{stage}"

app = FastAPI(
    title="Link Shortener",
    version="0.1.0",
    description=(
        "This service takes URLs and provides a shortened version in return. "
        + "The shortened URL can then be exchanged for the original URL."
    ),
    root_path=prefix,
)


if not os.environ.get("URL_TABLE"):
    log.info("Using Memory Store")
    db = make_store()
else:
    log.info("Using DynamoDB Store")
    db = make_store("dynamodb")


@app.post(
    "/",
    status_code=201,
    responses={
        "201": {"model": ShortUrl, "description": "Successfully created short URL"}
    },
)
def create_short_url(
    original_url: OriginalUrl,
    request: Request,
) -> ShortUrl:
    """
    Submit a URL and receive back a shortened URL
    """
    url_id = db.save_url(original_url.url)
    return ShortUrl(url=build_url(url_id, request.url))


@app.get(
    "/{url_id}",
    status_code=308,
    responses={
        "308": {"model": None, "description": "Redirect to original URL"},
        "404": {"model": ErrorMessage, "description": "Original URL not Found"},
    },
)
def get_original_url(url_id: ShortId) -> RedirectResponse:
    """
    Exchange a short URL for the original URL
    """
    url = db.get_url(url_id)
    if not url:
        raise HTTPException(status_code=404, detail="Original URL not Found")
    return RedirectResponse(url, status_code=308)


handler = Mangum(app)
