from contextlib import asynccontextmanager
from typing import AsyncIterator, override

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import BrowserContext, async_playwright

from webquest.browsers.browser import Browser


class Hyperbrowser(Browser):
    """
    A Browser implementation that uses Hyperbrowser for remote browser sessions.

    This class manages the creation and cleanup of Hyperbrowser sessions and provides
    a Playwright BrowserContext connected to the remote session.
    """

    def __init__(
        self,
        client: AsyncHyperbrowser | None = None,
    ):
        """
        Initialize the Hyperbrowser instance.

        Args:
            client (AsyncHyperbrowser | None): An optional AsyncHyperbrowser client.
                If not provided, a new client will be created.
        """
        if client is None:
            client = AsyncHyperbrowser()
        self._client = client

    @override
    @asynccontextmanager
    async def get_context(self) -> AsyncIterator[BrowserContext]:
        """
        Get a browser context from a new Hyperbrowser session.

        This method creates a new session, connects to it using Playwright, yields
        the context, and ensures the session is stopped afterwards.

        Yields:
            BrowserContext: The Playwright browser context connected to the Hyperbrowser session.
        """
        session = await self._client.sessions.create()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
            context = browser.contexts[0]
            try:
                yield context
            finally:
                await self._client.sessions.stop(session.id)
