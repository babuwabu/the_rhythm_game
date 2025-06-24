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

class NoteType(Enum):
    NORMAL = "NORMAL"
    HOLD = "HOLD"
    SPECIAL = "SPECIAL"


# ABSTRACTION: Abstract base classes define interfaces
class GameObject(ABC):
    """Abstract base class for all game objects"""
    def __init__(self, x, y):
        self._x = x  # ENCAPSULATION: Private attributes
        self._y = y
        
    @property
    def x(self):  # ENCAPSULATION: Controlled access via properties
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @abstractmethod
    def update(self):
        """Abstract method that must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Abstract method for drawing the object"""
        pass