import pygame
import sys
import os
from constants import *
from dialogue_system import draw_dialogue
from menu_system import create_button, create_mute_icon, draw_gallery_screen, draw_dialogue
from script_loader import load_script
from assets import ICONS, CHARACTERS
from save_system import SaveSystem  # Import the SaveSystem class
from minigame.main import start_minigame  # Adjust the import path if necessary
from quiz import run_quiz  # Adjust the import path if necessary
from gallery_system import GallerySystem
from tube_game.tire import run_graduated_tube_game  # Adjust the import path if necessary
from test.challenge import UnderTheHoodGame
from fuse import FuseMemoryGame  # Adjust the import path if necessary
from cargame.game import start_cosmic_challenge
from minigame2.main import start_minigame  # Adjust the import path if necessary
from minigame2.main2 import start_oil_spill_challenge
from minigame2.main3 import start_oil_drain_challenge

# Set the working directory to the directory where main.py is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

# Define colors
RED = (255, 0, 0)

# instantiate the gallery
gallery = GallerySystem()


# Initialize the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
pygame.display.set_caption("CarCare")

# Load and scale mute/unmute icons
icon_size = 30  # Match the size defined in create_mute_icon
volume_off = pygame.transform.scale(pygame.image.load(ICONS["volume_off"]), (icon_size, icon_size))
volume_on = pygame.transform.scale(pygame.image.load(ICONS["volume_on"]), (icon_size, icon_size))

# Initialize global states
is_muted = False
current_screen = "main_menu"


    
# Initialize the Save System
save_system = SaveSystem()
save_system.setup_buttons(WINDOW_WIDTH)

def draw_character(screen, character_surf, position):
    """Draw `character_surf` at left/center/right on `screen`."""
    w, h = screen.get_size()
    if position == "left":
        x, y = 50, h - character_surf.get_height() - 50
    elif position == "center":
        x = (w - character_surf.get_width()) // 2
        y = h - character_surf.get_height() - 50
    elif position == "right":
        x = w - character_surf.get_width() - 50
        y = h - character_surf.get_height() - 50
    else:
        x, y = 0, 0
    screen.blit(character_surf, (x, y))

