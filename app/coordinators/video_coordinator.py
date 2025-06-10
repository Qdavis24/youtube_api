from app.services.youtube_service import YoutubeService
from app.models.youtube_video_processed import YoutubeVideoProcessed


class VideoCoordinator:
    MODEL_TO_SERVICE_MAPPING = {
        "video_id": "get_id",
        "title": "get_title",
        "transcript": "get_transcript",
        "thumbnail_url": "get_thumbnail",
        "description": "get_description"
    }
    def __init__(self):
        self.youtube_service = YoutubeService()
        self._cache : dict[str, YoutubeVideoProcessed] = {}

    def _check_cache(self, attribute: str, url : str):
        if url not in self._cache:
            return False, YoutubeVideoProcessed()
        if not getattr(self._cache[url], attribute):
            return False, self._cache[url]
        return True, self._cache[url]

    def _process_request(self, attribute: str, url: str):
        has_data, video_model = self._check_cache(attribute, url)
        if has_data:
            return getattr(video_model, attribute)
        request_data = getattr(self.youtube_service, VideoCoordinator.MODEL_TO_SERVICE_MAPPING[attribute])(url)
        setattr(video_model, attribute, request_data)
        return request_data

    def retrieve_transcript(self, url: str):
        return self._process_request("transcript", url)

    def retrieve_thumbnail(self, url: str):
        return self._process_request("thumbnail_url", url)
    
    def retrieve_title(self, url: str):
        return self._process_request("title", url)

    def retrieve_id(self, url: str):
        return self._process_request("id", url)

    def retrieve_description(self, url: str):
        return self._process_request("description", url)
    
    def retrieve_video(self, url: str):
        pass

    def retrieve_audio_url(self, url: str):
        pass
