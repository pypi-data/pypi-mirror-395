from pydantic import BaseModel


class Article(BaseModel):
    site: str
    url: str
    title: str
    published_at: str


class GoogleNewsSearchResponse(BaseModel):
    articles: list[Article]
