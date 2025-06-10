import datetime

class YoutubeVideoRaw:
    def __init__(self, raw_data: dict, url: str):
        self.raw_data = raw_data
        self.url = url