import os
import uuid
import mimetypes
import logging

logging.basicConfig(level=logging.INFO)

def get_video_metadata(video_path: str) -> dict:
    """Extract basic metadata from a video file."""
    if not os.path.exists(video_path):
        logging.error(f"Video file not found: {video_path}")
        raise FileNotFoundError(f"Video file not found: {video_path}")
    metadata = {
        "filename": os.path.basename(video_path),
        "size_bytes": os.path.getsize(video_path),
        "extension": os.path.splitext(video_path)[1],
        "mime_type": mimetypes.guess_type(video_path)[0]
    }
    logging.info(f"Extracted metadata for {video_path}")
    return metadata

def generate_video_id(prefix="VID") -> str:
    """Generate a unique video ID."""
    vid = f"{prefix}-{uuid.uuid4().hex[:8]}"
    logging.info(f"Generated video ID: {vid}")
    return vid

def is_valid_video_file(path: str) -> bool:
    """Check if a file is a valid video format."""
    mime_type = mimetypes.guess_type(path)[0]
    valid = mime_type and mime_type.startswith("video")
    logging.info(f"File {path} valid video: {valid}")
    return valid