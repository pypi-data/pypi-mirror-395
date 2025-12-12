from scene_env import Scene

def test_scene_render():
    scene = Scene("TestScene")
    assert scene.render() == "Rendering scene: TestScene"