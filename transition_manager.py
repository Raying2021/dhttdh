import pygame
from effects import Effects

class TransitionManager:
    def __init__(self, screen):
        self.screen = screen
        self.effects = Effects()
        
    def transition_scene(self, from_surface, to_surface, effect="fade", duration=500):
        """Transition between two scenes."""
        if effect == "fade":
            self.effects.fade_out(from_surface, duration//2)
            self.screen.blit(to_surface, (0, 0))
            self.effects.fade_in(to_surface, duration//2)
        elif effect == "slide":
            self.effects.slide_in(self.screen, to_surface, "right", duration)