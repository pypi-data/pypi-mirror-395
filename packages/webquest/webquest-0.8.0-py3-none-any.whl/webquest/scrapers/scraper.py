import asyncio
from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar, overload

from playwright.async_api import BrowserContext
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from webquest.browsers.browser import Browser

TSettings = TypeVar("TSettings", bound=BaseSettings)
TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)
TRaw = TypeVar("TRaw")


class Scraper(ABC, Generic[TSettings, TRequest, TResponse, TRaw]):
    """
    Abstract base class for web scrapers.

    This class defines the structure for a scraper, including fetching raw data
    and parsing it into a structured response. It handles the execution flow
    using a provided Browser instance.

    Type Parameters:
        TSettings: The type of the settings object.
        TRequest: The type of the request object.
        TResponse: The type of the parsed response object.
        TRaw: The type of the raw data fetched from the browser.
    """

    settings_model: ClassVar[type[TSettings]]
    request_model: ClassVar[type[TRequest]]
    response_model: ClassVar[type[TResponse]]

    def __init__(self, browser: Browser, settings: TSettings | None = None) -> None:
        """
        Initialize the Scraper.

        Args:
            browser (Browser): The browser instance to use for scraping.
        """
        self._browser = browser
        self._settings = settings if settings is not None else self.settings_model()

    @abstractmethod
    async def fetch(self, context: BrowserContext, request: TRequest) -> TRaw:
        """
        Fetch raw data from the target website.

        Args:
            context (BrowserContext): The browser context to use.
            request (TRequest): The request object containing parameters for the fetch operation.

        Returns:
            TRaw: The raw data fetched from the website.
        """
        ...

    @abstractmethod
    async def parse(self, raw: TRaw) -> TResponse:
        """
        Parse the raw data into a structured response.

        Args:
            raw (TRaw): The raw data returned by the fetch method.

        Returns:
            TResponse: The structured response object.
        """
        ...

    @overload
    async def run(self, request: TRequest, /) -> TResponse: ...

    @overload
    async def run(self, requests: list[TRequest], /) -> list[TResponse]: ...

    @overload
    async def run(self, *requests: TRequest) -> list[TResponse]: ...

    async def run(
        self,
        *requests: TRequest | list[TRequest],
    ) -> list[TResponse] | TResponse:
        """
        Run the scraper for one or more requests.

        This method handles the browser context creation, concurrent fetching,
        and parsing of results.

        Args:
            *requests: One or more request objects, or a list of request objects.

        Returns:
            list[TResponse] | TResponse: A single response if a single request was passed,
            or a list of responses corresponding to the input requests.
        """
        normalized_requests: list[TRequest]
        return_single = False

        if len(requests) == 1 and isinstance(requests[0], list):
            normalized_requests = requests[0]
        else:
            normalized_requests = []
            for req in requests:
                if isinstance(req, list):
                    raise TypeError("Expected request object, got list")
                normalized_requests.append(req)

            if len(normalized_requests) == 1:
                return_single = True

        async with self._browser.get_context() as context:
            raw_items = await asyncio.gather(
                *[self.fetch(context, request) for request in normalized_requests]
            )
        responses = await asyncio.gather(*[self.parse(raw) for raw in raw_items])
        if return_single:
            return responses[0]
        return responses
