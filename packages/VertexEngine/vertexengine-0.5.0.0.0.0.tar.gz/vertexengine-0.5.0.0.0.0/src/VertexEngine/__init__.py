# pyqtpygame_sdk/__init__.py
# Copyright (C) 2025
# This library/SDK is free. You can redistribute it.
# Tyrel Gomez (email as annbasilan)
# annbasilan0828@gmail.com
"""Vertex 3 is an SDK for RainOS GameDev. It's also supported by many others.

Supported OSes 
--------------
- RainOS 
- Windows 
- MacOS, 
- OS X 
- BeOS 
- FreeBSD 
- IRIX  
- and Linux

It is written on top of the excellent Pygame library which is ran on the even more excellent SDL library which runs on every Desktop OS with SDL."""
import pygame
from .engine import GameEngine
from .scenes import Scene, SceneManager
from .assets import AssetManager
from .audio import AudioManager
from pygame.base import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from pygame import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
import sys

print(
    "Vertex 3 (SDL {}.{}.{}, Python {}.{}.{})".format(  # pylint: disable=consider-using-f-string
        ver, *get_sdl_version() + sys.version_info[0:3]
    )
)

class VertexScreen():
    """Draw on VertexEngine's Screen."""
    def __init__(self):
        pass
    class Draw():
        "The Draw class to draw on VertexEngine"
        def __init__(self):
            pass
        def rect(self, surface, color, rect=None):
            """Draw a Rectangle of a solid color."""
            pygame.draw.rect(surface, color, rect)
        def polygon(self, surface, color, points, width):
            "Draw a polygon by marking points on the screen to make an n-gon"
            pygame.draw.polygon(surface, color, points, width)
        def circle(self, 
                   circle_surface, 
                   color, 
                   center, 
                   radius, 
                   width, 
                   draw_top_right, 
                   draw_top_left, 
                   draw_bottom_right, 
                   draw_bottom_left):
            """Draw a Circle with radius, color, etc."""
            pygame.draw.circle(self, circle_surface, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
        def ellipse(self, surface, color, rect, width):
            """Draw an elipse with surface, color, rect and width""" 
            pygame.draw.ellipse(self, surface, color, rect, width)
        def arc(self, surface, color, rect, start_angle, stop_angle, width):
            "Draw an arc with a lot of values"
            pygame.draw.arc(self, surface, color, rect, start_angle, stop_angle, width)
        