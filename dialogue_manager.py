import pygame
from typing import Optional, List, Tuple
from datetime import datetime

class DialogueManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dialogue_box_height = 200
        self.padding = 20
        self.font = pygame.font.SysFont('Arial', 28)
        self.name_font = pygame.font.SysFont('Arial', 32, bold=True)
        
        # Animation settings
        self.chars_per_frame = 2
        self.current_text = ""
        self.display_text = ""
        self.speaker = None
        self.is_animating = False
        
        # Add dialogue history
        self.dialogue_history = []
        self.max_history = 50  # Maximum number of dialogue entries to keep
        
    def start_dialogue(self, text: str, speaker: Optional[str] = None):
        """Start new dialogue."""
        self.current_text = text
        self.display_text = ""
        self.speaker = speaker
        self.is_animating = True
        
    def update(self) -> bool:
        """Update dialogue animation. Returns True if animation is complete."""
        if self.is_animating:
            if len(self.display_text) < len(self.current_text):
                self.display_text = self.current_text[:len(self.display_text) + self.chars_per_frame]
            else:
                self.is_animating = False
        return not self.is_animating
                
    def draw(self, screen: pygame.Surface) -> pygame.Surface:
        """Draw dialogue box and text."""
        # Create dialogue box
        box_surface = pygame.Surface((self.screen_width, self.dialogue_box_height), pygame.SRCALPHA)
        box_surface.fill((255, 255, 255, 230))
        
        # Draw speaker name if present
        y_offset = self.padding
        if self.speaker:
            name_surf = self.name_font.render(self.speaker, True, (0, 0, 0))
            box_surface.blit(name_surf, (self.padding, y_offset))
            y_offset += name_surf.get_height() + 5
            
        # Draw text
        wrapped_lines = self._wrap_text(self.display_text)
        for line in wrapped_lines:
            text_surf = self.font.render(line, True, (0, 0, 0))
            box_surface.blit(text_surf, (self.padding, y_offset))
            y_offset += self.font.get_linesize()
            
        return box_surface
        
    def _wrap_text(self, text: str) -> List[str]:
        """Wrap text to fit the dialogue box width."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = self.font.render(word + ' ', True, (0, 0, 0))
            word_width = word_surface.get_width()
            
            if current_width + word_width <= self.screen_width - 2 * self.padding:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
                
        lines.append(' '.join(current_line))
        return lines

    def add_to_history(self, speaker, text):
        """Add dialogue entry to history."""
        self.dialogue_history.append({
            'speaker': speaker,
            'text': text,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        # Maintain max history size
        if len(self.dialogue_history) > self.max_history:
            self.dialogue_history.pop(0)
    
    def show_history(self, screen):
        """Display dialogue history."""
        # Create scrollable history view
        history_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        history_surface.fill((255, 255, 255))
        
        y_offset = 20
        for entry in reversed(self.dialogue_history):
            # Draw timestamp
            time_text = self.font.render(entry['timestamp'], True, (128, 128, 128))
            history_surface.blit(time_text, (20, y_offset))
            
            # Draw speaker and text
            if entry['speaker']:
                speaker_text = self.name_font.render(entry['speaker'], True, (0, 0, 0))
                history_surface.blit(speaker_text, (100, y_offset))
                y_offset += 30
            
            text_lines = self._wrap_text(entry['text'])
            for line in text_lines:
                text_surface = self.font.render(line, True, (0, 0, 0))
                history_surface.blit(text_surface, (100, y_offset))
                y_offset += self.font.get_linesize()
            
            y_offset += 20
        
        return history_surface