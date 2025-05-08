import pygame
from constants import WHITE, BLACK, FONT, WINDOW_WIDTH, WINDOW_HEIGHT

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_surface = font.render(' '.join(current_line), True, BLACK)
        if line_surface.get_width() > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def draw_dialogue(screen, speaker, text):
    """Draw dialogue with speaker name and wrapped text."""
    # Define dialogue box dimensions
    dialogue_box_rect = pygame.Rect(50, WINDOW_HEIGHT - 200, WINDOW_WIDTH - 100, 150)
    pygame.draw.rect(screen, WHITE, dialogue_box_rect)
    pygame.draw.rect(screen, BLACK, dialogue_box_rect, 2)

    # Render speaker name
    if speaker:
        name_surface = FONT.render(speaker, True, BLACK)
        name_rect = name_surface.get_rect(topleft=(dialogue_box_rect.x + 10, dialogue_box_rect.y - 30))
        screen.blit(name_surface, name_rect)

    # Wrap and render text
    wrapped_lines = wrap_text(text, FONT, dialogue_box_rect.width - 20)
    for i, line in enumerate(wrapped_lines):
        line_surface = FONT.render(line, True, BLACK)
        line_rect = line_surface.get_rect(topleft=(dialogue_box_rect.x + 10, dialogue_box_rect.y + 10 + i * 30))
        screen.blit(line_surface, line_rect)