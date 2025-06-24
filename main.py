import pygame
import random
import math
from abc import ABC, abstractmethod
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)


class HitAccuracy(Enum):
    PERFECT = "PERFECT"
    GOOD = "GOOD"
    MISS = "MISS"

