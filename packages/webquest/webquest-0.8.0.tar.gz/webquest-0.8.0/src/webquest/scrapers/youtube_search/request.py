from pydantic import BaseModel


class YouTubeSearchRequest(BaseModel):
    query: str
