import pygame
import sys
import os
BASE_DIR = os.path.dirname(__file__)                         # …\VisualNovel
CHAR_DIR = os.path.join(BASE_DIR, 'images', 'characters')
def run_quiz():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 60

    # Colors
    COLORS = {
        "background": (245, 245, 245),
        "primary": (0, 82, 165),
        "success": (0, 128, 0),
        "danger": (200, 0, 0),
        "text": (255, 255, 255),
        "button_hover": (0, 114, 206)
    }

    # Display and caption
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car Parts Education Quiz with Nebula")
    clock = pygame.time.Clock()

    # Load Nebula images
    try:
        nebula_images = {
            "neutral":      pygame.image.load(os.path.join(CHAR_DIR, "nebulaNeutral.png")).convert_alpha(),
            "angry":        pygame.image.load(os.path.join(CHAR_DIR, "nebulaAngry.png")).convert_alpha(),
            "confirm":      pygame.image.load(os.path.join(CHAR_DIR, "nebulaConfirm.png")).convert_alpha(),
            "notification": pygame.image.load(os.path.join(CHAR_DIR, "nebulaNotification.png")).convert_alpha()
        }
        for key in nebula_images:
            nebula_images[key] = pygame.transform.scale(nebula_images[key], (250, 250))
    except Exception as e:
        print(f"Error loading Nebula images from {CHAR_DIR}: {e}")
        pygame.quit()
        sys.exit()

    # Fonts
    font_large = pygame.font.Font(None, 42)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)

    # Game states
    STATES = {"QUIZ": 0, "DIALOGUE": 1}
    current_state = STATES["QUIZ"]

    questions = [
        {
            "question": "What is the primary function of the alternator?",
            "options": [
                "A) Charge the battery while engine runs",
                "B) Power electrical systems",
                "C) Control fuel injection"
            ],
            "correct": [0, 1],
            "explanation": {
                "correct": "Correct! The alternator charges the battery\nand powers electrical systems!\nNebula approves!",
                "incorrect": "Oops! The alternator doesn't control\nfuel injection. Nebula is concerned!"
            }
        },
        {
            "question": "What does a catalytic converter do?",
            "options": [
                "A) Reduce harmful emissions",
                "B) Improve engine performance",
                "C) Filter engine oil"
            ],
            "correct": [0],
            "explanation": {
                "correct": "Great job! Catalytic converters reduce\ntoxic emissions. Nebula is proud!",
                "incorrect": "Not quite! They don't improve performance.\nNebula wants you to try again!"
            }
        }
    ]

    current_question = 0

    class Button:
        def __init__(self, x, y, width, height, text, color, hover_color):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.hover_color = hover_color
            self.is_hovered = False

        def draw(self, surface):
            color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            text_surf = font_medium.render(self.text, True, COLORS["text"])
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    class DialogueBox:
        def __init__(self, message, is_correct):
            self.width = 800
            self.height = 400
            self.rect = pygame.Rect((WIDTH-self.width)//2, (HEIGHT-self.height)//2, self.width, self.height)
            self.message = self.wrap_text(message)
            self.color = COLORS["success"] if is_correct else COLORS["danger"]
            self.button = Button(WIDTH//2-100, HEIGHT-150, 200, 50, 
                                "Next Question" if len(questions) > 1 else "Restart", 
                                COLORS["primary"], COLORS["button_hover"])
            self.nebula_image = nebula_images["confirm"] if is_correct else nebula_images["angry"]

        def wrap_text(self, text):
            wrapped = []
            for line in text.split('\n'):
                words = line.split(' ')
                current_line = []
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    if font_small.size(test_line)[0] <= self.width - 40:
                        current_line.append(word)
                    else:
                        wrapped.append(' '.join(current_line))
                        current_line = [word]
                wrapped.append(' '.join(current_line))
            return wrapped

        def draw(self, surface):
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            surface.blit(self.nebula_image, (self.rect.x - 300, self.rect.centery - 125))
            pygame.draw.rect(surface, self.color, self.rect, border_radius=12)
            y_offset = self.rect.y + 40
            for line in self.message:
                text_surf = font_small.render(line, True, COLORS["text"])
                text_rect = text_surf.get_rect(center=(self.rect.centerx, y_offset))
                surface.blit(text_surf, text_rect)
                y_offset += 40
            self.button.draw(surface)

    quiz_buttons = []
    current_dialogue = None

    def update_question():
        nonlocal quiz_buttons
        quiz_buttons = [
            Button((WIDTH-BUTTON_WIDTH)//2, 200+i*100, BUTTON_WIDTH, BUTTON_HEIGHT,
                   questions[current_question]["options"][i], COLORS["primary"], COLORS["button_hover"])
            for i in range(3)
        ]

    def draw_main_screen():
        screen.fill(COLORS["background"])
        if current_state == STATES["QUIZ"]:
            screen.blit(nebula_images["neutral"], (50, HEIGHT-300))
        title_surf = font_large.render("Car Parts Knowledge Quiz", True, COLORS["primary"])
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, 80)))
        q_surf = font_medium.render(questions[current_question]["question"], True, COLORS["primary"])
        screen.blit(q_surf, q_surf.get_rect(center=(WIDTH//2, 160)))
        for button in quiz_buttons:
            button.draw(screen)

    update_question()

    # Main loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == STATES["QUIZ"]:
                    for i, button in enumerate(quiz_buttons):
                        if button.rect.collidepoint(mouse_pos):
                            is_correct = i in questions[current_question]["correct"]
                            explanation = questions[current_question]["explanation"]["correct" if is_correct else "incorrect"]
                            current_dialogue = DialogueBox(explanation, is_correct)
                            current_state = STATES["DIALOGUE"]
                elif current_state == STATES["DIALOGUE"]:
                    if current_dialogue.button.rect.collidepoint(mouse_pos):
                        if len(questions) > 1:
                            # <-- Removed the invalid 'nonlocal current_question' here
                            current_question = (current_question + 1) % len(questions)
                            update_question()
                        current_state = STATES["QUIZ"]

        if current_state == STATES["QUIZ"]:
            for button in quiz_buttons:
                button.is_hovered = button.rect.collidepoint(mouse_pos)
        elif current_state == STATES["DIALOGUE"]:
            current_dialogue.button.is_hovered = current_dialogue.button.rect.collidepoint(mouse_pos)

        draw_main_screen()
        if current_state == STATES["DIALOGUE"]:
            current_dialogue.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Only run if executed directly
if __name__ == "__main__":
    run_quiz()
