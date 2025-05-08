import pygame
import logging
import os

class SoundManager:
    def __init__(self):
        """Initialize the sound manager."""
        self.is_muted = False
        self.previous_volume = 1.0
        self.sounds = {}
        self.current_music = None
        try:
            pygame.mixer.init()
        except pygame.error as e:
            logging.error(f"Could not initialize sound mixer: {e}")
        
        # GUI settings
        self.volume_icon_rect = None
        self.font = pygame.font.Font(None, 24)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (128, 128, 128)
        self.button_width = 40
        self.button_height = 30
        self.padding = 10
        
        logging.info("Sound Manager initialized")

    def setup_volume_control(self, screen_width, adjacent_button_rect=None):
        """Create volume control icon position."""
        x = (adjacent_button_rect.right + self.padding if adjacent_button_rect 
             else screen_width - self.button_width - self.padding)
        y = self.padding
        self.volume_icon_rect = pygame.Rect(x, y, self.button_width, self.button_height)

    def handle_volume(self, is_mute=None, volume=None):
        """Centralized volume handling."""
        if is_mute is not None:
            self.is_muted = is_mute
        
        if volume is not None:
            self.previous_volume = max(0.0, min(1.0, volume))
            
        current_volume = 0 if self.is_muted else self.previous_volume
        try:
            pygame.mixer.music.set_volume(current_volume)
            for sound in self.sounds.values():
                sound.set_volume(current_volume)
        except Exception as e:
            logging.error(f"Error setting volume: {e}")

    def toggle_mute(self):
        """Toggle mute state and return new state."""
        self.is_muted = not self.is_muted
        try:
            self.handle_volume()
            logging.info(f"Sound {'muted' if self.is_muted else 'unmuted'}")
        except Exception as e:
            logging.error(f"Error toggling mute: {e}")
        return self.is_muted

    def set_volume(self, volume):
        """Set the volume for all sounds."""
        self.handle_volume(volume=volume)
        logging.info(f"Volume set to {self.previous_volume}")

    def draw_volume_icon(self, screen):
        """Draw volume icon with appropriate symbol."""
        if self.volume_icon_rect:
            # Draw button background
            pygame.draw.rect(screen, self.DARK_GRAY if self.is_muted else self.GRAY, 
                           self.volume_icon_rect)
            pygame.draw.rect(screen, self.BLACK, self.volume_icon_rect, 2)
            
            # Draw appropriate symbol
            symbol = "🔇" if self.is_muted else "🔊"
            text_surface = self.font.render(symbol, True, self.BLACK)
            text_rect = text_surface.get_rect(center=self.volume_icon_rect.center)
            screen.blit(text_surface, text_rect)
            
    def play_music(self, file, loop=False):
        """Play a music file."""
        try:
            print(f"Attempting to play music: {file}")
            print(f"File exists: {os.path.exists(file)}")
            print(f"Full path: {os.path.abspath(file)}")
            
            pygame.mixer.music.load(file)
            pygame.mixer.music.set_volume(0 if self.is_muted else self.previous_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = file
            logging.info(f"Playing music: {file}, loop={loop}")
            print(f"Successfully started music playback: {file}")
        except Exception as e:
            logging.error(f"Error playing music {file}: {e}")
            print(f"ERROR playing music {file}: {e}")
            
    def play_sound(self, file):
        """Play a sound effect."""
        try:
            print(f"Attempting to play sound: {file}")
            print(f"File exists: {os.path.exists(file)}")
            print(f"Full path: {os.path.abspath(file)}")
            
            if file not in self.sounds:
                self.sounds[file] = pygame.mixer.Sound(file)
            sound = self.sounds[file]
            sound.set_volume(0 if self.is_muted else self.previous_volume)
            sound.play()
            logging.info(f"Playing sound: {file}")
            print(f"Successfully started sound playback: {file}")
        except Exception as e:
            logging.error(f"Error playing sound {file}: {e}")
            print(f"ERROR playing sound {file}: {e}")