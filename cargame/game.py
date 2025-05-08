import os
import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1535, 810
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Challenge")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 50, 255)
ORANGE = (255, 150, 50)
DARK_BLUE = (10, 10, 40)
GRAY = (100, 100, 100)

# Fonts
title_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# Game variables
clock = pygame.time.Clock()
FPS = 60

# Background particles (starfield)
particles = []
for _ in range(100):
    particles.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(0.2, 0.5),
        'size': random.randint(1, 3),
        'color': random.choice([WHITE, (200, 200, 255), (255, 255, 200)])
    })

# Get the directory of this file
base_dir = os.path.dirname(__file__)

# Load images
try:
    background = pygame.image.load(os.path.join(base_dir, "way.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    player_image = pygame.image.load(os.path.join(base_dir, "car.png"))
    player_image = pygame.transform.scale(player_image, (200, 200))
    obstacle_image = pygame.image.load(os.path.join(base_dir, "cars.png"))
    obstacle_image = pygame.transform.scale(obstacle_image, (200, 200))
except:
    # Fallback if images not found
    background = None
    player_image = None
    obstacle_image = None

# Player setup
player_size = 100
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 120
player_speed = 8

# Obstacles
obstacles = []
obstacle_speed = 4
obstacle_width = 100
obstacle_height = 150
obstacle_frequency = 45

# Game state
current_level = 1
max_unlocked_level = 1
game_active = False
level_complete = False
all_levels_complete = False
score = 0
level_requirements = {1: 25, 2: 30, 3: 45, 4: 50}

# Animation variables
menu_angle = 0
button_pulse = 0
title_glow = 0

def reset_level():
    global player_x, player_y, obstacles, score
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 120
    obstacles = []
    score = 0

def create_obstacle():
    obstacle_x = random.randint(0, WIDTH - obstacle_width)
    obstacles.append(pygame.Rect(obstacle_x, -obstacle_height, obstacle_width, obstacle_height))

def draw_player():
    if player_image:
        screen.blit(player_image, (player_x, player_y))
    else:
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

def update_obstacles():
    global score
    for obstacle in obstacles[:]:
        obstacle.y += obstacle_speed
        if obstacle.top > HEIGHT:
            obstacles.remove(obstacle)
            score += 1

def draw_obstacles():
    for obstacle in obstacles:
        if obstacle_image:
            screen.blit(obstacle_image, (obstacle.x, obstacle.y))
        else:
            pygame.draw.rect(screen, RED, obstacle)

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_size, 150)
    return any(player_rect.colliderect(obstacle) for obstacle in obstacles)

def draw_menu():
    global menu_angle, button_pulse, title_glow
    
    # Animate background
    menu_angle += 0.005
    button_pulse = math.sin(pygame.time.get_ticks() * 0.002) * 5
    title_glow = math.sin(pygame.time.get_ticks() * 0.001) * 0.2 + 0.8
    
    # Draw animated space background
    screen.fill(DARK_BLUE)
    for particle in particles:
        particle['y'] += particle['speed']
        if particle['y'] > HEIGHT:
            particle['y'] = 0
            particle['x'] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, particle['color'], 
                          (int(particle['x']), int(particle['y'])), 
                          particle['size'])
    
    # Title with glow effect
    title_text = title_font.render("COSMIC CHALLENGE", True, 
                                 (int(255*title_glow), int(255*title_glow), int(255*title_glow)))
    title_shadow = title_font.render("COSMIC CHALLENGE", True, (50, 50, 100))
    
    for i in range(3):
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + i, 
                                 80 + i))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80))
    
    # Subtitle
    subtitle = small_font.render("Journey Through the Cosmic Levels", True, 
                               (200, 200, 255))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 160))
    
    # Level buttons with animation
    level_colors = [BLUE, GREEN, YELLOW, ORANGE]
    
    for i in range(1, 5):
        button_y = 250 + i * 90
        button_rect = pygame.Rect(WIDTH//2 - 110, button_y - 5, 220, 70)
        
        # Button glow effect for unlocked levels
        if i <= max_unlocked_level:
            button_color = level_colors[i-1]
            glow_size = int(10 + button_pulse)
            
            # Button glow
            for j in range(glow_size, 0, -2):
                alpha = 100 - j * 10
                if alpha > 0:
                    glow_surf = pygame.Surface((220 + j*2, 70 + j*2), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (*button_color[:3], alpha), 
                                    (0, 0, 220 + j*2, 70 + j*2), 
                                    border_radius=10)
                    screen.blit(glow_surf, (WIDTH//2 - 110 - j, button_y - 5 - j))
        
        # Button itself
        if i <= max_unlocked_level:
            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            level_text = font.render(f"LEVEL {i}", True, WHITE)
            req_text = small_font.render(f"{level_requirements[i]} points", True, WHITE)
        else:
            pygame.draw.rect(screen, (50, 50, 70), button_rect, border_radius=10)
            level_text = font.render(f"LEVEL {i}", True, (100, 100, 100))
            req_text = small_font.render("LOCKED", True, (100, 100, 100))
        
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, button_y))
        screen.blit(req_text, (WIDTH//2 - req_text.get_width()//2, button_y + 35))
    
    # Footer instructions
    footer = small_font.render("Use arrow keys to move • Avoid the oncoming cars", True, 
                             (150, 150, 255))
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 40))

def draw_level_complete():
    # Draw starfield background
    screen.fill(DARK_BLUE)
    for particle in particles:
        pygame.draw.circle(screen, particle['color'], 
                          (int(particle['x']), int(particle['y'])), 
                          particle['size'])
    
    message = font.render(f"Level {current_level} Complete!", True, GREEN)
    screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - 50))
    
    next_text = small_font.render("Ready for the next challenge?", True, WHITE)
    screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 20))
    
    continue_text = small_font.render("Press any key to continue", True, YELLOW)
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 80))

