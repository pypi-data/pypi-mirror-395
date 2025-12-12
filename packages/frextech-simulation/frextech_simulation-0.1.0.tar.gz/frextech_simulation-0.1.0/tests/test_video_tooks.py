import pytest
import os
from utils import get_video_metadata, generate_video_id, is_valid_video_file

def test_generate_video_id():
    vid = generate_video_id()
    assert vid.startswith("VID-")
    assert len(vid) > 5

def test_get_video_metadata(tmp_path):
    path = tmp_path / "test.mp4"
    path.write_bytes(b"fake video data")
    metadata = get_video_metadata(path)
    assert metadata["filename"] == "test.mp4"
    assert metadata["extension"] == ".mp4"
    assert metadata["size_bytes"] > 0

def test_is_valid_video_file(tmp_path):
    path = tmp_path / "test.mp4"
    path.write_bytes(b"fake video data")
    assert is_valid_video_file(path) is True