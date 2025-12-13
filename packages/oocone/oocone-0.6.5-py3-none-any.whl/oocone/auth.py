"""Defines the Auth class."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

import aiohttp
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from oocone import errors

if TYPE_CHECKING:
    from typing import Any

ROUTE_LOGIN = "/signinForm.php?mode=ok"
BEAUTIFULSOUP_PARSER = "html.parser"

logger = logging.getLogger(__name__)


class Auth:
    """Acquires authentication for the dashboard and makes authenticated requests."""

    def __init__(
        self,
        *,
        base_url: str,
        username: str,
        password: str,
        websession: aiohttp.ClientSession | None = None,
    ) -> None:
        """
        Create a new instance.

        Params:
            base_url: The URL on which the enocoo dashboard is available, e.g.
                ``https://ems123.enocoo.com:12345``. This will be used to initialize the
                [`base_url`][oocone.auth.Auth.base_url] attribute.
            username: The username to use for logging in to the dashboard.
            password: The password to use for logging in to the dashboard.
            websession: Allows customization of the used web session. If unset, a new session will
                be created internally.
        """
        self._base_url = base_url.rstrip("/")
        self.__username = username
        self.__password = password
        self._session = websession or aiohttp.ClientSession()
        self._logged_in = False

    @property
    def base_url(self) -> str:
        """The URL on which the enocoo dashboard is available."""
        return self._base_url

    @staticmethod
    def _response_indicates_not_logged_in(response: BeautifulSoup) -> bool:
        if response.title is not None and "abgemeldet" in response.title.text.lower():
            return True
        if response.find("input", {"type": "password"}) is not None:  # noqa: SIM103
            return True

        return False

    async def _login(self) -> None:
        async with self._session.post(
            self._base_url + ROUTE_LOGIN,
            data={"user": self.__username, "passwort": self.__password},
        ) as response:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, features=BEAUTIFULSOUP_PARSER)
            if self._response_indicates_not_logged_in(soup):
                raise errors.AuthenticationFailed

    async def request(
        self, method: str, path: str, *, retry_with_login: bool = True, **kwargs: Any
    ) -> tuple[aiohttp.ClientResponse, BeautifulSoup]:
        """
        Make a request.

        Params:
            method: The [HTTP request method](https://en.wikipedia.org/wiki/HTTP#Request_methods) to
                use, e.g. ``GET`` or ``POST``.
            path: The path of the resource to request, relative to the
                [`base_ref`][oocone.Auth.__init__].
            retry_with_login: If this option is set and the response indicates that the resource
                could not be fetched due to not being logged in, the method will log in and retry
                the request.
            kwargs: Will be passed to [`ClientSession.request()`][aiohttp.ClientSession.request].

        Returns:
            the raw response
            allows scraping of the response

        """
        try:
            logger.debug("=>       %s %s/%s", method.upper(), self._base_url, path)
            response = await self._session.request(
                method,
                f"{self._base_url}/{path}",
                **kwargs,
            )
        except aiohttp.client_exceptions.ClientError as e:
            raise errors.ConnectionIssue from e

        logger.debug("<= (%s) %s %s/%s", response.status, method.upper(), self._base_url, path)
        soup = BeautifulSoup(await response.text(), BEAUTIFULSOUP_PARSER)

        if self._response_indicates_not_logged_in(soup):
            if retry_with_login:
                await self._login()
                return await self.request(method, path, retry_with_login=False, **kwargs)

            raise errors.AuthenticationFailed

        return (response, soup)


# Some of the responses returned by enocoo trigger a BeautifulSoup warning. So we disable the
# warning, at least for the current module.
warnings.filterwarnings(
    action="ignore",
    category=MarkupResemblesLocatorWarning,
    module=__name__,
    append=True,
)
