from abc import ABC, abstractmethod
from typing import AsyncContextManager

from playwright.async_api import BrowserContext


class Browser(ABC):
    """
    Abstract base class for browser implementations.

    This class defines the interface for obtaining a browser context, which is used
    for performing web scraping operations.
    """

    @abstractmethod
    def get_context(self) -> AsyncContextManager[BrowserContext]:
        """
        Get an asynchronous context manager that yields a Playwright BrowserContext.

        Returns:
            AsyncContextManager[BrowserContext]: An async context manager that yields a BrowserContext.
        """
        ...
