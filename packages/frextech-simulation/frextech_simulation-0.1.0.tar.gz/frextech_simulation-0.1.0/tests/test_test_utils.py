import pytest
from tests.test_utils import mock_scene, mock_metrics, mock_video_metadata
from tests.test_utils import assert_dicts_equal, assert_in_range, assert_keys_present, assert_positive

def test_mock_scene():
    scene = mock_scene()
    assert scene.name == "TestScene"
    assert isinstance(scene.objects, list)

def test_mock_metrics():
    metrics = mock_metrics()
    assert "accuracy" in metrics
    assert "efficiency" in metrics
    assert "stability" in metrics

def test_mock_video_metadata():
    metadata = mock_video_metadata()
    assert metadata["extension"] == ".mp4"

def test_assertions():
    assert_dicts_equal({"a": 1}, {"a": 1})
    assert_in_range(5, 1, 10)
    assert_keys_present({"a": 1, "b": 2}, ["a", "b"])
    assert_positive(10)