from . import api_bp
from flask import request, jsonify
from app.coordinators.video_coordinator import VideoCoordinator

video_coordinator = VideoCoordinator()

@api_bp.route("/health")
def health():
    return {"status": "ok"}

@api_bp.route("/transcript", methods=["GET"])
def get_transcript():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    transcript = video_coordinator.retrieve_transcript(url)
    return jsonify({"transcript": transcript})

@api_bp.route("/id", methods=["GET"])
def get_id():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    video_id = video_coordinator.retrieve_id(url)
    return jsonify({"id": video_id})

@api_bp.route("/description", methods=["GET"])
def get_description():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter required"}), 400
    
    description = video_coordinator.retrieve_description(url)
    return jsonify({"description": description})