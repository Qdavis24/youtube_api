from yt_dlp import YoutubeDL
from app.models.youtube_video import YoutubeVideo
from app.utils.youtube_dlp_formatter import YoutubeDlpFormatter
from app.services.redis_service import redis_client
from app.config import config
from dataclasses import asdict
import os
import hashlib
import json




class YoutubeService:
    def __init__(self):
        self._cache = redis_client
        self.formatter = YoutubeDlpFormatter
        self.temp_dir = "/tmp"
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_yt_config(self, filename_base):
        return {
            "writesubtitles": True,
            "writeautomaticsub": True,
            "skip_download": True,
            "subtitleslangs": ["en", "en-orig"],
            "subtitlesformat": "json3",
            "outtmpl": os.path.join(self.temp_dir, f"{filename_base}.%(ext)s"),
            "proxy": config.PROXY
        }

    def _get_video_data(self, url: str):
        if self._cache.exists(f"video:{url}"):
            bytes_video = self._cache.get(f"video:{url}")
            video_model = YoutubeVideo(**json.loads(bytes_video))
            return video_model
        
        url_hash = hashlib.md5(url.encode()).hexdigest()
        with YoutubeDL(params=self._get_yt_config(url_hash)) as yt:
            data = yt.extract_info(url=url, download=True)
            
        automatic_captions_filepath = f"{self.temp_dir}/{url_hash}.en.json3"
            
        if os.path.exists(automatic_captions_filepath):
            with open(automatic_captions_filepath, "r") as automatic_caption_file:
                parsed_automatic_captions = self.formatter.parse_json3_transcript(
                    automatic_caption_file.read()
                )
            os.remove(automatic_captions_filepath)
        else:
            parsed_automatic_captions = "No transcript available"

        video_model = YoutubeVideo(
            url=url,
            video_id=data.get("id", "unknown"),
            title=data.get("title", "unknown"),
            description=data.get("description", "unknown"),
            thumbnail_url=data.get("thumbnail", "unknown"),
            automatic_captions=parsed_automatic_captions,
        )

        self._cache.set(f"video:{url}", json.dumps(asdict(video_model)))

        return video_model
    
    def get_data(self, url: str):
        data = self._get_video_data(url)
        return data

    def get_description(self, url: str):
        data = self._get_video_data(url)
        return data.description

    def get_title(self, url: str):
        data = self._get_video_data(url)
        return data.title

    def get_id(self, url: str):
        data = self._get_video_data(url)
        return data.video_id

    def get_automatic_captions(self, url: str):
        data = self._get_video_data(url)
        return data.automatic_captions

    def get_thumbnail(self, url: str):
        data = self._get_video_data(url)
        return data.thumbnail_url