def show_pause_menu():
    """Display the pause menu."""
    menu_running = True

    # Create a semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(150)  # Set transparency
    overlay.fill(BLACK)

    # Draw menu options
    font = pygame.font.Font(None, 50)
    return_text = font.render("Return to Main Menu", True, WHITE)
    return_rect = return_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    while menu_running:
        screen.blit(overlay, (0, 0))
        screen.blit(return_text, return_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_rect.collidepoint(mouse_pos):
                    return "main_menu"  # Return to the main menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False  # Close the pause menu

    return None  # Resume the game
def show_save_selection_menu():
    """Display the save selection menu."""
    menu_running = True

    # Get save information
    save_info = save_system.get_save_info()

    # Create a semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(150)  # Set transparency
    overlay.fill(BLACK)

    # Draw menu options
    font = pygame.font.Font(None, 36)
    options = []
    for i, save in enumerate(save_info):
        text = f"Slot {save['slot']}: {save['timestamp']}" if save['exists'] else f"Slot {save['slot']}: Empty"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 50))
        options.append((text_surface, text_rect, save['slot'], save['exists']))

    delete_font = pygame.font.Font(None, 28)
    delete_text = delete_font.render("Click to delete a save (Right-click)", True, RED)
    delete_rect = delete_text.get_rect(center=(WINDOW_WIDTH // 2, 400))

    while menu_running:
        screen.blit(overlay, (0, 0))

        # Draw save slots
        for text_surface, text_rect, _, _ in options:
            screen.blit(text_surface, text_rect)

        # Draw delete instruction
        screen.blit(delete_text, delete_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for _, text_rect, slot, exists in options:
                    if text_rect.collidepoint(mouse_pos):
                        if event.button == 1:  # Left-click to load
                            if exists:
                                return slot  # Return the selected slot
                        elif event.button == 3:  # Right-click to delete
                            if exists:
                                save_system.delete_save(slot)
                                save_info = save_system.get_save_info()  # Refresh save info
                                options = []
                                for i, save in enumerate(save_info):
                                    text = f"Slot {save['slot']}: {save['timestamp']}" if save['exists'] else f"Slot {save['slot']}: Empty"
                                    text_surface = font.render(text, True, WHITE)
                                    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 50))
                                    options.append((text_surface, text_rect, save['slot'], save['exists']))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False  # Close the menu

    return None  # No save selected

def start_new_game(start_index=0):
    global current_screen
    script = load_script("script.json")
    if not script: return
    # Setup audio
    pygame.mixer.set_num_channels(3)
    sfx_channel = pygame.mixer.Channel(1)
    amb_channel = pygame.mixer.Channel(2)

    curr_bg = None; curr_bg_file = ""
    curr_char = None; curr_char_pos = None
    in_zoom = False

    def size(): return screen.get_width(), screen.get_height()
    font_b = pygame.font.Font(None, 28)
    sw, sh = size()
    save_s = font_b.render("Save", True, WHITE)
    load_s = font_b.render("Load", True, WHITE)
    save_r = save_s.get_rect(topleft=(sw-200, 10))
    load_r = load_s.get_rect(topleft=(sw-100, 10))
    skip = start_index > 0

    for idx, cmd in enumerate(script['script']):
        if idx < start_index and skip:
            if cmd['type'] == 'background':
                curr_bg_file, img = cmd['file'], pygame.image.load(cmd['file'])
                curr_bg = pygame.transform.scale(img, size())
            elif cmd['type'] == 'character':
                ch = CHARACTERS.get(cmd['name'])
                if ch:
                    surf = pygame.transform.scale(pygame.image.load(ch['file']), ch['size'])
                    curr_char, curr_char_pos = surf, cmd.get('position', ch['default_position'])
            elif cmd['type'] == 'hide_character': curr_char = None; curr_char_pos = None
            continue
        skip = False
        screen.fill(WHITE)
        # background
        if cmd['type'] == 'background':
            curr_bg_file, img = cmd['file'], pygame.image.load(cmd['file'])
            curr_bg = pygame.transform.scale(img, size()); screen.blit(curr_bg, (0, 0)); pygame.display.flip()
        # character
        elif cmd['type'] == 'character':
            name = cmd.get('name', '')
            if name and name in CHARACTERS and 'file' in CHARACTERS[name]:
                ch = CHARACTERS[name]
                img = pygame.image.load(ch['file'])
                surf = pygame.transform.scale(img, ch['size'])
                curr_char, curr_char_pos = surf, cmd.get('position', ch.get('default_position'))
            else:
                curr_char = None
                curr_char_pos = None

        # hide
        elif cmd['type'] == 'hide_character': curr_char = None; curr_char_pos = None

        elif cmd['type'] == 'dialogue':
            if curr_bg: screen.blit(curr_bg, (0, 0))
            if curr_char and curr_char_pos: draw_character(screen, curr_char, curr_char_pos)
            draw_dialogue(screen, cmd.get('speaker', ''), cmd['text'])
            pygame.draw.rect(screen, GRAY, save_r); pygame.draw.rect(screen, GRAY, load_r)
            screen.blit(save_s, save_r); screen.blit(load_s, load_r); pygame.display.flip()
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: save_system.save_game({'current_command_index': idx}, 1); pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        r = show_pause_menu()
                        if r == 'main_menu': return
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if save_r.collidepoint(e.pos): save_system.save_game({'current_command_index': idx}, 1)
                        elif load_r.collidepoint(e.pos):
                            slot = show_save_selection_menu()
                            data = save_system.load_game(slot) if slot else None
                            if data: start_new_game(data.get('current_command_index', 0)); return
                        else: waiting = False
        # sound
        elif cmd['type'] == 'quiz':
            run_quiz()

        elif cmd['type'] == 'tube_game':
            run_graduated_tube_game()  # Run the mini-game
            continue  # Ensure the script continues to the next command
        elif cmd['type'] == 'under_the_hood_game':
            UnderTheHoodGame().start_game()
            continue  # Ensure the script continues to the next command
        if cmd['type'] == 'cosmic_challenge':
            start_cosmic_challenge()  # Start the Cosmic Challenge game
            continue  # Ensure the script continues to the next command
        elif cmd['type'] == 'fuse_game':
                game = FuseMemoryGame()
                game.start_game_loop()  # Start the Fuse Memory Game
                continue  # Ensure the script continues to the next command
        if cmd['type'] == 'minigame2':
            start_minigame()  # Start the minigame
            continue  # Ensure the script continues to the next command
        elif cmd['type'] == 'oil_spill_challenge':
            start_oil_spill_challenge()# Start the Oil Spill Challenge minigame
            continue  # Ensure the script continues to the next command
        elif cmd['type'] == 'oil_drain_challenge':
            start_oil_drain_challenge()# Start the Oil Spill Challenge minigame
            continue  # Ensure the script continues to the next command
        
        elif cmd['type'] == 'sound':
            snd = pygame.mixer.Sound(cmd['file']) if cmd.get('file') else None
            if cmd.get('channel') == 'ambient':
                if snd and cmd.get('loop'): amb_channel.play(snd, loops=-1)
                else: amb_channel.stop()
            elif snd: snd.set_volume(0.3); sfx_channel.play(snd)
        # music
        elif cmd['type'] == 'music':
            if cmd.get('file'):
                pygame.mixer.music.load(cmd['file'])
                pygame.mixer.music.play(-1 if cmd.get('loop') else 0)
            elif cmd.get('stop', False):  # Stop music if "stop" is explicitly set to True
                pygame.mixer.music.stop()
        # fade
        elif cmd['type'] == 'fade':
            col = cmd.get('color', 'BLACK').upper(); fc = BLACK if col == 'BLACK' else WHITE; dur = cmd.get('duration', 1.0)
            fs = pygame.Surface(size()); fs.fill(fc); fs.set_alpha(0)
            clock = pygame.time.Clock(); a_step = 255 / (dur * 60); a = 0
            while a < 255:
                fs.set_alpha(int(a))
                if curr_bg: screen.blit(curr_bg, (0, 0))
                screen.blit(fs, (0, 0)); pygame.display.flip(); a += a_step; clock.tick(60)
        
        # wait
        elif cmd['type'] == 'wait':
            d = cmd.get('duration', 1.0)
            if 'black_screen' in curr_bg_file.lower():
                in_zoom = True; clock = pygame.time.Clock(); zf = 1.0; tz = 1.05; steps = int(d * 60); zs = (tz - zf) / steps
                ob = pygame.Surface(size()); ob.fill((20, 20, 20))
                for _ in range(steps):
                    zf += zs; zw = int(size()[0] * zf); zh = int(size()[1] * zf)
                    zz = pygame.transform.smoothscale(ob, (zw, zh))
                    screen.fill(BLACK); screen.blit(zz, ((size()[0] - zw) // 2, (size()[1] - zh) // 2)); pygame.display.flip(); clock.tick(60)
                in_zoom = False
            else: pygame.time.delay(int(d * 1000))
        # minigame
        elif cmd['type'] == 'minigame': start_minigame(screen)


def main():
    """Main game loop."""
    global current_screen, is_muted

    # Create buttons
    buttons = [
        create_button("New Game", 300),
        create_button("Continue", 400),
        create_button("Gallery", 500)
    ]

    mute_icon_rect = create_mute_icon()
    gallery = GallerySystem()   # ← instantiate here

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        # === MAIN MENU SCREEN ===
        if current_screen == "main_menu":
            # Draw title
            title_text = TITLE_FONT.render("CarCare", True, BLACK)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
            screen.blit(title_text, title_rect)

            # Draw buttons
            for text_surf, text_rect, btn_rect in buttons:
                pygame.draw.rect(screen, GRAY, btn_rect)
                pygame.draw.rect(screen, BLACK, btn_rect, 2)
                screen.blit(text_surf, text_rect)

            # Draw mute/unmute icon
            screen.blit(volume_off if is_muted else volume_on, mute_icon_rect)

            # Draw save/load buttons
            save_system.draw_buttons(screen)

        # === GALLERY SCREEN ===
        elif current_screen == "gallery":
            gallery.draw(screen)

            # Draw Back button
            back_font = pygame.font.Font(None, 36)
            back_text = back_font.render("← Back", True, BLACK)
            back_rect = back_text.get_rect(topleft=(20, 20))
            screen.blit(back_text, back_rect)

        # Flip & tick here so both screens render first
        pygame.display.flip()
        clock.tick(60)

        # === EVENT HANDLING ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Main Menu clicks
                if current_screen == "main_menu":
                    # Buttons
                    for i, (_, _, btn_rect) in enumerate(buttons):
                        if btn_rect.collidepoint(mx, my):
                            if i == 0:
                                start_new_game()
                            elif i == 1:
                                slot = show_save_selection_menu()
                                if slot:
                                    data = save_system.load_game(slot)
                                    if data:
                                        start_new_game(data.get("current_command_index", 0))
                            elif i == 2:
                                current_screen = "gallery"

                    # Mute icon
                    if mute_icon_rect.collidepoint(mx, my):
                        is_muted = not is_muted

                # Gallery clicks
                elif current_screen == "gallery":
                    # Back to main menu
                    if back_rect.collidepoint(mx, my):
                        current_screen = "main_menu"
                        continue

                    # Prev page
                    prev_rect = pygame.Rect(50, screen.get_height() - 80, 100, 40)
                    if gallery.current_page > 0 and prev_rect.collidepoint(mx, my):
                        gallery.current_page -= 1

                    # Next page
                    next_rect = pygame.Rect(
                        screen.get_width() - 150,
                        screen.get_height() - 80,
                        100, 40
                    )
                    if (gallery.current_page + 1) * gallery.items_per_page \
                       < len(gallery.gallery_items) \
                       and next_rect.collidepoint(mx, my):
                        gallery.current_page += 1



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()