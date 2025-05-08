import pygame

def draw_background(screen, background, width, height):
    """Draw the background image scaled to fit the screen."""
    if background:
        scaled_background = pygame.transform.scale(background, (width, height))
        screen.blit(scaled_background, (0, 0))

def draw_text_box(screen, text_box_height, text_box_padding, text, speaker, width, height):
    """Draw the text box and dialogue."""
    text_box_surface = pygame.Surface((width, text_box_height), pygame.SRCALPHA)
    text_box_surface.fill((255, 255, 255, 200))  # Semi-transparent white
    screen.blit(text_box_surface, (0, height - text_box_height))

    if text:
        font = pygame.font.SysFont('Arial', 28)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (text_box_padding, height - text_box_height + text_box_padding))

    if speaker:
        name_font = pygame.font.SysFont('Arial', 32, bold=True)
        name_surface = name_font.render(speaker, True, (0, 0, 0))
        screen.blit(name_surface, (text_box_padding, height - text_box_height - 40))