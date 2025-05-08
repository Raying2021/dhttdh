import os
import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1535, 810
TUBE_TOP, TUBE_BOTTOM = 100, 600
TUBE_HEIGHT = TUBE_BOTTOM - TUBE_TOP
TARGET_MIN, TARGET_MAX, PERFECT = 2.3, 2.7, 2.5
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 50, 255)

# Function to convert value to pixel position
def value_to_y(value):
    return int(TUBE_BOTTOM - (value / 5) * TUBE_HEIGHT)

# Function to reset game
def reset_game():
    global green_value, speed, moving_up, stopped, message, show_button
    green_value = random.uniform(0, 5)
    moving_up = True
    stopped = False
    message = ""
    show_button = False

# Function to draw menu
def draw_menu(screen, title_font, font, max_unlocked_level):
    screen.fill(BLACK)
    title_text = title_font.render("Graduated Tube Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    subtitle_text = font.render("Levels go from Easy to Hard", True, WHITE)
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, 200))

    for i in range(1, 5):
        button_y = 300 + i * 100
        button_rect = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
        if i <= max_unlocked_level:
            pygame.draw.rect(screen, BLUE, button_rect, border_radius=10)
            button_text = font.render(f"Level {i}: {levels[i]['name']}", True, WHITE)
        else:
            pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
            button_text = font.render(f"Level {i}: Locked", True, WHITE)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

# Function to draw level complete screen
def draw_level_complete(screen, font, current_level):
    screen.fill(BLACK)
    message = font.render(f"Good job! You successfully completed Level {current_level}.", True, GREEN)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 50))

    if current_level < 4:
        next_text = font.render("Let's move to the next level!", True, WHITE)
        screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 50))
    else:
        final_text = font.render("Congratulations! You completed all levels!", True, WHITE)
        screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2 + 50))

# Function to draw final game completion screen
def draw_game_finished(screen, title_font):
    screen.fill(BLACK)
    final_message = title_font.render("Good job! You finished this game!", True, GREEN)
    screen.blit(final_message, (WIDTH // 2 - final_message.get_width() // 2, HEIGHT // 2 - 50))

def run_graduated_tube_game():
    global green_value, speed, moving_up, stopped, message, show_button, levels, current_level, max_unlocked_level
    global game_active, menu_active, level_complete, all_levels_complete, game_finished
    global WIDTH, HEIGHT  # Update WIDTH and HEIGHT dynamically for fullscreen

    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
    WIDTH, HEIGHT = screen.get_size()  # Update WIDTH and HEIGHT to match fullscreen resolution
    pygame.display.set_caption("Graduated Tube Game")

    # Font setup
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)
    button_font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 72)

    # Load background image
    background = pygame.image.load(os.path.join(os.path.dirname(__file__), "novaGarage.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Button setup
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 50, 120, 40)

    # Level variables
    levels = {
        1: {"name": "Easy", "speed": 0.05},
        2: {"name": "Medium", "speed": 0.1},
        3: {"name": "Hard", "speed": 0.2},
        4: {"name": "Extreme", "speed": 0.3},
    }
    current_level = 1
    max_unlocked_level = 1
    game_active = False
    menu_active = True
    level_complete = False
    all_levels_complete = False
    game_finished = False

    # Reset game variables
    reset_game()

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(WHITE)

        if menu_active:
            draw_menu(screen, title_font, font, max_unlocked_level)
        elif level_complete:
            draw_level_complete(screen, font, current_level)
        elif game_finished:
            draw_game_finished(screen, title_font)
            pygame.display.flip()
            pygame.time.delay(2000)  # Wait for 2 seconds to show the "Game Done" message
            running = False  # Exit the game loop
        elif game_active:
            # Draw background
            screen.blit(background, (0, 0))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not stopped:
                    stopped = True
                    if TARGET_MIN <= green_value <= TARGET_MAX:
                        if round(green_value, 1) == PERFECT:
                            message = "Perfect!"
                        else:
                            message = "Good job!"
                        if current_level == max_unlocked_level and max_unlocked_level < 4:
                            max_unlocked_level += 1
                        level_complete = True
                        game_active = False
                    else:
                        message = "You lost! Try again"
                        show_button = True

                if event.type == pygame.MOUSEBUTTONDOWN and show_button:
                    if button_rect.collidepoint(event.pos):
                        reset_game()

            # Update movement
            if not stopped:
                if moving_up:
                    green_value += speed
                    if green_value >= 5:
                        moving_up = False
                else:
                    green_value -= speed
                    if green_value <= 0:
                        moving_up = True

            # Draw tube
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 30, TUBE_TOP, 60, TUBE_HEIGHT), 3)

            # Draw red filling
            fill_height = (green_value / 5) * TUBE_HEIGHT
            pygame.draw.rect(screen, RED, (WIDTH // 2 - 30, TUBE_BOTTOM - fill_height, 60, fill_height))

            # Draw specific numbers on the graduated tube
            marked_values = [0, 1, 2, 2.3, 2.5, 2.7, 3, 4, 5]
            for value in marked_values:
                y_pos = value_to_y(value)
                text_surface = small_font.render(f"{value:.1f}", True, WHITE)
                screen.blit(text_surface, (WIDTH // 2 - 80, y_pos - 10))
                pygame.draw.line(screen, WHITE, (WIDTH // 2 - 40, y_pos), (WIDTH // 2 - 20, y_pos), 2)

            # Draw message
            if stopped:
                text_surface = font.render(message, True, WHITE)
                screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 100))

            # Draw "Try Again" button
            if show_button:
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
                button_text = button_font.render("Try Again", True, WHITE)
                screen.blit(button_text, (button_rect.x + 15, button_rect.y + 8))

        # Event handling for menu and level complete screens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if menu_active and event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1, 5):
                    button_y = 300 + i * 100
                    button_rect = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
                    if button_rect.collidepoint(event.pos) and i <= max_unlocked_level:
                        current_level = i
                        speed = levels[current_level]["speed"]
                        reset_game()
                        menu_active = False
                        game_active = True
            if level_complete and event.type == pygame.KEYDOWN:
                if current_level < 4:
                    current_level += 1
                    speed = levels[current_level]["speed"]
                    reset_game()
                    game_active = True
                    level_complete = False
                else:
                    all_levels_complete = True
                    level_complete = False
                    game_finished = True

        pygame.display.flip()
        clock.tick(FPS)

    # Quit the game properly
    return  # Return control to the main script