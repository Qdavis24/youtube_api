from yt_dlp import YoutubeDL
from app.models.youtube_video_raw import YoutubeVideoRaw
from app.utils.youtube_dlp_formatter import YoutubeDlpFormatter
import requests
import json


class YoutubeService:
    YT_CONFIG = {
        "writeinfojson": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "skip_download": True,
        "extract_flat": False,
    }

    def __init__(self):
        self._cache: dict[str, YoutubeVideoRaw] = {}
        self.formatter = YoutubeDlpFormatter

    def _get_video_data(self, url: str):
        if url not in self._cache:
            with YoutubeDL(params=YoutubeService.YT_CONFIG) as yt:
                info = yt.extract_info(url=url, download=False)
            self._cache[url] = YoutubeVideoRaw(raw_data=info, url=url)
        return self._cache[url]

    def get_description(self, url: str):
        data = self._get_video_data(url)
        return data.raw_data.get("description", "unknown")

    def get_title(self, url: str):
        data = self._get_video_data(url)
        return data.raw_data.get("title", "unknown")

    def get_id(self, url: str):
        data = self._get_video_data(url)
        return data.raw_data.get("id", "unknown")

    def get_transcript(self, url: str):
        data = self._get_video_data(url)
        
        # Try automatic captions first
        auto_captions = data.raw_data.get("automatic_captions", {})
        captions = auto_captions.get("en") or auto_captions.get("en-orig")
        
        # If no auto captions, try manual subtitles
        if not captions:
            subtitles = data.raw_data.get("subtitles", {})
            captions = subtitles.get("en") or subtitles.get("en-orig")
        
        if not captions:
            return "No transcript available"
        
        # Find best format (prefer json3, then srv1, then others)
        format_priority = ["json3", "srv1", "srv2", "srv3", "vtt", "srt"]
        transcript_url = None
        
        for fmt in format_priority:
            for caption in captions:
                if caption.get("ext") == fmt:
                    transcript_url = caption.get("url")
                    break
            if transcript_url:
                break
        
        if not transcript_url:
            return "No suitable transcript format found"
        
        # Download and parse transcript
        try:
            response = requests.get(transcript_url, timeout=10)
            response.raise_for_status()
            
            if transcript_url.endswith("json3"):
                return self._parse_json3_transcript(response.text)
            elif "srv" in transcript_url:
                return self._parse_srv_transcript(response.text)
            else:
                return self._parse_vtt_srt_transcript(response.text)
                
        except requests.RequestException:
            return "Failed to download transcript"
    
    def _parse_json3_transcript(self, content: str) -> str:
        try:
            data = json.loads(content)
            events = data.get("events", [])
            transcript_parts = []
            
            for event in events:
                if "segs" in event:
                    for seg in event["segs"]:
                        if "utf8" in seg:
                            transcript_parts.append(seg["utf8"])
            
            return " ".join(transcript_parts).strip()
        except (json.JSONDecodeError, KeyError):
            return "Failed to parse JSON3 transcript"
    
    def _parse_srv_transcript(self, content: str) -> str:
        # SRV format is XML-based
        import re
        text_matches = re.findall(r'<text[^>]*>(.*?)</text>', content, re.DOTALL)
        transcript_parts = []
        
        for match in text_matches:
            # Remove HTML entities and tags
            clean_text = re.sub(r'&[^;]+;', '', match)
            clean_text = re.sub(r'<[^>]+>', '', clean_text)
            if clean_text.strip():
                transcript_parts.append(clean_text.strip())
        
        return " ".join(transcript_parts)
    
    def _parse_vtt_srt_transcript(self, content: str) -> str:
        # Parse VTT/SRT format
        import re
        lines = content.split('\n')
        transcript_parts = []
        
        for line in lines:
            line = line.strip()
            # Skip timestamp lines and empty lines
            if '-->' in line or line.isdigit() or not line:
                continue
            # Skip VTT header
            if line.startswith('WEBVTT') or line.startswith('NOTE'):
                continue
            transcript_parts.append(line)
        
        return " ".join(transcript_parts)

    def get_thumbnail(self, url: str):
        data = self._get_video_data(url)
        return data.raw_data.get("thumbnail", "unknown")
