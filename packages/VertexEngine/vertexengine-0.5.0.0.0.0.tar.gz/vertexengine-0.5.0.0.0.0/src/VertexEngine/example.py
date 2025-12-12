from PyQt6.QtWidgets import QApplication
from engine import GameEngine
import pygame
from scenes import Scene
from assets import AssetManager
from audio import AudioManager
import sys
class MyScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.assets = AssetManager()
        self.assets.load_image("ball", "ball.png")
        self.x = 100
        self.y = 100
        self.speed = 5
        self.width = engine.width
        self.height = engine.height

    def update(self):
        # Process pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x -= self.speed
                elif event.key == pygame.K_RIGHT:
                    self.x += self.speed
                elif event.key == pygame.K_UP:
                    self.y -= self.speed
                elif event.key == pygame.K_DOWN:
                    self.y += self.speed

        # Clamp the ball inside the engine window
        self.x = max(0, min(self.x, self.width - 50))
        self.y = max(0, min(self.y, self.height - 50))

    def draw(self, surface):
        surface.fill((0, 0, 0))  # clear screen
        ball = self.assets.get_image("ball")
        if ball:
            ball_scaled = pygame.transform.scale(ball, (55, 50))
            surface.blit(ball_scaled, (self.x, self.y))
        else:
            pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 25)

app = QApplication(sys.argv)  # ✅ must be first

engine = GameEngine()
engine.resize(800, 600)

# Create scene and add to manager
my_scene = MyScene(engine)
engine.scene_manager.add_scene("main", my_scene)
engine.scene_manager.switch_to("main")  # make it the active scene

# Show the engine
engine.show()

# Start the PyQt6 event loop
sys.exit(app.exec())
