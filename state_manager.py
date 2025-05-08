from enum import Enum
from typing import Optional, Dict, Any

class GameState(Enum):
    MAIN_MENU = "main_menu"
    GAMEPLAY = "gameplay"
    DIALOGUE = "dialogue"
    GALLERY = "gallery"
    LOAD_MENU = "load_menu"
    SAVE_MENU = "save_menu"
    PAUSED = "paused"

class StateManager:
    def __init__(self):
        self.current_state = GameState.MAIN_MENU
        self.previous_state = None
        self.state_data: Dict[str, Any] = {}
        self._state_handlers = {}
        self.dialogue_state = {
            "current_text": "",
            "current_speaker": None,
            "text_animation_done": False,
            "ready_for_input": True
        }

    def register_state_handler(self, state: GameState, handler):
        """Register a handler function for a specific state."""
        self._state_handlers[state] = handler

    def change_state(self, new_state: GameState):
        """Change to a new state while preserving the previous one."""
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Call state handler if exists
        if new_state in self._state_handlers:
            self._state_handlers[new_state]()

    def revert_to_previous(self):
        """Return to the previous state if it exists."""
        if self.previous_state:
            self.current_state = self.previous_state
            self.previous_state = None

    def set_dialogue_state(self, text: str, speaker: Optional[str] = None):
        """Update dialogue state."""
        self.dialogue_state.update({
            "current_text": text,
            "current_speaker": speaker,
            "text_animation_done": False,
            "ready_for_input": False
        })

    def is_dialogue_ready(self) -> bool:
        """Check if dialogue is ready for next input."""
        return self.dialogue_state["text_animation_done"] and self.dialogue_state["ready_for_input"]

    def store_state_data(self, key: str, value: Any):
        """Store arbitrary data associated with current state."""
        self.state_data[key] = value

    def get_state_data(self, key: str, default: Any = None) -> Any:
        """Retrieve stored state data."""
        return self.state_data.get(key, default)