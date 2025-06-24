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
        

# ENCAPSULATION: ScoreManager encapsulates scoring logic
class ScoreManager:
    """Manages scoring and statistics - demonstrates encapsulation"""
    def __init__(self):
        self.__score = 0  # ENCAPSULATION: Private attribute (name mangling)
        self.__combo = 0
        self.__max_combo = 0
        self.__hits = {accuracy: 0 for accuracy in HitAccuracy}
    
    @property
    def score(self):  # ENCAPSULATION: Read-only property
        return self.__score
    
    @property
    def combo(self):
        return self.__combo
    
    @property
    def max_combo(self):
        return self.__max_combo
    
    @property
    def hits(self):
        return self.__hits.copy()  # Return copy to prevent external modification
    
    def add_hit(self, accuracy: HitAccuracy, base_score: int):
        """Add a hit with given accuracy"""
        self.__hits[accuracy] += 1
        
        if accuracy != HitAccuracy.MISS:
            self.__combo += 1
            self.__max_combo = max(self.__max_combo, self.__combo)
            
            # Calculate score with combo multiplier
            multiplier = 1.0
            if accuracy == HitAccuracy.PERFECT:
                multiplier = 1.5
            elif accuracy == HitAccuracy.GOOD:
                multiplier = 1.0
            
            combo_bonus = min(self.__combo * 0.1, 2.0)  # Max 2x combo bonus
            final_score = int(base_score * multiplier * (1 + combo_bonus))
            self.__score += final_score
        else:
            self.__combo = 0

    def get_accuracy_percentage(self):
        """Calculate overall accuracy percentage"""
        total_hits = sum(self.__hits.values())
        if total_hits == 0:
            return 0
        successful_hits = self.__hits[HitAccuracy.PERFECT] + self.__hits[HitAccuracy.GOOD]
        return (successful_hits / total_hits) * 100

 
# POLYMORPHISM: Different input handlers
class InputHandler(ABC):
    """Abstract base class for input handling"""
    @abstractmethod
    def handle_input(self, events, keys_pressed):
        pass

class KeyboardInputHandler(InputHandler):
    """Keyboard input handler"""
    def __init__(self):
        self.lane_keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        self.key_states = [False] * 4
    
    def handle_input(self, events, keys_pressed):
        """Handle keyboard input"""
        pressed_lanes = []
        held_lanes = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                for i, key in enumerate(self.lane_keys):
                    if event.key == key:
                        pressed_lanes.append(i)
                        self.key_states[i] = True
            elif event.type == pygame.KEYUP:
                for i, key in enumerate(self.lane_keys):
                    if event.key == key:
                        self.key_states[i] = False
        
        # Check for held keys
        for i, held in enumerate(self.key_states):
            if held:
                held_lanes.append(i)
        
        return pressed_lanes, held_lanes
    

# Main Game Class
class RhythmGame:
    """Main game class demonstrating all OOP principles"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OOP Rhythm Game - 4 Pillars Demo")
        self.clock = pygame.time.Clock()
        
        # COMPOSITION: Game contains other objects
        self.notes = []
        self.score_manager = ScoreManager()  # ENCAPSULATION
        self.input_handler = KeyboardInputHandler()  # POLYMORPHISM
        
        # Game settings
        self.hit_zone_y = SCREEN_HEIGHT - 100
        self.last_note_time = 0
        self.note_interval = 800  # milliseconds
        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Feedback
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = WHITE
        
        self.running = True

    def spawn_note(self):
        """Spawn a new note using the factory pattern"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_note_time > self.note_interval:
            lane = random.randint(0, 3)
            # POLYMORPHISM: Factory creates different note types
            note = NoteFactory.create_random_note(lane)
            self.notes.append(note)
            self.last_note_time = current_time

