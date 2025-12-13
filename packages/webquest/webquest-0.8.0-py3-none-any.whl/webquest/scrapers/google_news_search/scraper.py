import asyncio
from typing import override
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.scrapers.google_news_search.request import (
    GoogleNewsSearchRequest,
)
from webquest.scrapers.google_news_search.response import (
    Article,
    GoogleNewsSearchResponse,
)
from webquest.scrapers.google_news_search.settings import (
    GoogleNewsSearchSettings,
)
from webquest.scrapers.scraper import Scraper


class GoogleNewsSearch(
    Scraper[
        GoogleNewsSearchSettings,
        GoogleNewsSearchRequest,
        GoogleNewsSearchResponse,
        str,
    ]
):
    """Scraper to perform a Google News search and parse the results."""

    settings_model = GoogleNewsSearchSettings
    request_model = GoogleNewsSearchRequest
    response_model = GoogleNewsSearchResponse

    @override
    async def fetch(
        self,
        context: BrowserContext,
        request: GoogleNewsSearchRequest,
    ) -> str:
        url = f"https://news.google.com/search?q={quote_plus(request.query)}"
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)

        html = await page.content()

        return html

    @override
    async def parse(self, raw: str) -> GoogleNewsSearchResponse:
        soup = BeautifulSoup(raw, "html.parser")
        articles: list[Article] = []

        article_tags = soup.find_all("c-wiz")
        for article_tag in article_tags:
            title_tag = article_tag.find("a", class_="JtKRv")
            if not title_tag:
                continue
            title = title_tag.get_text().strip()

            url_tag = article_tag.find("a", class_="JtKRv")
            if not url_tag:
                continue
            url = url_tag.get("href")
            if not isinstance(url, str):
                continue

            url = f"https://news.google.com{url[1:]}"

            site_tag = article_tag.find("div", class_="vr1PYe")
            if not site_tag:
                continue
            site = site_tag.get_text().strip()

            published_at_tag = article_tag.find("time")
            if not published_at_tag:
                continue
            published_at = published_at_tag.get_text().strip()

            article = Article(
                site=site[: self._settings.character_limit],
                url=url[: self._settings.character_limit],
                title=title[: self._settings.character_limit],
                published_at=published_at[: self._settings.character_limit],
            )

            articles.append(article)

        articles = articles[: self._settings.result_limit]

        return GoogleNewsSearchResponse(articles=articles)
