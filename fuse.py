import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 810
FUSE_TYPES = [
    {"color": (255, 0, 0), "shape": "cylinder", "amps": "5A"},    # Red cylinder (5A)
    {"color": (0, 255, 0), "shape": "blade", "amps": "10A"},      # Green blade (10A)
    {"color": (0, 0, 255), "shape": "cylinder", "amps": "15A"},   # Blue cylinder (15A)
    {"color": (255, 255, 0), "shape": "blade", "amps": "20A"},   # Yellow blade (20A)
    {"color": (255, 0, 255), "shape": "cylinder", "amps": "25A"}, # Pink cylinder (25A)
    {"color": (0, 255, 255), "shape": "blade", "amps": "30A"},    # Cyan blade (30A)
    {"color": (255, 165, 0), "shape": "cylinder", "amps": "40A"}, # Orange cylinder (40A)
]
FUSE_WIDTH = 80
FUSE_HEIGHT = 30
MARGIN = 15
FONT_SIZE = 24
LARGE_FONT_SIZE = 48
TITLE_FONT_SIZE = 64
MEMORIZE_TIME = 10
MAX_TRIALS = 3
BASE_SCORE = 1000
TRIAL_PENALTY = 100  # -100 per extra trial

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Fuse Memory Game")
font = pygame.font.SysFont('Arial', FONT_SIZE)
large_font = pygame.font.SysFont('Arial', LARGE_FONT_SIZE)
title_font = pygame.font.SysFont('Arial', TITLE_FONT_SIZE)

class FuseMemoryGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.original_sequence = random.sample(FUSE_TYPES, 7)
        self.shuffled_sequence = self.original_sequence.copy()
        random.shuffle(self.shuffled_sequence)
        self.player_sequence = [None] * 7
        self.game_state = "start"
        self.message = ""
        self.last_display_time = 0
        self.selected_index = -1
        self.trials_remaining = MAX_TRIALS
        self.score = BASE_SCORE
        self.current_trial = 0
        self.locked_positions = set()
        
    def start_game(self):
        self.game_state = "memorizing"
        self.message = "Memorize the fuse arrangement!"
        self.last_display_time = time.time()
        self.current_trial = 0
        self.score = BASE_SCORE
        self.locked_positions = set()
        self.player_sequence = [None] * 7
        self.shuffled_sequence = self.original_sequence.copy()
        random.shuffle(self.shuffled_sequence)
        
    def check_solution(self):
        if None not in self.player_sequence:
            self.current_trial += 1
            
            # Find new correct positions
            new_correct = [i for i in range(7) if self.player_sequence[i] == self.original_sequence[i]]
            self.locked_positions.update(new_correct)
            
            if len(self.locked_positions) == 7:
                trial_penalty = TRIAL_PENALTY * (self.current_trial - 1)
                self.score -= trial_penalty
                self.message = f"SUCCESS! Score: {self.score}"
                self.game_state = "game_over"
            else:
                self.trials_remaining -= 1
                if self.trials_remaining <= 0:
                    self.score = 0
                    self.message = f"GAME OVER! Final score: {self.score}"
                    self.game_state = "game_over"
                else:
                    # Prepare next trial
                    remaining_fuses = [self.original_sequence[i] for i in range(7) if i not in self.locked_positions]
                    self.shuffled_sequence = remaining_fuses.copy()
                    random.shuffle(self.shuffled_sequence)
                    
                    # Reset player sequence with locked positions
                    self.player_sequence = [self.original_sequence[i] if i in self.locked_positions else None for i in range(7)]
                    self.message = f"Locked {len(self.locked_positions)} fuses! {self.trials_remaining} trial(s) left!"

    def handle_click(self, mouse_pos):
        if self.game_state == "playing":
            # Check if clicking on placed fuses (top row)
            if 200 <= mouse_pos[1] <= 200 + FUSE_HEIGHT:
                fuse_index = (mouse_pos[0] - (SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2)) // (FUSE_WIDTH + MARGIN)
                if 0 <= fuse_index < 7 and self.player_sequence[fuse_index] is not None and fuse_index not in self.locked_positions:
                    # Return fuse to shuffled pool and clear the position
                    returned_fuse = self.player_sequence[fuse_index]
                    self.shuffled_sequence.append(returned_fuse)
                    self.player_sequence[fuse_index] = None
                    return
            
            # Check if clicking on shuffled fuses (bottom row)
            if 400 <= mouse_pos[1] <= 400 + FUSE_HEIGHT:
                fuse_index = (mouse_pos[0] - (SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2)) // (FUSE_WIDTH + MARGIN)
                if 0 <= fuse_index < len(self.shuffled_sequence):
                    # Find first empty non-locked position
                    for i in range(7):
                        if self.player_sequence[i] is None and i not in self.locked_positions:
                            self.player_sequence[i] = self.shuffled_sequence.pop(fuse_index)
                            break
            
            # Check submit button
            if (SCREEN_WIDTH//2 - 80 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 80 and
                550 <= mouse_pos[1] <= 610 and None not in self.player_sequence):
                self.check_solution()

    def draw_fuse(self, x, y, fuse, selected=False, locked=False, removable=False):
        if not fuse:
            return pygame.draw.rect(screen, (50, 50, 50), (x, y, FUSE_WIDTH, FUSE_HEIGHT), 0, 5)
            
        # Fuse body
        if fuse["shape"] == "cylinder":
            pygame.draw.ellipse(screen, fuse["color"], (x, y, FUSE_WIDTH, FUSE_HEIGHT))
        else:  # blade type
            pygame.draw.rect(screen, fuse["color"], (x, y, FUSE_WIDTH, FUSE_HEIGHT), 0, 5)
        
        # Amperage label
        amp_text = font.render(fuse["amps"], True, (0, 0, 0))
        screen.blit(amp_text, (x + FUSE_WIDTH//2 - amp_text.get_width()//2, 
                             y + FUSE_HEIGHT//2 - amp_text.get_height()//2))
        
        # Selection/Locked highlight
        if locked:
            border_color = (0, 255, 0)  # Green for locked
            border_width = 3
        elif removable:
            border_color = (255, 100, 100)  # Red for removable
            border_width = 3
        elif selected:
            border_color = (255, 255, 0)  # Yellow for selected
            border_width = 2
        else:
            border_color = (255, 255, 255)  # White for normal
            border_width = 2
        
        if fuse["shape"] == "cylinder":
            pygame.draw.ellipse(screen, border_color, (x, y, FUSE_WIDTH, FUSE_HEIGHT), border_width)
        else:
            pygame.draw.rect(screen, border_color, (x, y, FUSE_WIDTH, FUSE_HEIGHT), border_width, 5)

    def draw_start_screen(self):
        screen.fill((30, 30, 40))
        title = title_font.render("CAR FUSE MEMORY GAME", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        instructions = [
            "How to play:",
            "1. Memorize the fuse arrangement (10 seconds)",
            "2. Click on shuffled fuses to place them",
            "3. Click on placed fuses to remove them",
            f"4. You have {MAX_TRIALS} attempts",
            "5. Correct fuses stay locked in place",
            "6. Score starts at 1000, -100 per extra attempt",
            "7. Score is 0 if you don't solve it!",
            "",
            "Click START to begin!"
        ]
        
        for i, line in enumerate(instructions):
            text = font.render(line, True, (220, 220, 220))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))
        
        # Start button
        pygame.draw.rect(screen, (200, 50, 50), (SCREEN_WIDTH//2 - 120, 550, 240, 80), 0, 15)
        start_text = large_font.render("START", True, (255, 255, 255))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 570))
    
    def draw_memorizing_screen(self):
        screen.fill((40, 40, 50))
        remaining_time = max(0, MEMORIZE_TIME - (time.time() - self.last_display_time))
        time_text = large_font.render(f"Memorize these fuses! Time left: {remaining_time:.1f}s", True, (255, 215, 0))
        screen.blit(time_text, (SCREEN_WIDTH//2 - time_text.get_width()//2, 50))
        
        # Draw fuse box
        pygame.draw.rect(screen, (20, 20, 30), (SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2, 150, 7*FUSE_WIDTH + 6*MARGIN, 200), 0, 10)
        
        for i, fuse in enumerate(self.original_sequence):
            self.draw_fuse(SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2 + i*(FUSE_WIDTH + MARGIN), 200, fuse)
        
        if time.time() - self.last_display_time > MEMORIZE_TIME:
            self.game_state = "playing"
            self.message = "Now recreate the sequence!"

    def draw_playing_screen(self):
        screen.fill((40, 40, 50))
        header = large_font.render(self.message, True, (255, 255, 255))
        screen.blit(header, (SCREEN_WIDTH//2 - header.get_width()//2, 50))
        
        # Fuse box (top row - player's sequence)
        pygame.draw.rect(screen, (20, 20, 30), (SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2, 150, 7*FUSE_WIDTH + 6*MARGIN, 200), 0, 10)
        
        for i in range(7):
            fuse = self.player_sequence[i]
            removable = (fuse is not None and i not in self.locked_positions)
            self.draw_fuse(SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2 + i*(FUSE_WIDTH + MARGIN), 
                          200, fuse, 
                          locked=(i in self.locked_positions),
                          removable=removable)
        
        # Shuffled fuses (bottom row)
        for i, fuse in enumerate(self.shuffled_sequence):
            self.draw_fuse(SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2 + i*(FUSE_WIDTH + MARGIN), 400, fuse, (i == self.selected_index))
        
        # Stats
        trials_text = font.render(f"Trials: {self.trials_remaining}/{MAX_TRIALS}", True, (255, 215, 0))
        score_text = font.render(f"Score: {self.score}", True, (255, 215, 0))
        screen.blit(trials_text, (50, 650))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 50, 650))
        
        # Submit button
        if None not in self.player_sequence:
            pygame.draw.rect(screen, (50, 200, 50), (SCREEN_WIDTH//2 - 80, 550, 160, 60), 0, 10)
            submit_text = large_font.render("CHECK", True, (255, 255, 255))
            screen.blit(submit_text, (SCREEN_WIDTH//2 - submit_text.get_width()//2, 560))

    def draw_game_over_screen(self):
        screen.fill((30, 30, 40))
        result_text = title_font.render(self.message, True, (255, 215, 0))
        screen.blit(result_text, (SCREEN_WIDTH//2 - result_text.get_width()//2, 150))
        
        seq_text = large_font.render("Correct Fuse Arrangement:", True, (220, 220, 220))
        screen.blit(seq_text, (SCREEN_WIDTH//2 - seq_text.get_width()//2, 250))
        
        # Draw fuse box
        pygame.draw.rect(screen, (20, 20, 30), (SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2, 300, 7*FUSE_WIDTH + 6*MARGIN, 200), 0, 10)
        
        for i, fuse in enumerate(self.original_sequence):
            self.draw_fuse(SCREEN_WIDTH//2 - (7*FUSE_WIDTH + 6*MARGIN)//2 + i*(FUSE_WIDTH + MARGIN), 350, fuse)
        
        # Play again button
        pygame.draw.rect(screen, (200, 50, 50), (SCREEN_WIDTH//2 - 120, 550, 240, 80), 0, 15)
        again_text = large_font.render("PLAY AGAIN", True, (255, 255, 255))
        screen.blit(again_text, (SCREEN_WIDTH//2 - again_text.get_width()//2, 570))
    
    def draw(self):
        if self.game_state == "start":
            self.draw_start_screen()
        elif self.game_state == "memorizing":
            self.draw_memorizing_screen()
        elif self.game_state == "playing":
            self.draw_playing_screen()
        elif self.game_state == "game_over":
            self.draw_game_over_screen()

        # Draw the Exit button (common to all screens)
        pygame.draw.rect(screen, (50, 50, 200), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80, 120, 50), 0, 10)
        exit_text = font.render("EXIT", True, (255, 255, 255))
        screen.blit(exit_text, (SCREEN_WIDTH - 150 + 60 - exit_text.get_width() // 2, SCREEN_HEIGHT - 80 + 25 - exit_text.get_height() // 2))
    def start_game_loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if the Exit button is clicked
                    if (SCREEN_WIDTH - 150 <= mouse_pos[0] <= SCREEN_WIDTH - 150 + 120 and
                        SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 80 + 50):
                        running = False  # Exit the game loop
                    
                    if self.game_state == "start":
                        if (SCREEN_WIDTH//2 - 120 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 120 and
                            550 <= mouse_pos[1] <= 630):
                            self.start_game()
                    
                    elif self.game_state == "playing":
                        self.handle_click(mouse_pos)
                    
                    elif self.game_state == "game_over":
                        if (SCREEN_WIDTH//2 - 120 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 120 and
                            550 <= mouse_pos[1] <= 630):
                            self.reset_game()
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
