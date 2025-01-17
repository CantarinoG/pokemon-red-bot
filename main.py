from input_controller import InputController
from screen_capture import ScreenCapture
from battle_state import BattleState
from template_matcher import TemplateMatcher
from gui_logger import GUILogger

window_name = "RetroArch Gambatte v0.5.0-netlink"
character_section_bbox = (844, 430, 960, 580)
bottom_section_bbox = (360, 484, 1574, 1079)
my_pokemon_section_bbox = (362, 306, 917, 733)
enemy_pokemon_section_bbox = (984, 0, 1564, 423)
moves_section_bbox = (614, 678, 1609, 1110)
pp_section_bbox = (406, 529, 970, 750)
matching_threshold = 0.03

input_controller = InputController()
screen_capture = ScreenCapture()
template_matcher = TemplateMatcher()
gui_logger = GUILogger()

focused_succesfully = input_controller.focus_window(window_name)
if (not focused_succesfully):
    print("Error: Failed to focus window. Please make sure the emulator is running.")
    exit(1)

battle_state = None

while True:
    screen_capture.capture_screen()

    character_section = screen_capture.get_screen_section(character_section_bbox)
    character_match = template_matcher.get_best_match_from_folder("assets/character_sprites", character_section)
    if character_match["difference"] <= matching_threshold:
        battle_state = None
        input_controller.press_next_direction()
        gui_logger.display("Searching for pokemons to battle...")
        continue

    bottom_section = screen_capture.get_screen_section(bottom_section_bbox)
    action_match = template_matcher.get_match_value("assets/actions.png", bottom_section)
    if action_match["difference"] <= matching_threshold and not battle_state:
        my_pokemon_section = screen_capture.get_screen_section(my_pokemon_section_bbox)
        my_pokemon_match = template_matcher.get_best_match_from_folder("assets/pokemon_back_sprites", my_pokemon_section)
        enemy_pokemon_section = screen_capture.get_screen_section(enemy_pokemon_section_bbox)
        enemy_pokemon_match = template_matcher.get_best_match_from_folder("assets/pokemon_front_sprites", enemy_pokemon_section)
        battle_state = BattleState()
        battle_state.my_pokemon_name = my_pokemon_match["name"]
        battle_state.enemy_pokemon_name = enemy_pokemon_match["name"]
        battle_state.get_pokemon_types()
        gui_logger.display(battle_state.to_string())
        continue

    if action_match["difference"] <= matching_threshold:
        input_controller.press_x()
        continue

    move_selection_match = template_matcher.get_match_value("assets/move_selection.png", bottom_section)
    if move_selection_match["difference"] <= matching_threshold and not battle_state.moves:
        moves_section = screen_capture.get_screen_section(moves_section_bbox)
        moves_found = template_matcher.get_n_best_matches_from_folder(4, "assets/moves", moves_section)
        battle_state.moves = [{"name": move["name"], "damage": 0} for move in moves_found]
        battle_state.update_moves_damage()
        gui_logger.display(battle_state.to_string())
        number_of_moves = battle_state.get_movements_to_highest_damage()
        for _ in range(number_of_moves):
            input_controller.press_down()
        continue
    
    if move_selection_match["difference"] <= matching_threshold:
        pp_section = screen_capture.get_screen_section(pp_section_bbox)
        no_pp_match = template_matcher.get_match_value("assets/0_pp.png", pp_section)
        if no_pp_match["difference"] <= matching_threshold:
            battle_state.moves[battle_state.move_selected]["damage"] = -1
            number_of_moves = battle_state.get_movements_to_highest_damage()
            for _ in range(number_of_moves):
                input_controller.press_down()
            continue
        else:
            input_controller.press_x()

    input_controller.press_z()