import pygame
import random
import math
import numpy as np
from abc import ABC, abstractmethod
from enum import Enum

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)

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
        
# ENCAPSULATION: AudioManager handles all sound effects and music
class AudioManager:
    """Manages all audio - background music and sound effects"""
    def __init__(self):
        self._sounds = {}
        self._music_loaded = False
        self._music_volume = 0.5
        self._sfx_volume = 0.7
        
        # Load sound effects
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound effects"""
   
    def _sounds(self):

        try:
            try:
                self._sounds['perfect'] = pygame.mixer.Sound("perfect.wav")
                self._sounds['good'] = pygame.mixer.Sound("good.wav")
                self._sounds['miss'] = pygame.mixer.Sound("miss.wav")
                self._sounds['special'] = pygame.mixer.Sound("special.mp3")
                print("Loaded WAV sound files successfully!")
            except:
                # If files don't exist, generate synthetic sounds
                print("Sound files not found - generating synthetic sounds")
                self._create_hit_sounds()
            
        except Exception as e:
            print(f"Sound initialization failed: {e}")
        # Create super basic fallback
    
    def _generate_beep(self, frequency, duration):
        self._sounds = {
            'perfect': pygame.mixer.Sound(buffer=self._generate_beep(880, 0.1)),
            'good': pygame.mixer.Sound(buffer=self._generate_beep(440, 0.1)),
            'miss': pygame.mixer.Sound(buffer=self._generate_beep(220, 0.2)),
            'special': pygame.mixer.Sound(buffer=self._generate_chord([523, 659, 784], 0.2))
        }

    def _generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2), dtype=np.int16)

        # Generate sine wave
        for i in range(frames):
            sample = int(16384 * math.sin(2 * math.pi * frequency * i / sample_rate))
            # Apply envelope to avoid clicks
            envelope = min(1.0, i / (frames * 0.1), (frames - i) / (frames * 0.1))
            sample = int(sample * envelope)
            arr[i] = [sample, sample]
        
        return arr.tobytes()

    def _generate_chord(self, frequencies, duration):
        """Generate a chord (multiple frequencies)"""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2), dtype=np.int16)
        
        for i in range(frames):
            sample = 0
            for freq in frequencies:
                sample += int(5000 * math.sin(2 * math.pi * freq * i / sample_rate))
            
            # Apply envelope
            envelope = min(1.0, i / (frames * 0.1), (frames - i) / (frames * 0.1))
            sample = int(sample * envelope)
            arr[i] = [sample, sample]
        
        return arr.tobytes()

    def set_volume(self):
        sound.set_volume(self._sfx_volume)

    def _create_hit_sounds(self):
        """Create simple hit sound effects"""
        # Perfect hit sound (higher pitch)
        self._sounds['perfect'] = pygame.mixer.Sound(buffer=self._generate_beep(880, 0.1))
        
        # Good hit sound (medium pitch)
        self._sounds['good'] = pygame.mixer.Sound(buffer=self._generate_beep(440, 0.1))
        
        # Miss sound (lower pitch)
        self._sounds['miss'] = pygame.mixer.Sound(buffer=self._generate_beep(220, 0.2))
        
        # Special note sound (chord)
        self._sounds['special'] = pygame.mixer.Sound(buffer=self._generate_chord([523, 659, 784], 0.2))
    
    def load_background_music(self, music_file):
        """Load background music file"""
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self._music_volume)
            self._music_loaded = True
            print(f"Background music loaded: {music_file}")
        except Exception as e:
            print(f"Warning: Could not load background music: {e}")
            self._music_loaded = False
    
    def play_background_music(self, loops=-1):
        """Play background music (loops=-1 means infinite loop)"""
        if self._music_loaded:
            try:
                pygame.mixer.music.play(loops)
                print("Background music started")
            except Exception as e:
                print(f"Warning: Could not play background music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()

    def play_hit_sound(self, accuracy: HitAccuracy, is_special=False):
        """Play sound effect for note hit"""
        try:
            if is_special:
                self._sounds['special'].play()
            elif accuracy == HitAccuracy.PERFECT:
                self._sounds['perfect'].play()
            elif accuracy == HitAccuracy.GOOD:
                self._sounds['good'].play()
            else:
                self._sounds['miss'].play()
        except Exception as e:
            print(f"Couldn't play sound: {e}")

    
    def set_music_volume(self, volume):
        """Set background music volume (0.0 to 1.0)"""
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self._sfx_volume = max(0.0, min(1.0, volume))

        for sound in self.values():
            sound.set_volume(self._sfx_volume)

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
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OOP Rhythm Game - 4 Pillars Demo")
        
        self.audio_manager = AudioManager()
        self.audio_manager.set_sfx_volume(0.7)

        try:
            self.audio_manager = AudioManager()
            # Ensure volumes are set
            self.audio_manager.set_sfx_volume(0.7)
            self.audio_manager.set_music_volume(0.5)
        except Exception as e:
            print(f"Audio initialization error: {e}")
            # Create minimal audio fallback
            self.audio_manager = None

        try:
            self.audio_manager.load_background_music("background_music.wav")
            self.audio_manager.set_music_volume(0.5)  # 50% volume
            self.audio_manager.play_background_music(loops=-1)  # -1 = infinite loop
        except Exception as e:
            print(f"Background music error: {e}")
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

    def update_notes(self):
        """Update all notes"""
        for note in self.notes[:]:  # Create copy to avoid modification during iteration
            note.update()  # POLYMORPHISM: Different note types update differently
            
            if note.is_off_screen():
                if not note.hit:
                    # Missed note
                    self.score_manager.add_hit(HitAccuracy.MISS, 0)
                    self.show_feedback("MISS", RED)
                self.notes.remove(note)

    def handle_input(self, events, keys_pressed):
        """Handle player input"""
        pressed_lanes, held_lanes = self.input_handler.handle_input(events, keys_pressed)
        
        # Handle pressed lanes
        for lane in pressed_lanes:
            self.check_hit(lane, False)
        
        # Handle held lanes for hold notes
        for lane in held_lanes:
            self.check_hit(lane, True)
    
    def check_hit(self, lane, is_hold):
        """Check if a note was hit in the specified lane"""
        for note in self.notes:
            if note.lane == lane and not note.hit:
                distance = note.get_hit_zone_distance(self.hit_zone_y)
                
                # Different logic for hold notes
                if isinstance(note, HoldNote):
                    if is_hold and distance <= 30:
                        note.being_held = True
                        if not hasattr(note, '_hit_registered'):
                            accuracy = note.calculate_accuracy(distance)
                            self.score_manager.add_hit(accuracy, note.score_value)
                            self.audio_manager.play_hit_sound(accuracy)  # Play sound for hold notes too
                            self.show_feedback(accuracy.value, self.get_accuracy_color(accuracy))
                            note._hit_registered = True
                else:
                    # Normal and special notes
                    if not is_hold and distance <= 40:
                        accuracy = note.calculate_accuracy(distance)
                        # POLYMORPHISM: Different note types have different score values
                        self.score_manager.add_hit(accuracy, note.score_value)
                        self.audio_manager.play_hit_sound(accuracy, isinstance(note, SpecialNote))
                        self.show_feedback(accuracy.value, self.get_accuracy_color(accuracy))
                        note.hit = True
                        break

    def get_accuracy_color(self, accuracy):
        """Get color for accuracy feedback"""
        if accuracy == HitAccuracy.PERFECT:
            return GREEN
        elif accuracy == HitAccuracy.GOOD:
            return YELLOW
        else:
            return RED
    
    def show_feedback(self, text, color):
        """Show feedback text"""
        self.feedback_text = text
        self.feedback_color = color
        self.feedback_timer = 60  # Show for 1 second at 60 FPS              

    def draw(self):
        """Draw all game elements"""
        self.screen.fill(BLACK)
        
        # Draw lanes
        for i in range(4):
            x = i * 150 + 100
            pygame.draw.line(self.screen, WHITE, (x - 50, 0), (x - 50, SCREEN_HEIGHT), 2)
            pygame.draw.line(self.screen, WHITE, (x + 50, 0), (x + 50, SCREEN_HEIGHT), 2)
        
        # Draw hit zone
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (50, self.hit_zone_y - 20, 500, 40))
        pygame.draw.rect(self.screen, WHITE, 
                        (50, self.hit_zone_y - 20, 500, 40), 2)
        
        # Draw notes - POLYMORPHISM: Each note type draws differently
        for note in self.notes:
            note.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw feedback
        if self.feedback_timer > 0:
            text = self.font.render(self.feedback_text, True, self.feedback_color)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(text, rect)
            self.feedback_timer -= 1
        
        pygame.display.flip()

    def draw_ui(self):
        """Draw user interface"""
        # Score
        score_text = self.font.render(f"Score: {self.score_manager.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Combo
        combo_text = self.font.render(f"Combo: {self.score_manager.combo}", True, WHITE)
        self.screen.blit(combo_text, (10, 50))
        
        # Accuracy
        accuracy = self.score_manager.get_accuracy_percentage()
        accuracy_text = self.small_font.render(f"Accuracy: {accuracy:.1f}%", True, WHITE)
        self.screen.blit(accuracy_text, (10, 90))
        
        # Hit statistics
        hits = self.score_manager.hits
        stats_y = 130
        for accuracy, count in hits.items():
            color = self.get_accuracy_color(accuracy)
            stats_text = self.small_font.render(f"{accuracy.value}: {count}", True, color)
            self.screen.blit(stats_text, (10, stats_y))
            stats_y += 25
        
        # Controls
        controls = ["Controls:", "D F J K", "Hold for long notes"]
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, 10 + i * 25))

    def run(self):
        """Main game loop"""
        while self.running:
            events = pygame.event.get()
            keys_pressed = pygame.key.get_pressed()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Handle input
            self.handle_input(events, keys_pressed)
            
            # Update game
            self.spawn_note()
            self.update_notes()
            
            # Draw
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = RhythmGame()

    if game.audio_manager:
        game.audio_manager.play_hit_sound(HitAccuracy.PERFECT)
        pygame.time.delay(300)
        game.audio_manager.play_hit_sound(HitAccuracy.GOOD)
        pygame.time.delay(300)
        game.audio_manager.play_hit_sound(HitAccuracy.MISS)
        pygame.time.delay(300)
        game.audio_manager.play_hit_sound(HitAccuracy.PERFECT, True)


    game.run()