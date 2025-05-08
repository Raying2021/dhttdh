import pygame
import sys
import os
from pygame.locals import *

def start_oil_drain_challenge():
    # Initialize pygame
    pygame.init()

    # Set up the display
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Oil Drain Challenge')

    # Helper function for text with background
    def create_text_with_background(text, font_obj, color=(255, 255, 255)):
        text_surface = font_obj.render(text, True, color)
        background = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
        background.fill((0, 0, 0))
        background.blit(text_surface, (10, 5))
        return background

    # Load images with error handling and fallback
    base_dir = os.path.dirname(__file__)  # Get the directory of this file

    try:
        background_path = os.path.join(base_dir, 'Car_hood.jpg')
        print(f"Loading background from: {background_path}")  # Debugging
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        has_background = True
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load background image: {e}")
        has_background = False
        background_color = (100, 100, 100)  # Gray fallback

    try:
        oil_drain_path = os.path.join(base_dir, 'Oil_drain.png')
        print(f"Loading oil drain from: {oil_drain_path}")  # Debugging
        oil_drain = pygame.image.load(oil_drain_path)
        oil_drain = pygame.transform.scale(oil_drain, (400, 400))  # 2x bigger
        has_oil_drain = True
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load oil drain image: {e}")
        has_oil_drain = False
        oil_drain_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 1, 200, 200)  # Fallback rectangle

    # Game states
    STATES = {"WAITING": 0, "MINIGAME": 1, "GAME_OVER": 2, "VICTORY": 3}
    current_state = STATES["WAITING"]

    # Game variables
    press_count = 0
    press_timer = 0
    threshold_speed = 3  # Presses per second threshold
    progress = 0
    win_threshold = 50
    last_press_time = 0
    space_held = False
    scored_clicks = 0

    # Text setup
    font = pygame.font.Font(None, 72)
    instruction_font = pygame.font.Font(None, 36)
    game_over_text = create_text_with_background("Game Over!", font, (255, 0, 0))
    oil_back_text = create_text_with_background("All the oil went back in the engine, looks like I have to start over", instruction_font)
    be_faster_text = create_text_with_background("Be faster next time!", instruction_font)
    retry_text = create_text_with_background("Click to retry", font)
    start_text = create_text_with_background("Click or press SPACE to start!", font)

    # Instructions
    instructions = [
        "Mash the SPACE BAR as fast as you can!",
        "Maintain high speed to fill the progress bar",
        "Keep going until it's full!"
    ]
    instruction_surfaces = [create_text_with_background(text, instruction_font) for text in instructions]
    victory_text = create_text_with_background("You won!!!", font)
    continue_text = create_text_with_background("Click to continue", font)

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if current_state == STATES["WAITING"]:
                if (event.type == KEYDOWN and event.key == K_SPACE) or event.type == MOUSEBUTTONDOWN:
                    current_state = STATES["MINIGAME"]
                    press_timer = current_time

            elif current_state == STATES["MINIGAME"]:
                if event.type == KEYDOWN and event.key == K_SPACE and not space_held:
                    space_held = True
                    press_count += 1
                    last_press_time = current_time

                if event.type == KEYUP and event.key == K_SPACE:
                    space_held = False

            elif current_state == STATES["VICTORY"] and event.type == MOUSEBUTTONDOWN:
                running = False
            elif current_state == STATES["GAME_OVER"] and event.type == MOUSEBUTTONDOWN:
                current_state = STATES["WAITING"]
                progress = 0
                scored_clicks = 0

        # Draw background
        if has_background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(background_color)

        # Draw oil drain
        if has_oil_drain:
            drain_rect = oil_drain.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(oil_drain, drain_rect)
        else:
            pygame.draw.rect(screen, (50, 50, 50), oil_drain_rect)  # Fallback rectangle

        # Calculate press speed (presses per second)
        if current_time - press_timer > 1000:
            press_speed = press_count
            press_count = 0
            press_timer = current_time

            if press_speed >= threshold_speed:
                scored_clicks += (press_speed - threshold_speed + 1) * 2
            scored_clicks -= 1  # Lose 1 click per second regardless of press speed

            progress = max(0, scored_clicks)

        # Display instructions
        for i, surface in enumerate(instruction_surfaces):
            rect = surface.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            screen.blit(surface, rect)

        # Draw vertical progress bar on the right
        bar_width = 40  # Made wider
        bar_height = SCREEN_HEIGHT - 40  # Almost full screen height, leaving small margin
        bar_x = SCREEN_WIDTH - 70
        bar_y = 20  # Small margin from top
        progress_height = (progress / win_threshold) * bar_height
        progress_rect = pygame.Rect(bar_x, bar_y + bar_height - progress_height, bar_width, progress_height)
        pygame.draw.rect(screen, (255, 140, 0), progress_rect)  # Changed to orange
        # Added thick outline (4 pixels)
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 4)

        if progress >= win_threshold:
            current_state = STATES["VICTORY"]
        elif scored_clicks <= -10:
            current_state = STATES["GAME_OVER"]

        elif current_state == STATES["VICTORY"]:
            screen.blit(victory_text, victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        elif current_state == STATES["GAME_OVER"]:
            screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
            screen.blit(oil_back_text, oil_back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(be_faster_text, be_faster_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            screen.blit(retry_text, retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

        pygame.display.flip()
        clock.tick(60)

    # Switch to fullscreen before exiting
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Oil Drain Challenge - Fullscreen Mode')

