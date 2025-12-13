from abc import ABC
from typing import Generic, Type, TypeVar, override

from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from pydantic import BaseModel

from webquest.browsers.browser import Browser
from webquest.scrapers.scraper import Scraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TResponse = TypeVar("TResponse", bound=BaseModel)


class OpenAIParser(
    Generic[TRequest, TResponse],
    Scraper[TRequest, str, TResponse],
    ABC,
):
    """Abstract base class for OpenAI-based parsers."""

    def __init__(
        self,
        browser: Browser,
        response_type: Type[TResponse],
        client: AsyncOpenAI | None = None,
        model: str = "gpt-5-mini",
        input: str = "Parse the following web content:\n",
        character_limit: int = 20000,
    ) -> None:
        self._response_type = response_type
        if client is None:
            client = AsyncOpenAI()
        self._client = client
        self._model = model
        self._character_limit = character_limit
        self._input = input
        super().__init__(browser=browser)

    @override
    async def parse(self, raw: str) -> TResponse:
        soup = BeautifulSoup(raw, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        if len(text) > self._character_limit:
            start = (len(text) - self._character_limit) // 2
            end = start + self._character_limit
            text = text[start:end]

        response = await self._client.responses.parse(
            input=f"{self._input}{text}",
            text_format=self._response_type,
            model=self._model,
            reasoning={"effort": "minimal"},
        )
        if response.output_parsed is None:
            raise ValueError("Failed to parse the response into the desired format.")
        return response.output_parsed
