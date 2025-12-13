from typing import override
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.scrapers.scraper import Scraper
from webquest.scrapers.youtube_search.request import YouTubeSearchRequest
from webquest.scrapers.youtube_search.response import (
    Channel,
    Post,
    Short,
    Video,
    YouTubeSearchResponse,
)
from webquest.scrapers.youtube_search.settings import YouTubeSearchSettings


class YouTubeSearch(
    Scraper[
        YouTubeSearchSettings,
        YouTubeSearchRequest,
        YouTubeSearchResponse,
        str,
    ]
):
    """Scraper to perform a YouTube search and parse the results."""

    settings_model = YouTubeSearchSettings
    request_model = YouTubeSearchRequest
    response_model = YouTubeSearchResponse

    def _parse_videos(self, soup: BeautifulSoup) -> list[Video]:
        videos: list[Video] = []
        video_tags = soup.find_all("ytd-video-renderer")

        for video_tag in video_tags:
            title_tag = video_tag.find(
                "h3",
                class_="title-and-badge style-scope ytd-video-renderer",
            )
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            views_tag, published_at_tag = video_tag.find_all(
                "span",
                class_="inline-metadata-item style-scope ytd-video-meta-block",
            )
            views = views_tag.get_text(strip=True)
            published_at = published_at_tag.get_text(strip=True)

            description_tag = video_tag.find(
                "yt-formatted-string",
                class_="metadata-snippet-text style-scope ytd-video-renderer",
            )
            if not description_tag:
                continue
            description = description_tag.get_text(strip=True)

            channel_name_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope yt-formatted-string",
            )
            if not channel_name_tag:
                continue
            channel_name = channel_name_tag.get_text(strip=True)

            channel_id_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope yt-formatted-string",
            )
            if not channel_id_tag:
                continue
            channel_id = channel_id_tag.get("href")
            if not isinstance(channel_id, str):
                continue
            channel_id = channel_id[1:]

            channel_url = f"https://www.youtube.com/{channel_id}"

            video_id_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope ytd-video-renderer",
            )
            if not video_id_tag:
                continue
            video_id = video_id_tag.get("href")
            if not isinstance(video_id, str):
                continue
            video_id = video_id.split("v=")[-1].split("&")[0]

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            video = Video(
                id=video_id,
                url=video_url[: self._settings.character_limit],
                title=title[: self._settings.character_limit],
                description=description[: self._settings.character_limit],
                published_at=published_at[: self._settings.character_limit],
                views=views[: self._settings.character_limit],
                channel_id=channel_id[: self._settings.character_limit],
                channel_url=channel_url[: self._settings.character_limit],
                channel_name=channel_name[: self._settings.character_limit],
            )
            videos.append(video)

        videos = [video for video in videos if len(video.id) == 11]

        unique_videos = {video.id: video for video in videos}
        videos = list(unique_videos.values())

        return videos

    def _parse_channels(self, soup: BeautifulSoup) -> list[Channel]:
        channels: list[Channel] = []
        channel_tags = soup.find_all("ytd-channel-renderer")
        for channel_tag in channel_tags:
            channel_name_tag = channel_tag.find(
                "yt-formatted-string",
                class_="style-scope ytd-channel-name",
            )
            if not channel_name_tag:
                continue
            channel_name = channel_name_tag.get_text(strip=True)

            description_tag = channel_tag.find("yt-formatted-string", id="description")
            if not description_tag:
                continue
            description: str | None = description_tag.get_text(strip=True)
            if description == "":
                description = None

            channel_id_tag = channel_tag.find("yt-formatted-string", id="subscribers")
            if not channel_id_tag:
                continue
            channel_id = channel_id_tag.get_text(strip=True)

            channel_url = f"https://www.youtube.com/{channel_id}"

            subscribers_tag = channel_tag.find("span", id="video-count")
            if not subscribers_tag:
                continue
            subscribers = subscribers_tag.get_text(strip=True)

            channel = Channel(
                id=channel_id[: self._settings.character_limit],
                url=channel_url[: self._settings.character_limit],
                name=channel_name[: self._settings.character_limit],
                description=description[: self._settings.character_limit]
                if description
                else None,
                subscribers=subscribers[: self._settings.character_limit],
            )
            channels.append(channel)
        return channels

    def _parse_posts(self, soup: BeautifulSoup) -> list[Post]:
        posts: list[Post] = []
        post_tags = soup.find_all("ytd-post-renderer")
        for post_tag in post_tags:
            content_tag = post_tag.find(
                "div",
                id="content",
            )
            if not content_tag:
                continue
            content = content_tag.get_text(strip=True)

            channel_name_tag = post_tag.find(
                "div",
                id="author",
            )
            if not channel_name_tag:
                continue
            channel_name = channel_name_tag.get_text(strip=True)

            published_at_tag = post_tag.find(
                "yt-formatted-string",
                id="published-time-text",
            )
            if not published_at_tag:
                continue
            published_at = published_at_tag.get_text(strip=True)

            channel_id_tag = post_tag.find(
                "a",
                id="author-text",
            )
            if not channel_id_tag:
                continue
            channel_id = channel_id_tag.get("href")
            if not isinstance(channel_id, str):
                continue
            channel_id = channel_id[1:]

            channel_url = f"https://www.youtube.com/{channel_id}"

            post_id_tag = post_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope yt-formatted-string",
            )
            if not post_id_tag:
                continue
            post_id = post_id_tag.get("href")
            if not isinstance(post_id, str):
                continue
            post_id = post_id.split("/post/")[-1]

            post_url = f"https://www.youtube.com/post/{post_id}"

            likes_tag = post_tag.find(
                "span",
                id="vote-count-middle",
            )
            if not likes_tag:
                continue
            likes = likes_tag.get_text(strip=True)

            comments_tag = post_tag.find(
                "div",
                class_="yt-spec-button-shape-next__button-text-content",
            )
            if not comments_tag:
                continue
            comments = comments_tag.get_text(strip=True)

            post = Post(
                id=post_id[: self._settings.character_limit],
                url=post_url[: self._settings.character_limit],
                content=content[: self._settings.character_limit],
                published_at=published_at[: self._settings.character_limit],
                channel_id=channel_id[: self._settings.character_limit],
                channel_url=channel_url[: self._settings.character_limit],
                channel_name=channel_name[: self._settings.character_limit],
                comments=comments[: self._settings.character_limit],
                likes=likes[: self._settings.character_limit],
            )
            posts.append(post)

        return posts

    def _parse_shorts(self, soup: BeautifulSoup) -> list[Short]:
        shorts: list[Short] = []
        short_tags = soup.find_all("ytm-shorts-lockup-view-model-v2")
        for short_tag in short_tags:
            title_tag = short_tag.find(
                "h3",
                role="presentation",
            )
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            views_tag = short_tag.find(
                "div",
                class_="shortsLockupViewModelHostOutsideMetadataSubhead shortsLockupViewModelHostMetadataSubhead",
            )
            if not views_tag:
                continue
            views = views_tag.get_text(strip=True)

            short_id_tag = short_tag.find(
                "a",
                class_="shortsLockupViewModelHostEndpoint shortsLockupViewModelHostOutsideMetadataEndpoint",
            )
            if not short_id_tag:
                continue
            short_id = short_id_tag.get("href")
            if not isinstance(short_id, str):
                continue
            short_id = short_id.split("shorts/")[-1]

            short_url = f"https://www.youtube.com/shorts/{short_id}"

            short = Short(
                id=short_id[: self._settings.character_limit],
                url=short_url[: self._settings.character_limit],
                title=title[: self._settings.character_limit],
                views=views[: self._settings.character_limit],
            )
            shorts.append(short)
        return shorts

    def _parse_search_results(self, soup: BeautifulSoup) -> YouTubeSearchResponse:
        videos = self._parse_videos(soup)
        channels = self._parse_channels(soup)
        posts = self._parse_posts(soup)
        shorts = self._parse_shorts(soup)
        return YouTubeSearchResponse(
            videos=videos[: self._settings.result_limit],
            channels=channels[: self._settings.result_limit],
            posts=posts[: self._settings.result_limit],
            shorts=shorts[: self._settings.result_limit],
        )

    @override
    async def parse(self, raw: str) -> YouTubeSearchResponse:
        soup = BeautifulSoup(raw, "html.parser")
        result = self._parse_search_results(soup)
        return result

    @override
    async def fetch(
        self,
        context: BrowserContext,
        request: YouTubeSearchRequest,
    ) -> str:
        url = (
            f"https://www.youtube.com/results?search_query={quote_plus(request.query)}"
        )
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector("ytd-video-renderer", timeout=10000)
        html = await page.content()
        return html
