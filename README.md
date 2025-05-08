# Visual Novel Engine

A simple, customizable visual novel engine built with Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Creating Your Story](#creating-your-story)
  - [The Script File](#the-script-file)
  - [Scene Structure](#scene-structure)
  - [Command Types](#command-types)
  - [Example Script](#example-script)
- [Adding Assets](#adding-assets)
  - [Images](#images)
  - [Audio](#audio)
- [Gallery System](#gallery-system)
- [Save/Load System](#saveload-system)
- [Troubleshooting](#troubleshooting)

## Introduction

This Visual Novel Engine provides a framework for creating interactive stories with images, dialogue, sounds, and basic animations. The engine is built with Pygame and uses a JSON-based scripting system that makes it easy to create and modify your visual novel without extensive programming knowledge.

## Features

- **Script-driven storytelling**: Define your entire story in a JSON file
- **Scene management**: Display backgrounds and characters
- **Dialogue system**: Present character dialogue with names
- **Sound management**: Play background music and sound effects
- **Save/Load system**: Allow players to save and load their progress
- **Gallery system**: Unlock and view art as players progress
- **Simple effects**: Fade transitions, simultaneous actions
- **Customizable UI**: Easy to modify interface elements

## Getting Started

1. Install Python 3.6 or higher
2. Install Pygame: `pip install pygame`
3. Clone this repository or download the source files
4. Run the game: `python main.py`

## Project Structure

- `main.py` - Entry point for the game
- `visual_novel.py` - Core engine functionality
- `scene_manager.py` - Handles backgrounds and characters
- `dialogue_manager.py` - Manages text display and speakers
- `sound_manager.py` - Controls music and sound effects
- `gallery_system.py` - Handles unlockable images/scenes
- `save_system.py` - Manages saving/loading game state
- `resource_loader.py` - Loads and manages assets
- `script.json` - Contains the story script and scene definitions
- `gallery_config.json` - Gallery item configuration
- `gallery_progress.json` - Tracks unlocked gallery items
- `images/` - Directory for background and character images
- `sounds/` - Directory for music and sound effects
- `saves/` - Directory for save files

## Creating Your Story

### The Script File

The story is defined in `script.json`, which contains two main sections:

1. `scenes` - Defines all the backgrounds, characters, and music for each scene
2. `script` - Contains the sequence of commands that drive the story

### Scene Structure

Each scene is defined with:

```json
"scene_name": {
    "background": "path/to/background.png",
    "characters": {
        "character_name": "path/to/character.png"
    },
    "music": "path/to/background_music.mp3"
}
```

### Command Types

The engine supports these command types:

- **scene** - Change to a new scene: `{"type": "scene", "name": "scene_name"}`
- **dialogue** - Display character dialogue: `{"type": "dialogue", "speaker": "Character", "text": "Hello world"}`
- **sound** - Play a sound effect: `{"type": "sound", "file": "path/to/sound.wav"}`
- **music** - Play background music: `{"type": "music", "file": "path/to/music.mp3", "loop": true}`
- **quote** - Display a quote: `{"type": "quote", "text": "An important quote.", "duration": 2.0}`
- **fade** - Fade the screen: `{"type": "fade", "color": [0, 0, 0], "duration": 1.0}`
- **simultaneous** - Execute multiple commands at once: `{"type": "simultaneous", "commands": [...]}`

### Example Script

Here's a simple example script:

```json
{
    "scenes": {
        "classroom": {
            "background": "images/classroom.png",
            "characters": {
                "teacher": "images/characters/teacher.png",
                "student": "images/characters/student.png"
            },
            "music": "sounds/music/classroom_theme.mp3"
        },
        "hallway": {
            "background": "images/hallway.png",
            "characters": {},
            "music": "sounds/music/hallway_theme.mp3"
        }
    },
    "script": [
        {
            "type": "scene",
            "name": "classroom"
        },
        {
            "type": "dialogue",
            "speaker": "Teacher",
            "text": "Welcome to class everyone!"
        },
        {
            "type": "dialogue",
            "speaker": "Student",
            "text": "Good morning, teacher."
        },
        {
            "type": "sound",
            "file": "sounds/sound_effects/bell.wav"
        },
        {
            "type": "fade",
            "color": [0, 0, 0],
            "duration": 1.0
        },
        {
            "type": "scene",
            "name": "hallway"
        },
        {
            "type": "dialogue",
            "speaker": "Student",
            "text": "Time for the next class!"
        }
    ]
}
```

## Adding Assets

### Images

Place your images in the `images/` directory. The engine supports the following structure:

- `images/Act1/`, `images/Act2/`, etc. - Background images for different acts
- `images/characters/` - Character sprites
- `images/icons/` - UI elements and icons

Recommended formats: PNG, JPG
Recommended size for backgrounds: 1024x768 pixels

### Audio

Place your audio files in the `sounds/` directory:

- `sounds/music/` - Background music tracks
- `sounds/sound_effects/` - Short sound effects

Supported formats: MP3, WAV, OGG
Recommended music format: MP3 (better compression)
Recommended sound effect format: WAV (better quality)

## Gallery System

The gallery system allows players to unlock and view artwork as they progress through the story.

### Configuration

Gallery items are defined in `gallery_config.json`:

```json
{
  "item_id": {
    "title": "Item Title",
    "description": "Item description",
    "image_path": "path/to/image.png",
    "category": "Category",
    "unlock_requirement": "Requirements to unlock"
  }
}
```

### Unlocking Items

To unlock an item in your script, you'll need to add code to the engine to call:

```python
gallery.unlock_item("item_id")
```

## Save/Load System

The engine provides a simple save/load system that stores:

- Current position in the script
- Unlocked gallery items
- Game state information

Save files are stored in the `saves/` directory as JSON files.

### Creating Multiple Save Slots

By default, the engine supports 3 save slots, but you can modify this in `save_system.py`:

```python
self.max_saves = 3  # Change this number
```

## Troubleshooting

### Common Issues

1. **Images not showing**: 
   - Check file paths in `script.json`
   - Ensure images are in the correct format (PNG or JPG)
   - Check the console for error messages about missing files

2. **Audio not playing**:
   - Verify file paths in `script.json`
   - Ensure audio files are in supported formats (MP3, WAV, OGG)
   - Check if sound is muted (top-right corner of the game window)

3. **Script errors**:
   - Check your JSON syntax for missing commas or brackets
   - Ensure all required fields are present for each command
   - Look for typos in scene or character names

4. **Performance issues**:
   - Reduce image sizes for better performance
   - Compress audio files appropriately
   - Limit the number of simultaneous elements on screen

### Logging

The engine includes a logging system that writes to game log files in the main directory. Check these logs for detailed error information.

