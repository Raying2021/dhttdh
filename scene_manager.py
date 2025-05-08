import pygame
import os
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class Scene:
    background: Optional[pygame.Surface] = None
    characters: Dict[str, pygame.Surface] = None
    music: Optional[str] = None
    
    def __post_init__(self):
        print(f"Scene created with background: {self.background}")
        if self.background:
            print(f"Background dimensions: {self.background.get_width()}x{self.background.get_height()}")

class SceneManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_scene = Scene()
        self.scenes = {}
        self.transition_active = False
    
    def load_scene(self, scene_name: str, background, characters: Dict[str, str] = None, music_path: Optional[str] = None):
        """Load a new scene with background and characters."""
        try:
            print(f"Loading scene: {scene_name}")
            print(f"Background type: {type(background)}")
            
            # If background is already a Surface, use it directly
            if isinstance(background, pygame.Surface):
                print("Background is a Surface")
                bg_surface = background
                # Scale if needed
                if bg_surface.get_width() != self.screen_width or bg_surface.get_height() != self.screen_height:
                    print(f"Scaling background from {bg_surface.get_width()}x{bg_surface.get_height()} to {self.screen_width}x{self.screen_height}")
                    bg_surface = pygame.transform.scale(bg_surface, (self.screen_width, self.screen_height))
            else:
                # Otherwise load from path
                print(f"Background is a path: {background}")
                print(f"File exists: {os.path.exists(background)}")
                bg_surface = pygame.image.load(background)
                print(f"Image loaded from path: {bg_surface.get_width()}x{bg_surface.get_height()}")
                bg_surface = pygame.transform.scale(bg_surface, (self.screen_width, self.screen_height))
            
            loaded_characters = {}
            if characters:
                for char_name, char_path in characters.items():
                    print(f"Loading character: {char_name} from {char_path}")
                    char_img = pygame.image.load(char_path)
                    loaded_characters[char_name] = char_img
            
            scene = Scene(
                background=bg_surface,
                characters=loaded_characters,
                music=music_path
            )
            
            print(f"Scene created with background size: {bg_surface.get_width()}x{bg_surface.get_height()}")
            self.scenes[scene_name] = scene
            print(f"Scene {scene_name} successfully added to scenes dictionary")
            
        except Exception as e:
            print(f"Error loading scene {scene_name}: {e}")
    
    def change_scene(self, scene_name: str):
        """Change to a different scene."""
        print(f"Changing to scene: {scene_name}")
        print(f"Available scenes: {list(self.scenes.keys())}")
        
        if scene_name in self.scenes:
            print(f"Scene {scene_name} found")
            self.current_scene = self.scenes[scene_name]
            
            print(f"Current scene set. Background: {self.current_scene.background}")
            print(f"Background size: {self.current_scene.background.get_width()}x{self.current_scene.background.get_height()}")
            
            if self.current_scene.music:
                try:
                    pygame.mixer.music.load(self.current_scene.music)
                    pygame.mixer.music.play(-1)                    
                except Exception as e:
                    print(f"Error playing scene music: {e}")
        else:
            print(f"Scene {scene_name} not found in available scenes!")