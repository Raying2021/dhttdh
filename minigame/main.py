import pygame
import sys
import os
from pygame.locals import *

def start_minigame(screen):
    """Run the minigame."""
    # Initialize pygame variables
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800

    # Load images
    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
    try:
        background = pygame.image.load(os.path.join(images_folder, 'Car_hood.png'))
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        oil_cap = pygame.image.load(os.path.join(images_folder, 'oil_cap.png'))
        oil_cap = pygame.transform.scale(oil_cap, (80, 80))

        oil_meter = pygame.image.load(os.path.join(images_folder, 'Oil_Meter.png'))
        oil_meter = pygame.transform.scale(oil_meter, (100, 100))

        inserted_meter = pygame.image.load(os.path.join(images_folder, 'Oil_meter_in.png'))
        inserted_meter = pygame.transform.scale(inserted_meter, (200, 200))
        
        unfilled_meter = pygame.image.load(os.path.join(images_folder, 'Oil_meter_unfilled.png'))
        unfilled_meter = pygame.transform.scale(unfilled_meter, (400, 400))
    except pygame.error as e:
        print(f"Couldn't load images: {e}")
        return "error"

    # Game states
    SCENE_1 = 0
    SCENE_2 = 1
    SCENE_3 = 2
    current_scene = SCENE_1

    # Clickable areas
    oil_cap_rect = oil_cap.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    oil_meter_rect = oil_meter.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
    inserted_meter_rect = inserted_meter.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    unfilled_meter_rect = unfilled_meter.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Animation variables
    oil_cap_alpha = 255
    oil_cap_y = SCREEN_HEIGHT // 2
    oil_cap_rising = False

    # Scene 2 transition variables
    fade_progress = 0
    fade_in = True
    fade_out = False

    # Text setup
    font = pygame.font.Font(None, 36)

    def create_text_surface(text):
        text_surface = font.render(text, True, (255, 255, 255))
        padding = 10
        background = pygame.Surface((text_surface.get_width() + padding * 2, text_surface.get_height() + padding * 2))
        background.fill((0, 0, 0))
        background.blit(text_surface, (padding, padding))
        return background

    error_text = create_text_surface("I can't use this right now")
    lack_oil_text = create_text_surface("The engine lacks oil")
    error_rect = error_text.get_rect(bottom=SCREEN_HEIGHT - 10, centerx=SCREEN_WIDTH // 2)
    show_error = False
    error_timer = 0

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        oil_cap_hover = oil_cap_rect.collidepoint(mouse_pos) and not oil_cap_rising
        oil_meter_hover = oil_meter_rect.collidepoint(mouse_pos)
        unfilled_meter_hover = unfilled_meter_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if current_scene == SCENE_1:
                    if oil_meter_hover and not oil_cap_rising and oil_cap_alpha == 255:
                        show_error = True
                        error_timer = 120
                    elif oil_cap_hover:
                        oil_cap_rising = True
                    elif oil_meter_hover and oil_cap_alpha == 0:
                        current_scene = SCENE_2
                        fade_progress = 0
                        fade_in = True
                elif current_scene == SCENE_3:
                    if unfilled_meter_hover:
                        fade_out = True

        screen.blit(background, (0, 0))

        if current_scene == SCENE_1:
            if oil_cap_rising:
                oil_cap_y -= 2
                oil_cap_alpha = max(0, oil_cap_alpha - 3)
            
            if oil_cap_alpha > 0:
                oil_cap_copy = oil_cap.copy()
                oil_cap_copy.set_alpha(oil_cap_alpha)
                oil_cap_rect.centery = oil_cap_y
                screen.blit(oil_cap_copy, oil_cap_rect)

                if oil_cap_hover and not oil_cap_rising:
                    highlight = pygame.Surface(oil_cap.get_size(), pygame.SRCALPHA)
                    pygame.draw.rect(highlight, (255, 255, 0, 150), highlight.get_rect(), 5)
                    screen.blit(highlight, oil_cap_rect)

            screen.blit(oil_meter, oil_meter_rect)
            if oil_meter_hover and oil_cap_alpha == 0:
                highlight = pygame.Surface(oil_meter.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(highlight, (255, 255, 0, 150), highlight.get_rect(), 5)
                screen.blit(highlight, oil_meter_rect)

            if show_error:
                screen.blit(error_text, error_rect)
                error_timer -= 1
                if error_timer <= 0:
                    show_error = False

        elif current_scene == SCENE_2:
            if fade_in:
                fade_progress = min(255, fade_progress + 5)
                if fade_progress >= 255:
                    fade_in = False

            temp_surface = inserted_meter.copy()
            temp_surface.set_alpha(fade_progress)
            screen.blit(temp_surface, inserted_meter_rect)

            if not fade_in:
                if inserted_meter_rect.collidepoint(mouse_pos):
                    highlight = pygame.Surface(inserted_meter.get_size(), pygame.SRCALPHA)
                    pygame.draw.rect(highlight, (255, 255, 0, 150), highlight.get_rect(), 5)
                    screen.blit(highlight, inserted_meter_rect)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        fade_out = True
                
            if fade_out:
                fade_progress = max(0, fade_progress - 5)
                if fade_progress <= 0:
                    current_scene = SCENE_3
                    fade_progress = 0
                    fade_in = True
                    fade_out = False

        elif current_scene == SCENE_3:
            if fade_in:
                fade_progress = min(255, fade_progress + 5)
                if fade_progress >= 255:
                    fade_in = False

            temp_surface = unfilled_meter.copy()
            temp_surface.set_alpha(fade_progress)
            screen.blit(temp_surface, unfilled_meter_rect)

            if not fade_in:
                screen.blit(lack_oil_text, lack_oil_text.get_rect(bottom=SCREEN_HEIGHT - 10, centerx=SCREEN_WIDTH // 2))
                if unfilled_meter_hover:
                    highlight = pygame.Surface(unfilled_meter.get_size(), pygame.SRCALPHA)
                    pygame.draw.rect(highlight, (255, 255, 0, 150), highlight.get_rect(), 5)
                    screen.blit(highlight, unfilled_meter_rect)

            if fade_out:
                fade_progress = max(0, fade_progress - 5)
                if fade_progress <= 0:
                    running = False

        pygame.display.flip()
        clock.tick(60)

    return "success"  # Return a result when the minigame ends