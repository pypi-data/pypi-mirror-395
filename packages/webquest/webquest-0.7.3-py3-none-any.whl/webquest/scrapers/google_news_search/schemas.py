from pydantic import BaseModel


class GoogleNewsSearchRequest(BaseModel):
    query: str


class Article(BaseModel):
    site: str
    url: str
    title: str
    published_at: str


class GoogleNewsSearchResponse(BaseModel):
    articles: list[Article]
