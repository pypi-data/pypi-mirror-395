import asyncio
from typing import override
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.scrapers.duckduckgo_search.schemas import (
    DuckDuckGoSearchRequest,
    DuckDuckGoSearchResponse,
    Page,
)
from webquest.scrapers.scraper import Scraper


class DuckDuckGoSearch(Scraper[DuckDuckGoSearchRequest, str, DuckDuckGoSearchResponse]):
    """Scraper to perform a DuckDuckGo web search and parse the results."""

    request = DuckDuckGoSearchRequest
    response = DuckDuckGoSearchResponse

    @override
    async def fetch(
        self,
        context: BrowserContext,
        request: DuckDuckGoSearchRequest,
    ) -> str:
        url = f"https://duckduckgo.com/?origin=funnel_home_website&t=h_&q={quote_plus(request.query)}&ia=web"
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)

        await page.wait_for_selector("button#more-results", timeout=15000)
        await page.click("button#more-results")

        await page.wait_for_selector("li[data-layout='organic']", timeout=15000)

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(4)

        html = await page.content()

        return html

    @override
    async def parse(self, raw: str) -> DuckDuckGoSearchResponse:
        soup = BeautifulSoup(raw, "html.parser")
        pages: list[Page] = []

        article_tags = soup.find_all("article", {"data-testid": "result"})

        for article_tag in article_tags:
            site_tag = article_tag.find("p", class_="fOCEb2mA3YZTJXXjpgdS")
            if not site_tag:
                continue
            site = site_tag.get_text(strip=True)

            url_tag = article_tag.find("a", {"data-testid": "result-title-a"})
            if not url_tag:
                continue
            url = url_tag.get("href")
            if not isinstance(url, str):
                continue

            title_tag = article_tag.find("span", class_="EKtkFWMYpwzMKOYr0GYm")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            description_tag = article_tag.find("span", class_="kY2IgmnCmOGjharHErah")
            if not description_tag:
                continue
            description = description_tag.get_text(strip=True)

            page = Page(
                site=site,
                url=url,
                title=title,
                description=description,
            )
            pages.append(page)

        return DuckDuckGoSearchResponse(pages=pages)
