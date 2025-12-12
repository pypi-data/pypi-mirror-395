import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    def load_music(self, path):
        self.music = path
        pygame.mixer.music.load(path)

    def play_music(self, loops=-1):
        if self.music:
            pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        pygame.mixer.music.stop()
