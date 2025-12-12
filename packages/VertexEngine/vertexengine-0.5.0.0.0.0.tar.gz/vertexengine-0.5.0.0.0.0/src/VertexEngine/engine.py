from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QTimer, Qt
import pygame
from .scenes import SceneManager

pygame.init()

class GameEngine(QWidget):
    def __init__(self, width=800, height=600, fps=60, title="Vertex App"):
        super().__init__()
        self.width = width
        self.height = height
        self.fps = fps

        # Qt key tracking (NOT pygame)
        self.keys_down = set()

        # pygame surface
        self.screen = pygame.Surface((self.width, self.height))

        # Scene manager
        self.scene_manager = SceneManager()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // self.fps)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # ---------------------- RENDER ----------------------

    def paintEvent(self, event):
        self.screen.fill((50, 50, 100))
        self.scene_manager.draw(self.screen)

        raw = pygame.image.tostring(self.screen, "RGBA")
        img = QImage(raw, self.width, self.height, QImage.Format.Format_RGBA8888)

        painter = QPainter(self)
        painter.drawImage(0, 0, img)

    def resizeEvent(self, event):
        size = event.size()
        self.width = size.width()
        self.height = size.height()
        self.screen = pygame.Surface((self.width, self.height))

    # ---------------------- UPDATE ----------------------

    def update_frame(self):
        if not self.hasFocus():
            self.keys_down.clear()  # prevent stuck movement

        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.update()

        self.update()

    # ---------------------- KEY INPUT ----------------------

    def keyPressEvent(self, event):
        self.keys_down.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_down:
            self.keys_down.remove(event.key())
