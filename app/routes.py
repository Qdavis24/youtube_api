from . import api_bp
from flask import request, jsonify
from app.services.youtube_service import YoutubeService
import psutil
from functools import wraps
from dataclasses import asdict
import os

ys = YoutubeService()


def track_bandwidth(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        net_before = psutil.net_io_counters()
        result = f(*args, **kwargs)
        net_after = psutil.net_io_counters()
        bytes_used = net_after.bytes_recv - net_before.bytes_recv
        data = result.get_json()
        data["bandwidth_used"] = bytes_used
        return jsonify(data)
    return decorated_func

def require_api_key(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key != os.environ.get("API_KEY"):
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated_func


@api_bp.route("/health")
def health():
    return {"status": "ok"}


@api_bp.route("/video-data", methods=["GET"])
@require_api_key
@track_bandwidth
def get_data():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    try:
        data = ys.get_data(url)
    except Exception as e:
        print(f"\nERROR\n{e}\n\n")
        return jsonify({"error": str(e)}), 500
    return jsonify(asdict(data))


@api_bp.route("/automatic-captions", methods=["GET"])
@require_api_key
@track_bandwidth
def get_automatic_captions():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    try:
        automatic_captions = ys.get_automatic_captions(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"automatic_captions": automatic_captions})


@api_bp.route("/video-id", methods=["GET"])
@require_api_key
@track_bandwidth
def get_id():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    try:
        video_id = ys.get_id(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"video_id": video_id})


@api_bp.route("/title", methods=["GET"])
@require_api_key
@track_bandwidth
def get_title():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    try:
        title = ys.get_title(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"title": title})


@api_bp.route("/description", methods=["GET"])
@require_api_key
@track_bandwidth
def get_description():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    try:
        description = ys.get_description(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"description": description})


@api_bp.route("/thumbnail", methods=["GET"])
@require_api_key
@track_bandwidth
def get_thumbnail():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    try:
        thumbnail_url = ys.get_thumbnail(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"thumbnail_url": thumbnail_url})