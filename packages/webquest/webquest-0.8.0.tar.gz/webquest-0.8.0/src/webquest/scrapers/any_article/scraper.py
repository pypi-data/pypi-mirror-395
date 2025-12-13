from typing import override

from openai import AsyncOpenAI
from playwright.async_api import BrowserContext

from webquest.browsers.browser import Browser
from webquest.parsers.openai_parser import OpenAIParser
from webquest.scrapers.any_article.request import AnyArticleRequest
from webquest.scrapers.any_article.response import AnyArticleResponse
from webquest.scrapers.any_article.settings import AnyArticleSettings
from webquest.scrapers.scraper import Scraper


class AnyArticle(
    Scraper[
        AnyArticleSettings,
        AnyArticleRequest,
        AnyArticleResponse,
        str,
    ]
):
    """Scraper to extract the main article from any web page using OpenAI."""

    settings_model = AnyArticleSettings
    request_model = AnyArticleRequest
    response_model = AnyArticleResponse

    def __init__(
        self,
        browser: Browser,
        settings: AnyArticleSettings | None = None,
        openai_client: AsyncOpenAI | None = None,
    ) -> None:
        super().__init__(browser=browser, settings=settings)
        self._parser = OpenAIParser[AnyArticleResponse](
            response_type=AnyArticleResponse,
            client=openai_client,
            model=self._settings.parser_model,
            input="Parse the following web page and extract the main article:\n\n",
            character_limit=self._settings.character_limit,
        )

    @override
    async def fetch(
        self,
        context: BrowserContext,
        request: AnyArticleRequest,
    ) -> str:
        page = await context.new_page()
        await page.goto(request.url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        html = await page.content()
        return html

    @override
    async def parse(self, raw: str) -> AnyArticleResponse:
        response = await self._parser.parse(raw)
        response.content = response.content[: self._settings.character_limit]
        return response
