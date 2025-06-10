import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.youtube_service import YoutubeService

ys = YoutubeService()

print(ys.get_transcript("https://www.youtube.com/watch?v=3bEkaRUVOeU&t=13s"))

print(ys.get_title("https://www.youtube.com/watch?v=3bEkaRUVOeU&t=13s"))

print(ys.get_id("https://www.youtube.com/watch?v=3bEkaRUVOeU&t=13s"))

print(ys.get_description("https://www.youtube.com/watch?v=3bEkaRUVOeU&t=13s"))