from pydantic import BaseModel


class YouTubeTranscriptRequest(BaseModel):
    video_id: str


class YouTubeTranscriptResponse(BaseModel):
    transcript: str
