from scene_env import Scene

def test_scene_render():
    scene = Scene(name="TestScene")
    assert scene.render() == "Rendering scene: TestScene with 0 object(s)"

def test_scene_add_object():
    scene = Scene()
    scene.add_object({"id": 1, "type": "sphere"})
    assert len(scene.objects) == 1