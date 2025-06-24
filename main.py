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

class Drawable(ABC):
    """Abstract interface for drawable objects"""
    @abstractmethod
    def render(self, screen):
        pass

# INHERITANCE: Base Note class
class Note(GameObject):
    """Base class for all notes - demonstrates inheritance"""
    def __init__(self, lane, y=-20):
        super().__init__(lane * 150 + 100, y)  # INHERITANCE: Call parent constructor
        self._lane = lane  # ENCAPSULATION: Private attribute
        self._width = 80
        self._height = 20
        self._speed = 4
        self._hit = False
        self._color = (255, 255, 255)
        
    @property
    def lane(self):  # ENCAPSULATION: Getter method
        return self._lane
    
    @property
    def hit(self):
        return self._hit
    
    @hit.setter
    def hit(self, value):
        self._hit = value

    def update(self):
        """Update note position"""
        self.y += self._speed
    
    def draw(self, screen):
        """Draw the note"""
        if not self._hit:
            pygame.draw.rect(screen, self._color, 
                           (self.x - self._width//2, self.y, self._width, self._height))
            pygame.draw.rect(screen, BLACK, 
                           (self.x - self._width//2, self.y, self._width, self._height), 2)
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def get_hit_zone_distance(self, hit_zone_y):
        """Calculate distance from hit zone"""
        return abs(self.y + self._height//2 - hit_zone_y)
    
    def calculate_accuracy(self, distance):
        """Calculate hit accuracy based on distance"""
        if distance <= 15:
            return HitAccuracy.PERFECT
        elif distance <= 30:
            return HitAccuracy.GOOD
        else:
            return HitAccuracy.MISS
        
