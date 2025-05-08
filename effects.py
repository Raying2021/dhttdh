import pygame
import random

def fade(surface, target_alpha, speed=5):
    """Fade a surface to a target alpha."""
    current_alpha = surface.get_alpha() or 255
    if current_alpha < target_alpha:
        return min(current_alpha + speed, target_alpha)
    elif current_alpha > target_alpha:
        return max(current_alpha - speed, target_alpha)
    return target_alpha

def shake(position, intensity=10):
    """Shake an object by randomly offsetting its position."""
    offset_x = random.randint(-intensity, intensity)
    offset_y = random.randint(-intensity, intensity)
    return position[0] + offset_x, position[1] + offset_y

def move(current_position, target_position, speed=5):
    """Move an object smoothly to a target position."""
    x, y = current_position
    target_x, target_y = target_position
    new_x = x + (target_x - x) / speed
    new_y = y + (target_y - y) / speed
    return new_x, new_y

def fade_to_color(screen, color, duration, clock, fps):
    """Fade the screen to a specific color."""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)
    for alpha in range(0, 256, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

class Effects:
    @staticmethod
    def fade_in(screen, duration_ms=500):
        temp_surface = screen.copy()
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        
        for alpha in range(255, -1, -5):
            fade_surface.set_alpha(alpha)
            screen.blit(temp_surface, (0, 0))
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(duration_ms // 51)
    
    @staticmethod
    def fade_out(screen, duration_ms=500):
        temp_surface = screen.copy()
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        
        for alpha in range(0, 256, 5):
            fade_surface.set_alpha(alpha)
            screen.blit(temp_surface, (0, 0))
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(duration_ms // 51)
    
    @staticmethod
    def slide_in(screen, surface, direction="right", duration_ms=500):
        width, height = screen.get_size()
        steps = 20
        delay = duration_ms // steps
        
        if direction == "right":
            for i in range(steps + 1):
                x = (i * width // steps) - width
                screen.blit(surface, (x, 0))
                pygame.display.flip()
                pygame.time.delay(delay)