def draw_all_levels_complete():
    # Draw starfield background
    screen.fill(DARK_BLUE)
    for particle in particles:
        pygame.draw.circle(screen, particle['color'], 
                          (int(particle['x']), int(particle['y'])), 
                          particle['size'])
    
    message = font.render("CONGRATULATIONS!", True, YELLOW)
    screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - 80))
    
    complete_text = font.render("You mastered all levels!", True, GREEN)
    screen.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, HEIGHT//2 - 20))
    
    stats = [
        f"Total score: {sum(level_requirements.values())} points",
        "You're a true champion!"
    ]
    
    for i, line in enumerate(stats):
        text = small_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 40 + i*30))
    
    return_text = small_font.render("Press any key to return to menu", True, YELLOW)
    screen.blit(return_text, (WIDTH//2 - return_text.get_width()//2, HEIGHT//2 + 120))

def draw_game():
    # Draw background (road if available, otherwise starfield)
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(DARK_BLUE)
        for particle in particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    draw_player()
    draw_obstacles()
    
    # Game info display
    level_text = small_font.render(f"LEVEL: {current_level}", True, WHITE)
    screen.blit(level_text, (20, 20))
    
    score_text = small_font.render(f"SCORE: {score}/{level_requirements[current_level]}", True, 
                                 GREEN if score >= level_requirements[current_level] else WHITE)
    screen.blit(score_text, (20, 50))
    
    # Progress bar
    progress = min(score / level_requirements[current_level], 1)
    pygame.draw.rect(screen, GRAY, (20, 90, 200, 20))
    pygame.draw.rect(screen, GREEN, (20, 90, 200 * progress, 20))

def handle_level_completion():
    global max_unlocked_level, current_level, level_complete, all_levels_complete
    if current_level < 4:
        max_unlocked_level = current_level + 1
        level_complete = True
    else:
        all_levels_complete = True
def draw_exit_button():
    # Draw the Exit button
    exit_rect = pygame.Rect(WIDTH - 150, HEIGHT - 80, 120, 50)
    pygame.draw.rect(screen, (200, 50, 50), exit_rect, border_radius=10)
    exit_text = small_font.render("EXIT", True, WHITE)
    screen.blit(exit_text, (WIDTH - 150 + 60 - exit_text.get_width() // 2, HEIGHT - 80 + 25 - exit_text.get_height() // 2))
    return exit_rect
def start_cosmic_challenge():
    global running, game_active, level_complete, all_levels_complete, current_level, max_unlocked_level, score, obstacles
    global player_x, player_y, screen  # Add screen to global variables

    # Initialize the game in windowed mode
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Start in windowed mode
    pygame.display.set_caption("Cosmic Challenge")

    # Reset game variables
    running = True
    game_active = False
    level_complete = False
    all_levels_complete = False
    current_level = 1
    max_unlocked_level = 1
    score = 0
    obstacles = []

    # Main game loop
    frame_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the Exit button is clicked
                exit_rect = pygame.Rect(WIDTH - 150, HEIGHT - 80, 120, 50)
                if exit_rect.collidepoint(mouse_pos):
                    # Switch to fullscreen mode and exit the game loop
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    return  # Exit the game and return control to the main script
                
                if not game_active and not level_complete:
                    for i in range(1, max_unlocked_level + 1):
                        button_rect = pygame.Rect(WIDTH//2 - 110, 245 + i * 90, 220, 70)
                        if button_rect.collidepoint(mouse_pos):
                            current_level = i
                            reset_level()
                            game_active = True
            
            if event.type == pygame.KEYDOWN:
                if level_complete:
                    level_complete = False
                    current_level += 1
                    reset_level()
                    game_active = True
                elif all_levels_complete:
                    all_levels_complete = False
                    current_level = 1
                    reset_level()
        
        if game_active:
            # Player movement
            keys = pygame.key.get_pressed()
            player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
            player_x = max(0, min(WIDTH - player_size, player_x))
            
            # Level-specific settings
            level_settings = {
                1: {'speed': 4, 'frequency': 45},
                2: {'speed': 6, 'frequency': 35},
                3: {'speed': 8, 'frequency': 25},
                4: {'speed': 10, 'frequency': 15}
            }
            settings = level_settings[current_level]
            obstacle_speed = settings['speed']
            
            # Spawn obstacles
            frame_count += 1
            if frame_count >= settings['frequency']:
                create_obstacle()
                frame_count = 0
            
            # Update game state
            update_obstacles()
            
            # Check for collisions
            if check_collision():
                game_active = False
                reset_level()
            
            # Check level completion
            if score >= level_requirements[current_level]:
                handle_level_completion()
                game_active = False
            
            # Draw game
            draw_game()
        
        elif level_complete:
            draw_level_complete()
        elif all_levels_complete:
            draw_all_levels_complete()
        else:
            draw_menu()
        
        # Draw the Exit button on all screens
        draw_exit_button()
        
        pygame.display.flip()
        clock.tick(FPS)