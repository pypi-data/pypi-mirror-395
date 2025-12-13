from typing import override

from openai import AsyncOpenAI
from playwright.async_api import BrowserContext

from webquest.browsers.browser import Browser
from webquest.scrapers.any_article.schemas import AnyArticleRequest, AnyArticleResponse
from webquest.scrapers.openai_parser import OpenAIParser


class AnyArticle(OpenAIParser[AnyArticleRequest, AnyArticleResponse]):
    """Scraper to extract the main article from any web page using OpenAI."""

    request = AnyArticleRequest
    response = AnyArticleResponse

    def __init__(
        self,
        browser: Browser,
        client: AsyncOpenAI | None = None,
        model: str = "gpt-5-mini",
        character_limit: int = 4000,
    ) -> None:
        super().__init__(
            browser=browser,
            response_type=AnyArticleResponse,
            client=client,
            model=model,
            input="Parse the following web page and extract the main article:\n\n",
            character_limit=character_limit,
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
