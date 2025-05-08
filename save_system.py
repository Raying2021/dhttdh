import json
import os
from datetime import datetime
import pygame

class SaveSystem:
    def __init__(self):
        self.save_folder = "saves"
        self.max_saves = 3
        self.ensure_save_folder_exists()
        self.save_button_rect = None
        self.load_button_rect = None
        self.font = pygame.font.Font(None, 24)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

    def ensure_save_folder_exists(self):
        """Create saves folder if it doesn't exist."""
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def setup_buttons(self, screen_width):
        """Create save/load buttons position."""
        self.save_button_rect = pygame.Rect(screen_width - 160, 20, 60, 40)
        self.load_button_rect = pygame.Rect(screen_width - 230, 20, 60, 40)

    def save_game(self, game_state, slot_number):
        """Save game to a specific slot."""
        filename = f"save_{slot_number}.json"
        filepath = os.path.join(self.save_folder, filename)
        
        # Add timestamp to save data
        game_state['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(filepath, "w") as f:
            json.dump(game_state, f)
            print("Game progress saved.")
        return filename
    def delete_save(self, slot):
        """Delete a save file."""
        filename = f"save_{slot}.json"
        filepath = os.path.join(self.save_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Save slot {slot} deleted.")
        else:
            print(f"Save slot {slot} does not exist.")

    def load_game(self, slot):
        """Load the saved game progress."""
        filename = f"save_{slot}.json"  # Corrected filename format
        filepath = os.path.join(self.save_folder, filename)
        try:
            with open(filepath, "r") as save_file:
                save_data = json.load(save_file)
                if "current_command_index" in save_data:
                    print("Game progress loaded.")
                    return save_data
                else:
                    print("Invalid save data format.")
                    return None
        except FileNotFoundError:
            print("No saved game found.")
            return None

    def get_save_info(self):
        """Get information about all save slots."""
        save_info = []
        for slot in range(1, self.max_saves + 1):
            filepath = os.path.join(self.save_folder, f"save_{slot}.json")
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    data = json.load(f)
                    save_info.append({
                        'slot': slot,
                        'timestamp': data.get('timestamp', 'Unknown'),
                        'exists': True
                    })
            else:
                save_info.append({
                    'slot': slot,
                    'timestamp': None,
                    'exists': False
                })
        return save_info

    def draw_buttons(self, screen):
        """Draw save/load text buttons."""
        for button, text in [(self.save_button_rect, "Save"), 
                           (self.load_button_rect, "Load")]:
            pygame.draw.rect(screen, self.GRAY, button)
            pygame.draw.rect(screen, self.BLACK, button, 2)
            text_surface = self.font.render(text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)