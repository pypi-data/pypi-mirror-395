from pygame import image

class AssetManager:
    def __init__(self):
        self.images = {}

    def load_image(self, name, path):
        try:
            img = image.load(path)  # no convert(), no convert_alpha()
            self.images[name] = img
            return img
        except FileNotFoundError:
            print(f"[Warning] Image '{path}' not found!")
            return None

    def get_image(self, name):
        return self.images.get(name)
