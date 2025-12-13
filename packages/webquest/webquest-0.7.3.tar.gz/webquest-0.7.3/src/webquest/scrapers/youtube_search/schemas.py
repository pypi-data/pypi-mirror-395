from pydantic import BaseModel


class Video(BaseModel):
    id: str
    url: str
    title: str
    description: str
    published_at: str
    views: str
    channel_id: str
    channel_url: str
    channel_name: str


class Channel(BaseModel):
    id: str
    url: str
    name: str
    description: str | None
    subscribers: str


class Post(BaseModel):
    id: str
    url: str
    content: str
    published_at: str
    channel_id: str
    channel_url: str
    channel_name: str
    comments: str
    likes: str


class Short(BaseModel):
    id: str
    url: str
    title: str
    views: str


class YouTubeSearchRequest(BaseModel):
    query: str


class YouTubeSearchResponse(BaseModel):
    videos: list[Video]
    channels: list[Channel]
    posts: list[Post]
    shorts: list[Short]
