from sim_env.scene import Scene

def mock_scene(name="TestScene") -> Scene:
    """Create a mock Scene object for testing."""
    return Scene(
        name=name,
        objects=[
            {"id": 1, "type": "sphere", "position": [0, 0, 0]},
            {"id": 2, "type": "cube", "position": [1, 1, 1]}
        ],
        environment={
            "gravity": 9.8,
            "lighting": "default"
        }
    )

def mock_metrics() -> dict:
    """Return a sample metrics dictionary for simulation scoring."""
    return {
        "accuracy": 0.92,
        "efficiency": 0.85,
        "stability": 0.78
    }

def mock_video_metadata() -> dict:
    """Return fake video metadata for testing."""
    return {
        "filename": "test_video.mp4",
        "size_bytes": 1024,
        "extension": ".mp4",
        "mime_type": "video/mp4"
    }