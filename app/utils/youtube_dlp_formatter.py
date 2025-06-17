import json


class YoutubeDlpFormatter:
    @staticmethod
    def parse_json3_transcript(content: str) -> str:
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

    @staticmethod
    def parse_srv_transcript(content: str) -> str:
        # SRV format is XML-based
        import re

        text_matches = re.findall(r"<text[^>]*>(.*?)</text>", content, re.DOTALL)
        transcript_parts = []

        for match in text_matches:
            # Remove HTML entities and tags
            clean_text = re.sub(r"&[^;]+;", "", match)
            clean_text = re.sub(r"<[^>]+>", "", clean_text)
            if clean_text.strip():
                transcript_parts.append(clean_text.strip())

        return " ".join(transcript_parts)

    @staticmethod
    def parse_vtt_srt_transcript(content: str) -> str:
        # Parse VTT/SRT format
        import re

        lines = content.split("\n")
        transcript_parts = []

        for line in lines:
            line = line.strip()
            # Skip timestamp lines and empty lines
            if "-->" in line or line.isdigit() or not line:
                continue
            # Skip VTT header
            if line.startswith("WEBVTT") or line.startswith("NOTE"):
                continue
            transcript_parts.append(line)

        return " ".join(transcript_parts)
