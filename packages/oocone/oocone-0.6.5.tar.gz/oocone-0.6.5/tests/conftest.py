"""Common fixtures and settings for all tests."""

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from aiohttp import web
from aiohttp.typedefs import Handler
from pytest_aiohttp.plugin import AiohttpClient

from . import TESTS_DIR, MockApiClient

pytest_plugins = ("pytest_asyncio",)

signed_in = web.AppKey("signed_in", bool)


@dataclass
class MockApiParams:
    """Parameters indicating how the Mock API works."""

    response_data_root_path: Path = TESTS_DIR / "data" / "responses"
    """The directory containing all response data sets."""

    dataset_name: str = "one_area"
    """Name of the dataset in use."""

    @property
    def response_data_path(self) -> Path:
        """Path to the response data set currently in use."""
        return self.response_data_root_path / self.dataset_name


MOCK_API_DATASET_NAMES = [child.name for child in MockApiParams().response_data_root_path.iterdir()]


@pytest.fixture
def mock_api_params() -> MockApiParams:
    """Return the MockApiParams for the current test."""
    return MockApiParams()


def _signin_form(mock_api_params: MockApiParams) -> Handler:
    async def handler(request: web.Request) -> web.Response:
        response_path = mock_api_params.response_data_path / "signinForm.failure.php"
        response = web.Response()

        if request.method == "POST":
            data = await request.post()
            username = data.get("user")
            password = data.get("passwort")
            credentials_correct = username == "correct" and password == "correct"  # noqa: S105

            if credentials_correct and request.query.get("mode") == "ok":
                response_path = mock_api_params.response_data_path / "signinForm.success.php"
                response.set_cookie("logged_in", "true")

        with Path.open(response_path, "rb") as f:
            response.body = f.read()

        return response

    return handler


def _response_from_file(
    response_path: Path | str, *, needs_login: bool = True, params: MockApiParams
) -> Handler:
    original_response_path = response_path

    async def handler(request: web.Request) -> web.Response:
        if needs_login and request.cookies.get("logged_in") != "true":
            response_path = params.response_data_path / "newMeterTable.notLoggedIn.php"
        else:
            response_path = params.response_data_path / original_response_path

        response = web.Response()
        with Path.open(response_path, "rb") as f:
            response.body = f.read()

        return response

    return handler


def _get_meter_data_with_param(mock_api_params: MockApiParams) -> Handler:
    async def handler(request: web.Request) -> web.Response:
        if request.cookies.get("logged_in") != "true":
            response_path = mock_api_params.response_data_path / "newMeterTable.notLoggedIn.php"
        else:
            q = request.query
            response_path = (
                mock_api_params.response_data_path
                / f"getMeterDataWithParam.{q['mClass']}.{q['AreaId']}.{q['from']}.{q['intVal']}.php"
            )

        response = web.Response()
        with Path.open(response_path, "rb") as f:
            response.body = f.read()

        return response

    return handler


def _get_pv_data_details(mock_api_params: MockApiParams) -> Handler:
    async def handler(request: web.Request) -> web.Response:
        if request.cookies.get("logged_in") != "true":
            response_path = mock_api_params.response_data_path / "newMeterTable.notLoggedIn.php"
        else:
            q = request.query
            response_path = (
                mock_api_params.response_data_path
                / f"getPVDataDetails.GesamtverbrauchUndErzeugung.{q['from']}.{q['intVal']}.php"
            )

        response = web.Response()
        with Path.open(response_path, "rb") as f:
            response.body = f.read()

        return response

    return handler


def _post_new_meter_table(mock_api_params: MockApiParams) -> Handler:
    async def handler(request: web.Request) -> web.Response:
        response = web.Response()
        response.body = _new_meter_table_body(
            logged_in=request.cookies.get("logged_in") == "true",
            date=dt.date.fromisoformat(str((await request.post())["dateParam"])),
            mock_api_params=mock_api_params,
        )
        return response

    return handler


def _new_meter_table_body(
    *, mock_api_params: MockApiParams, logged_in: bool, date: dt.date, time: dt.time | None = None
) -> bytes:
    if not logged_in:
        response_path = mock_api_params.response_data_path / "newMeterTable.notLoggedIn.php"
    else:
        response_path = mock_api_params.response_data_path / "newMeterTable.php"

    with Path.open(response_path, "rb") as f:
        body = f.read()

    body = body.replace(b"01.01.2021", f"{date.day:02}.{date.month:02}.{date.year:04}".encode())
    if time is not None:
        body = body.replace(b"12:34:56", time.isoformat("seconds").encode())

    return body


@pytest.fixture
async def mock_api(mock_api_params: MockApiParams, aiohttp_client: AiohttpClient) -> MockApiClient:
    """Return a mock API instance."""
    app = web.Application()
    app[signed_in] = False

    app.router.add_post("/signinForm.php", _signin_form(mock_api_params))
    app.router.add_get(
        "/php/getTrafficLightStatus.php",
        _response_from_file("getTrafficLightStatus.php", params=mock_api_params, needs_login=False),
    )
    app.router.add_get(
        "/php/getMeterDataWithParam.php", _get_meter_data_with_param(mock_api_params)
    )
    app.router.add_get("/php/getPVDataDetails.php", _get_pv_data_details(mock_api_params))
    app.router.add_post("/php/newMeterTable.php", _post_new_meter_table(mock_api_params))
    app.router.add_get(
        "/php/ownConsumption.php", _response_from_file("ownConsumption.php", params=mock_api_params)
    )
    return await aiohttp_client(app)


@pytest.fixture
async def mock_auth(mock_api: MockApiClient):  # type: ignore[no-untyped-def] # noqa: ANN201
    """Return an Auth instance accessing a mock API."""
    # Importing oocone directly inside conftest.py breaks the typeguard plugin for pytest,
    # so we import it lazily. Because of this, we cannot give a return type hint :(
    from oocone import Auth  # noqa: PLC0415

    return Auth(
        websession=mock_api.session,
        base_url=str(mock_api.server.make_url("/")),
        username="correct",
        password="correct",  # noqa: S106
    )


def pytest_collection_modifyitems(items: list[Any]) -> None:
    """Apply additional metadata to tests."""
    for item in items:
        if "mock_api" in item.fixturenames:
            item.add_marker(pytest.mark.mock_api)
