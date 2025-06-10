from dataclasses import dataclass
from typing import Optional, List

@dataclass
class YoutubeVideoProcessed:
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    transcript: Optional[str] = None
    thumbnail_url: Optional[str] = None