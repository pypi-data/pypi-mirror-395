from typing import Generic, Type, TypeVar

from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from pydantic import BaseModel

TResponse = TypeVar("TResponse", bound=BaseModel)


class OpenAIParser(Generic[TResponse]):
    """Abstract base class for OpenAI-based parsers."""

    def __init__(
        self,
        response_type: Type[TResponse],
        client: AsyncOpenAI | None = None,
        model: str = "gpt-5-mini",
        input: str = "Parse the following web content:\n",
        character_limit: int = 5000,
    ) -> None:
        self._response_type = response_type
        self._client = client if client is not None else AsyncOpenAI()
        self._model = model
        self._character_limit = character_limit
        self._input = input

    async def parse(self, html: str) -> TResponse:
        soup = BeautifulSoup(html, "html.parser")
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
