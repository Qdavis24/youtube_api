from yt_dlp import YoutubeDL
from app.models.youtube_video import YoutubeVideo
from app.utils.youtube_dlp_formatter import YoutubeDlpFormatter
import os
import tempfile
import hashlib



class YoutubeService:
    def __init__(self):
        self._cache: dict[str, YoutubeVideo] = {}
        self.formatter = YoutubeDlpFormatter
        self.temp_dir = tempfile.mkdtemp()

    def _get_yt_config(self, filename_base):
        return {
            "writesubtitles": True,
            "writeautomaticsub": True,
            "skip_download": True,
            "subtitleslangs": ["en", "en-orig"],
            "subtitlesformat": "json3",
            "outtmpl": os.path.join(self.temp_dir, f"{filename_base}.%(ext)s"),
            "proxy": f"http://{os.environ.get('PROXY_USERNAME')}:{os.environ.get('PROXY_PASSWORD')}@p.webshare.io:{os.environ.get('PROXY_PORT')}"
        }

    def _get_video_data(self, url: str):
        if url not in self._cache:
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

            self._cache[url] = YoutubeVideo(
                url=url,
                video_id=data.get("id", "unknown"),
                title=data.get("title", "unknown"),
                description=data.get("description", "unknown"),
                thumbnail_url=data.get("thumbnail", "unknown"),
                automatic_captions=parsed_automatic_captions,
            )
        return self._cache[url]
    
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
