import os
import json
from game_logger import GameLogger

def load_script(file_path):
    """Load the script from a JSON file."""
    try:
        # Ensure the file path is relative to the main.py directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, file_path)

        with open(full_path, "r", encoding="utf-8") as file:
            script_data = json.load(file)
            
            # Validate script structure
            if not isinstance(script_data, dict):
                GameLogger.error("Invalid script format: root must be an object")
                return None
                
            if "scenes" not in script_data:
                GameLogger.error("Invalid script format: missing 'scenes' section")
                return None
                
            if "script" not in script_data:
                GameLogger.error("Invalid script format: missing 'script' section")
                return None
                
            return script_data
            
    except FileNotFoundError:
        GameLogger.error(f"Script file not found: {full_path}")
        return None
    except json.JSONDecodeError as e:
        GameLogger.error(f"Invalid JSON in script file: {e}")
        return None
    except Exception as e:
        GameLogger.error(f"Unexpected error loading script: {e}")
        return None