# scene_env/scene.py

class Scene:
    def __init__(self, name="DefaultScene", objects=None, environment=None):
        self.name = name
        self.objects = objects if objects is not None else []
        self.environment = environment if environment is not None else {}

    def render(self):
        return f"Rendering scene: {self.name} with {len(self.objects)} object(s)"

    def add_object(self, obj):
        self.objects.append(obj)

    def set_environment(self, key, value):
        self.environment[key] = value