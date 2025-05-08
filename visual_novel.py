import pygame
import logging
from scene_manager import SceneManager
from state_manager import StateManager
from dialogue_manager import DialogueManager
from sound_manager import SoundManager

class VisualNovel:
    def __init__(self, width=1280, height=720):
        logging.info("Initializing Visual Novel")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize managers
        self.scene_manager = SceneManager(width, height)
        self.state_manager = StateManager()
        self.dialogue_manager = DialogueManager(width, height)
        self.sound_manager = SoundManager()

        # Script management
        self.current_scene = None
        self.script = []
        self.script_index = 0

        # GUI management - arrange buttons horizontally with sound button
        button_width = 80
        button_height = 30
        button_spacing = 10
        sound_button_size = 40
        
        # Adjust start_x to accommodate sound button
        start_x = width - (button_width * 3 + button_spacing * 2 + sound_button_size + button_spacing) - 10
        
        self.buttons = {
            'save': pygame.Rect(start_x, 10, button_width, button_height),
            'load': pygame.Rect(start_x + button_width + button_spacing, 10, button_width, button_height),
            'menu': pygame.Rect(start_x + (button_width + button_spacing) * 2, 10, button_width, button_height)
        }
        
        # Sound button rectangle - positioned to the right of menu button
        self.sound_button_rect = pygame.Rect(
            self.buttons['menu'].right + button_spacing,
            10,
            sound_button_size,
            sound_button_size
        )
        
        # Initialize fonts
        self.font = pygame.font.SysFont('Arial', 28)
        self.gui_font = pygame.font.SysFont('Arial', 20)

        # Dialogue box setup
        self.dialogue_box_rect = pygame.Rect(0, height - 200, width, 200)
        self.waiting_for_click = False
        self.current_text = ""
        self.current_speaker = None

        logging.info("Visual Novel initialization complete")

    def load_script(self, script):
        """Load the script into the game."""
        logging.info(f"Loading script with {len(script)} commands")
        self.script = script
        self.script_index = 0

    def advance_script(self):
        """Advance to the next command in the script."""
        if self.script_index >= len(self.script):
            logging.info("End of script reached")
            self.running = False
            return

        command = self.script[self.script_index]
        command_type = command.get("type", "dialogue")
        logging.debug(f"Executing command type: {command_type}")

        if command_type == "scene":
            self.scene_manager.change_scene(command["name"])
        elif command_type == "dialogue":
            self.current_speaker = command.get("speaker", "")
            self.current_text = command["text"]
            self.waiting_for_click = True
        elif command_type == "sound":
            self.sound_manager.play_sound(command["file"])
        elif command_type == "music":
            self.sound_manager.play_music(command["file"], command.get("loop", False))
        elif command_type == "quote":
            self.current_text = command["text"]
            self.waiting_for_click = True
            pygame.time.wait(int(command["duration"] * 1000))
        elif command_type == "fade":
            self.fade_screen(command["color"], command["duration"])
        elif command_type == "simultaneous":
            for cmd in command["commands"]:
                self.execute_command(cmd)

        self.script_index += 1

    def execute_command(self, command):
        """Execute a single command."""
        command_type = command.get("type", "dialogue")
        print(f"Executing command: {command_type}")
        
        if command_type == "scene":
            print(f"Changing scene to: {command['name']}")
            self.scene_manager.change_scene(command["name"])
            print("Scene change complete")
        elif command_type == "music":
            print(f"Playing music: {command['file']}")
            self.sound_manager.play_music(command["file"], command.get("loop", False))
        elif command_type == "sound":
            print(f"Playing sound: {command['file']}")
            self.sound_manager.play_sound(command["file"])

    def fade_screen(self, color, duration):
        """Fade the screen to a color."""
        print("Starting fade screen effect")
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill(color)
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(int((duration * 1000) / 51))
        print("Fade screen effect completed")

    def draw_gui_buttons(self):
        """Draw GUI buttons including volume control."""
        for button_name, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
            text = self.gui_font.render(button_name.upper(), True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def handle_gui_click(self, pos):
        """Handle GUI button clicks."""
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                logging.info(f"GUI button clicked: {button_name}")
                if button_name == 'save':
                    logging.info("Save functionality not implemented yet")
                    # Placeholder for save functionality
                elif button_name == 'load':
                    logging.info("Load functionality not implemented yet")
                    # Placeholder for load functionality
                elif button_name == 'menu':
                    logging.info("Returning to main menu")
                    self.running = False
                return True
        return False

    def run(self, mute_icon_rect, is_muted, volume_on, volume_off):
        """Main game loop."""
        logging.info("Starting visual novel game loop")
        # Force-set a scene to debug rendering
        print("Current scenes available:", list(self.scene_manager.scenes.keys()))
        if "train" in self.scene_manager.scenes:
            print("Setting initial scene to 'train'")
            self.scene_manager.change_scene("train")
        self.advance_script()

        while self.running:
            self.screen.fill((0, 0, 0))  # Black background as fallback

            # Draw current scene if exists
            try:
                if (self.scene_manager and 
                    self.scene_manager.current_scene and 
                    hasattr(self.scene_manager.current_scene, 'background') and 
                    self.scene_manager.current_scene.background is not None):
                    
                    self.screen.blit(self.scene_manager.current_scene.background, (0, 0))                                        
                else:
                    missing_elements = []
                    if not self.scene_manager:
                        missing_elements.append("scene_manager is None")
                    elif not self.scene_manager.current_scene:
                        missing_elements.append("current_scene is None")
                    elif not hasattr(self.scene_manager.current_scene, 'background'):
                        missing_elements.append("current_scene has no background attribute")
                    elif self.scene_manager.current_scene.background is None:
                        missing_elements.append("background is None")
                    
                    print(f"Cannot draw background. Missing elements: {', '.join(missing_elements)}")
            except Exception as e:
                logging.error(f"Failed to draw scene: {e}")
                print(f"ERROR drawing scene: {e}")
                # Continue with black background

            # Draw dialogue box if we have text
            if self.current_text:
                pygame.draw.rect(self.screen, (255, 255, 255), self.dialogue_box_rect)
                text_surface = self.font.render(self.current_text, True, (0, 0, 0))
                self.screen.blit(text_surface, (20, self.height - 180))

            # Draw GUI components
            self.draw_gui_buttons()
            
            # Draw sound button
            self.screen.blit(
                volume_off if is_muted else volume_on, 
                self.sound_button_rect
            )

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Quit event received")
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    # Handle sound button click
                    if self.sound_button_rect.collidepoint(mouse_pos):
                        is_muted = not is_muted
                        self.sound_manager.toggle_mute()
                        continue
                    
                    if not self.handle_gui_click(event.pos):
                        if self.dialogue_box_rect.collidepoint(event.pos) and self.waiting_for_click:
                            self.waiting_for_click = False
                            self.advance_script()

            pygame.display.flip()
            self.clock.tick(60)

        logging.info("Visual novel game loop ended")