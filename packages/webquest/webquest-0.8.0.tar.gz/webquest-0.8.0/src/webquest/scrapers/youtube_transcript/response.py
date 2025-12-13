from pydantic import BaseModel


class YouTubeTranscriptResponse(BaseModel):
    transcript: str
