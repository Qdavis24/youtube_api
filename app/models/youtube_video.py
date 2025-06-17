from dataclasses import dataclass
from typing import Optional, Dict, List, Any

@dataclass
class YoutubeVideo:
    url: str
    video_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    automatic_captions: Optional[Dict[str, List[Dict[str, Any]]]] = None