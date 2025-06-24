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
        

# INHERITANCE: Specialized note types inherit from Note
class NormalNote(Note):
    """Normal note - basic implementation"""
    def __init__(self, lane, y=-20):
        super().__init__(lane, y)
        self._color = (100, 150, 255)
        self._score_value = 100
    
    @property
    def score_value(self):
        return self._score_value
    

class HoldNote(Note):
    """Hold note - must be held down"""
    def __init__(self, lane, y=-20, duration=60):
        super().__init__(lane, y)
        self._color = (255, 150, 100)
        self._duration = duration
        self._hold_timer = 0
        self._being_held = False
        self._score_value = 200
        self._height = 40  # Taller than normal notes
    
    @property
    def score_value(self):
        return self._score_value
    
    @property
    def being_held(self):
        return self._being_held
    
    @being_held.setter
    def being_held(self, value):
        self._being_held = value
        if value:
            self._hold_timer += 1
    
    def draw(self, screen):
        """Override draw method for visual distinction"""
        if not self._hit:
            # Draw main body
            pygame.draw.rect(screen, self._color, 
                           (self.x - self._width//2, self.y, self._width, self._height))
            # Draw hold indicator
            pygame.draw.rect(screen, (255, 255, 0), 
                           (self.x - self._width//2 + 5, self.y + 5, self._width - 10, self._height - 10))
            pygame.draw.rect(screen, BLACK, 
                           (self.x - self._width//2, self.y, self._width, self._height), 2)
            

class SpecialNote(Note):
    """Special note with bonus effects"""
    def __init__(self, lane, y=-20):
        super().__init__(lane, y)
        self._color = (255, 215, 0)  # Gold color
        self._score_value = 500
        self._glow_timer = 0
    
    @property
    def score_value(self):
        return self._score_value
    
    def update(self):
        """Override update to add glow effect"""
        super().update()
        self._glow_timer += 1
    
    def draw(self, screen):
        """Override draw method with glow effect"""
        if not self._hit:
            # Create pulsing glow effect
            glow_intensity = int(50 + 30 * math.sin(self._glow_timer * 0.2))
            glow_color = (255, 255, glow_intensity)
            
            # Draw glow
            pygame.draw.rect(screen, glow_color, 
                           (self.x - self._width//2 - 5, self.y - 5, 
                            self._width + 10, self._height + 10))
            # Draw main note
            pygame.draw.rect(screen, self._color, 
                           (self.x - self._width//2, self.y, self._width, self._height))
            pygame.draw.rect(screen, BLACK, 
                           (self.x - self._width//2, self.y, self._width, self._height), 2)
            

# POLYMORPHISM: Factory pattern for creating different note types
class NoteFactory:
    """Factory class for creating notes - demonstrates polymorphism"""
    
    @staticmethod
    def create_note(note_type: NoteType, lane: int, y: int = -20) -> Note:
        """POLYMORPHISM: Returns different note types through same interface"""
        if note_type == NoteType.NORMAL:
            return NormalNote(lane, y)
        elif note_type == NoteType.HOLD:
            return HoldNote(lane, y)
        elif note_type == NoteType.SPECIAL:
            return SpecialNote(lane, y)
        else:
            return NormalNote(lane, y)  # Default case
    
    @staticmethod
    def create_random_note(lane: int, y: int = -20) -> Note:
        """Create a random note type"""
        # Weight the probability: 70% normal, 20% hold, 10% special
        rand = random.random()
        if rand < 0.7:
            return NoteFactory.create_note(NoteType.NORMAL, lane, y)
        elif rand < 0.9:
            return NoteFactory.create_note(NoteType.HOLD, lane, y)
        else:
            return NoteFactory.create_note(NoteType.SPECIAL, lane, y)
        
