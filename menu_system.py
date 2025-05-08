import pygame
from constants import WHITE, BLACK, GRAY, FONT, WINDOW_WIDTH, WINDOW_HEIGHT

def create_button(text, y_position):
    """Create a button with the given text at the specified y-position."""
    text_surface = FONT.render(text, True, BLACK)
    button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, y_position, 200, 50)
    text_rect = text_surface.get_rect(center=button_rect.center)
    return text_surface, text_rect, button_rect

def create_mute_icon():
    """Create the mute icon in the upper-right corner."""
    padding = 20  # Space from the edges
    icon_size = 10  # Size of the icon (adjust as needed)
    return pygame.Rect(WINDOW_WIDTH - icon_size - padding, padding, icon_size, icon_size)

def draw_gallery_screen(screen, gallery):
    """Draw the gallery screen."""
    screen.fill(WHITE)
    
    # Draw back button
    back_button = create_button("Back", WINDOW_HEIGHT - 100)[2]
    pygame.draw.rect(screen, GRAY, back_button)
    text = FONT.render("Back", True, BLACK)
    text_rect = text.get_rect(center=back_button.center)
    screen.blit(text, text_rect)
    
    # Draw gallery items
    gallery.draw(screen)
    
    return back_button
def draw_dialogue(screen, speaker, text):
    window_width, window_height = screen.get_size()

    # Set dialogue box to 80% of the window width
    dialogue_width = int(window_width * 0.8)
    dialogue_height = 180  # You can adjust this if needed
    dialogue_x = (window_width - dialogue_width) // 2
    dialogue_y = window_height - dialogue_height - 30  # 30px margin from bottom

    dialogue_box_rect = pygame.Rect(dialogue_x, dialogue_y, dialogue_width, dialogue_height)

    # Draw the dialogue box
    pygame.draw.rect(screen, (200, 200, 200), dialogue_box_rect)  # Light gray
    pygame.draw.rect(screen, (0, 0, 0), dialogue_box_rect, 3)      # Black border

    # Fonts
    speaker_font = pygame.font.Font(None, 42)
    text_font = pygame.font.Font(None, 32)

    # Render speaker name
    speaker_surface = speaker_font.render(speaker, True, (0, 0, 0))
    screen.blit(speaker_surface, (dialogue_box_rect.x + 20, dialogue_box_rect.y + 10))

    # Word wrapping
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if text_font.size(test_line)[0] < dialogue_width - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Draw each wrapped line
    for i, line in enumerate(lines):
        line_surface = text_font.render(line, True, (0, 0, 0))
        screen.blit(line_surface, (dialogue_box_rect.x + 20, dialogue_box_rect.y + 60 + i * 35))
