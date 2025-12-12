class Scene:
    def __init__(self, engine):
        self.engine = engine

    def update(self):
        pass

    def draw(self, surface):
        pass

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def switch_to(self, name):
        self.current_scene = self.scenes.get(name)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, surface):
        if self.current_scene:
            self.current_scene.draw(surface)
