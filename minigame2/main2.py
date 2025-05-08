import pygame
import sys
import os
import math
import random
from pygame.locals import *

def start_oil_spill_challenge():
    # Initialize pygame
    pygame.init()

    # Set up the display
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Oil Spill Challenge')

    # Game states
    STATES = {
        "MINIGAME": 0,  # Oil container balancing game
        "GAME_OVER": 1,  # Loss screen
        "VICTORY": 2  # Victory screen from previous game
    }

    current_state = STATES["MINIGAME"]

    # Load images
    base_dir = os.path.dirname(__file__)  # Get the directory of this file

    try:
        background = pygame.image.load(os.path.join(base_dir, 'Car_hood.jpg'))
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        oil_container_path = os.path.join(base_dir, 'plastic-motor-oil-container-3d-model-max-obj-fbx.png')
        print("Loading oil container from:", oil_container_path)  # Debugging
        oil_container_original = pygame.image.load(oil_container_path)
        aspect_ratio = oil_container_original.get_height() / oil_container_original.get_width()
        target_width = 300
        oil_container = pygame.transform.scale(
            oil_container_original, (target_width, int(target_width * aspect_ratio)))
        oil_container = pygame.transform.flip(oil_container, True, False)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(1)
    except pygame.error as e:
        print(f"Couldn't load images: {e}")
        sys.exit(1)

    # Helper function for text with background
    def create_text_with_background(text, font_obj, color=(255, 255, 255)):
        text_surface = font_obj.render(text, True, color)
        background = pygame.Surface(
            (text_surface.get_width() + 20, text_surface.get_height() + 10))
        background.fill((0, 0, 0))
        background.blit(text_surface, (10, 5))
        return background

    # Text setup
    font = pygame.font.Font(None, 72)
    instruction_font = pygame.font.Font(None, 36)
    game_over_text = create_text_with_background("Game Over!", font, (255, 0, 0))
    victory_text = create_text_with_background("You won!!!", font)
    retry_text = create_text_with_background("Retry", font)
    continue_text = create_text_with_background("Click to continue", font)

    # Instructions text
    instructions = [
        "Balance the oil container using your mouse!",
        "Keep the tilt between 30-60 degrees",
        "Hold it steady in range for 5 seconds to win!"
    ]
    instruction_surfaces = [
        create_text_with_background(text, instruction_font)
        for text in instructions
    ]

    # Get rects for text positioning
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT // 2 - 50))
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                 SCREEN_HEIGHT // 2))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2,
                                             SCREEN_HEIGHT // 2 + 100))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                   SCREEN_HEIGHT // 2 + 100))

    # Game variables
    container_pos = [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 100]
    container_angle = 0
    visual_angle = -45
    container_velocity = 0
    balance_threshold = 70
    game_time = 0
    win_time = 300
    start_countdown = 180
    show_ready = False
    show_go = False
    waiting_for_click = True
    countdown_started = False

    # Button
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70,
                               200, 60)

    # Fade variables
    fade_alpha = 255
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if current_state == STATES["GAME_OVER"] and retry_button.collidepoint(mouse_pos):
                    # Reset game with countdown
                    current_state = STATES["MINIGAME"]
                    container_pos = [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 100]
                    container_angle = 0
                    container_velocity = 0
                    game_time = 0
                    start_countdown = 90
                    show_ready = False
                    show_go = False
                    waiting_for_click = True
                    countdown_started = False
                elif current_state == STATES["VICTORY"]:
                    running = False
                elif current_state == STATES["MINIGAME"] and waiting_for_click:
                    waiting_for_click = False
                    countdown_started = True

        # Draw background
        screen.blit(background, (0, 0))

        if current_state == STATES["MINIGAME"]:
            if waiting_for_click:
                # Display instructions only before click
                for i, surface in enumerate(instruction_surfaces):
                    rect = surface.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2 - 100 +
                                                    i * 40))
                    screen.blit(surface, rect)

            elif countdown_started:
                if start_countdown > 0:
                    start_countdown -= 1
                    if start_countdown <= 120 and start_countdown > 60 and not show_ready:
                        show_ready = True
                        show_go = False
                    if start_countdown <= 60 and not show_go:
                        show_go = True
                        show_ready = False

                    if show_ready:
                        ready_text = create_text_with_background("Ready...", font)
                        ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                                 SCREEN_HEIGHT // 3))
                        screen.blit(ready_text, ready_rect)
                    elif show_go:
                        go_text = create_text_with_background("GO!", font)
                        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                           SCREEN_HEIGHT // 3))
                        screen.blit(go_text, go_rect)

                else:
                    # Update container physics
                    mouse_x = pygame.mouse.get_pos()[0]
                    tilt_factor = (mouse_x - (SCREEN_WIDTH // 2)) / 300.0
                    container_velocity += tilt_factor * 0.15
                    container_velocity *= 0.985
                    container_angle += container_velocity

                    # Check for failure
                    if container_angle < -60 or container_angle > -30:
                        game_time = max(0, game_time - 1)
                    else:
                        game_time += 1

                    if container_angle < -70 or container_angle > 20:
                        current_state = STATES["GAME_OVER"]

                    if game_time >= win_time:
                        current_state = STATES["VICTORY"]

        elif current_state == STATES["GAME_OVER"]:
            screen.blit(game_over_text, game_over_rect)
            pygame.draw.rect(screen, (0, 0, 0), retry_button)
            screen.blit(retry_text, retry_rect)

        elif current_state == STATES["VICTORY"]:
            screen.blit(victory_text, victory_rect)
            screen.blit(continue_text, continue_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()