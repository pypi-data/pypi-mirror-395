from pydantic_settings import BaseSettings


class YouTubeTranscriptSettings(BaseSettings):
    character_limit: int = 5000
