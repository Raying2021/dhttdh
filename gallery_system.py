import json
import os
import pygame

class GallerySystem:
    def __init__(self):
        self.gallery_items = {}
        self.unlocked_items = set()
        self.current_page = 0
        self.items_per_page = 6
        self.ensure_files_exist()
        self.load_gallery_config("gallery_config.json")
        self.load_progress()

    def ensure_files_exist(self):
        """Ensure required files exist with default content."""
        # Create gallery_progress.json if it doesn't exist
        if not os.path.exists("gallery_progress.json"):
            with open("gallery_progress.json", "w", encoding="utf-8") as f:
                json.dump([], f)  # Empty list as default
        
        # Create gallery_config.json if it doesn't exist
        if not os.path.exists("gallery_config.json"):
            with open("gallery_config.json", "w", encoding="utf-8") as f:
                json.dump({}, f)  # Empty dict as default

    def load_gallery_config(self, config_file):
        """Load gallery configuration."""
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8-sig") as f:
                    self.gallery_items = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading gallery config: {e}")
                # Create new empty config
                self.gallery_items = {}

    def load_progress(self):
        """Load previously unlocked items."""
        try:
            if os.path.exists("gallery_progress.json"):
                with open("gallery_progress.json", "r", encoding="utf-8-sig") as f:
                    data = f.read().strip()
                    if data:  # Only try to load if file is not empty
                        items = json.loads(data)
                        self.unlocked_items = set(item["id"] for item in items if item.get("unlocked", False))
                    else:
                        self.unlocked_items = set()
        except Exception as e:
            print(f"Warning: Could not load gallery progress: {e}, starting fresh")
            self.unlocked_items = set()

    def unlock_item(self, item_id):
        """Unlock a gallery item."""
        if item_id in self.gallery_items:
            self.unlocked_items.add(item_id)
            self.save_progress()

    def save_progress(self):
        """Save unlocked items."""
        with open("gallery_progress.json", "w", encoding="utf-8") as f:
            json.dump(list(self.unlocked_items), f)

    def is_item_unlocked(self, item_id):
        """Check if an item is unlocked."""
        return item_id in self.unlocked_items

    def draw(self, screen):
        """Draw gallery items on screen."""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        if not self.gallery_items:
            # Draw "No items available" message
            text = font.render("No gallery items available", True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 
                                            screen.get_height() // 2))
            screen.blit(text, text_rect)
            return
            
        # Draw gallery title
        title = font.render("Gallery", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title, title_rect)
        
        # Calculate item positions (2x3 grid)
        start_x, start_y = 100, 120
        spacing_x, spacing_y = 300, 200
        items_per_row = 3
        
        # Get items for current page
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        items_to_show = list(self.gallery_items.items())[start_idx:end_idx]
        
        # Draw each gallery item
        for i, (item_id, item_data) in enumerate(items_to_show):
            row = i // items_per_row
            col = i % items_per_row
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            # Create item rectangle
            item_rect = pygame.Rect(x, y, 250, 150)
            
            # Draw background
            is_unlocked = item_id in self.unlocked_items
            bg_color = (200, 200, 200) if is_unlocked else (100, 100, 100)
            pygame.draw.rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, (0, 0, 0), item_rect, 2)
            
            # Draw item title
            if is_unlocked:
                title_text = font.render(item_data["title"], True, (0, 0, 0))
            else:
                title_text = font.render("???", True, (50, 50, 50))
            
            title_rect = title_text.get_rect(center=(item_rect.centerx, item_rect.y + 30))
            screen.blit(title_text, title_rect)
            
            # Draw item description or unlock requirement
            if is_unlocked:
                desc_text = small_font.render(item_data["description"], True, (0, 0, 0))
            else:
                desc_text = small_font.render(f"Locked: {item_data['unlock_requirement']}", True, (50, 50, 50))
                
            desc_rect = desc_text.get_rect(center=(item_rect.centerx, item_rect.y + 100))
            screen.blit(desc_text, desc_rect)
        
        # Draw navigation buttons if needed
        if len(self.gallery_items) > self.items_per_page:
            # Prev button
            if self.current_page > 0:
                prev_button = pygame.Rect(50, screen.get_height() - 80, 100, 40)
                pygame.draw.rect(screen, (200, 200, 200), prev_button)
                prev_text = font.render("Prev", True, (0, 0, 0))
                prev_rect = prev_text.get_rect(center=prev_button.center)
                screen.blit(prev_text, prev_rect)
            
            # Next button
            if (self.current_page + 1) * self.items_per_page < len(self.gallery_items):
                next_button = pygame.Rect(screen.get_width() - 150, screen.get_height() - 80, 100, 40)
                pygame.draw.rect(screen, (200, 200, 200), next_button)
                next_text = font.render("Next", True, (0, 0, 0))
                next_rect = next_text.get_rect(center=next_button.center)
                screen.blit(next_text, next_rect)