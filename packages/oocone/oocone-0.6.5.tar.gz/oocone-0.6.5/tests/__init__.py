"""Tests suite for `oocone`."""

from pathlib import Path
from zoneinfo import ZoneInfo

from aiohttp import web, web_app
from aiohttp.test_utils import TestClient

MockApiClient = TestClient[web.Request, web_app.Application]
TESTS_DIR: Path = Path(__file__).parent
TIMEZONE = ZoneInfo("Europe/Berlin")

__all__ = [
    "TESTS_DIR",
    "TIMEZONE",
    "MockApiClient",
]
