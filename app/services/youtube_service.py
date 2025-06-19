from yt_dlp import YoutubeDL
from app.models.youtube_video import YoutubeVideo
from app.utils.youtube_dlp_formatter import YoutubeDlpFormatter
from app.services.redis_service import redis_client
from app.config import config
from dataclasses import asdict
import os
import hashlib
import json
import shutil





class YoutubeService:
    def __init__(self):
        self._cache = redis_client
        self.formatter = YoutubeDlpFormatter
        self.resources_directory = "./temp-resources"
        os.makedirs(self.resources_directory, exist_ok=True)

    def _get_yt_config(self, export_file_path: str):
        return {
            "writeautomaticsub": True,
            "skip_download": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "json3",
            "outtmpl": {
                "thumbnail": os.path.join(export_file_path, "thumbnail.%(ext)s"),
                "subtitle": os.path.join(export_file_path, f"subtitle.%(ext)s"),
            },
            "proxy": config.PROXY
        }

    def _get_video_data(self, url: str):
        if self._cache.exists(f"video:{url}"):
            bytes_video = self._cache.get(f"video:{url}")
            video_model = YoutubeVideo(**json.loads(bytes_video))
            return video_model
    
        temp_directory_hash = hashlib.md5(url.encode()).hexdigest()
        temp_directory_filepath = f"{self.resources_directory}/{temp_directory_hash}"
        print(temp_directory_filepath)
        os.makedirs(temp_directory_filepath, exist_ok=False)

        data = None
        with YoutubeDL(params=self._get_yt_config(temp_directory_filepath)) as yt:
            data = yt.extract_info(url=url, download=True)
            
        automatic_captions_filepath = f"{temp_directory_filepath}/subtitle.en.json3"
            
        if os.path.exists(automatic_captions_filepath):
            with open(automatic_captions_filepath, "r") as automatic_caption_file:
                parsed_automatic_captions = self.formatter.parse_json3_transcript(
                    automatic_caption_file.read()
                )
        else:
            parsed_automatic_captions = "No transcript available"

        shutil.rmtree(temp_directory_filepath)

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
