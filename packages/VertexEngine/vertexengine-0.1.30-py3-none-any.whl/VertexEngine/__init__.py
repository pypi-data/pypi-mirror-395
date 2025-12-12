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