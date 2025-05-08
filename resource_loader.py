import pygame
import os

class ResourceLoader:
    @staticmethod
    def load_image(path, size=None):
        try:
            # Add debugging output
            print(f"Attempting to load image: {path}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Full path: {os.path.abspath(path)}")
            print(f"File exists: {os.path.exists(path)}")
            
            if not os.path.exists(path):
                print(f"Warning: Image not found: {path}")
                # Create placeholder
                surface = pygame.Surface(size or (100, 100))
                surface.fill((255, 0, 255))  # Magenta for missing texture
                
                # Draw a pattern to make it obvious
                pygame.draw.line(surface, (0, 0, 0), (0, 0), (surface.get_width(), surface.get_height()), 2)
                pygame.draw.line(surface, (0, 0, 0), (0, surface.get_height()), (surface.get_width(), 0), 2)
                
                # Draw text "Missing" on the placeholder
                font = pygame.font.Font(None, 24)
                text = font.render("Missing", True, (0, 0, 0))
                text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
                surface.blit(text, text_rect)
                
                return surface
                
            image = pygame.image.load(path)
            print(f"Image loaded successfully: {path}")
            
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            surface = pygame.Surface(size or (100, 100))
            surface.fill((255, 0, 255))
            
            # Draw text with error message
            font = pygame.font.Font(None, 24)
            text = font.render("Error", True, (0, 0, 0))
            text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
            surface.blit(text, text_rect)
            
            return surface