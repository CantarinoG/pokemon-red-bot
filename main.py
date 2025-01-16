import subprocess
import time
import pyscreenshot as ImageGrab
import os
import cv2
import numpy as np
import tkinter as tk

def create_overlay_window():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Keep window on top
    root.attributes('-alpha', 0.8)     # Make slightly transparent
    root.overrideredirect(True)        # Remove window decorations
    
    # Increased height from 100 to 250 and added padding
    root.geometry('300x250+50+50')  # width x height + x_position + y_position
    
    # Create label for text with padding and word wrap
    label = tk.Label(root, 
                     text="Your Text Here",
                     font=('Arial', 14),
                     bg='black',
                     fg='white',
                     wraplength=280,  # Wrap text before window edge
                     justify='left',
                     padx=10,
                     pady=10)
    label.pack(expand=True, fill='both')
    
    return root, label

def activate_emulator_window():
    subprocess.run(['xdotool', 'search', '--name', "RetroArch Gambatte v0.5.0-netlink", 'windowactivate'], check=True)
    print("Changed window")

def setup_environment():
    os.makedirs("temp", exist_ok=True)
    time.sleep(0.5)
    print("Slept")

def capture_screen():
    screen_image = ImageGrab.grab()
    screen_image.save("temp/screen.png")
    print("Took print from screen")
    return screen_image

def get_character_section(screen_image):
    bbox = (844, 430, 960, 580)
    character_section = screen_image.crop(bbox)
    character_section.save("temp/char_section.png")
    return cv2.cvtColor(np.array(character_section), cv2.COLOR_RGB2BGR)

def find_best_direction_match(character_section):
    sprite_directions = ['back', 'front', 'left', 'right']
    threshold = 0.1
    best_match = {'direction': None, 'difference': float('inf')}

    for direction in sprite_directions:
        template = cv2.imread(f'assets/character_sprites/{direction}.png')
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_template, 254, 255, cv2.THRESH_BINARY_INV)
        
        result = cv2.matchTemplate(
            character_section,
            template,
            cv2.TM_SQDIFF_NORMED,
            mask=mask
        )
        min_val, _, _, _ = cv2.minMaxLoc(result)
        
        if min_val < best_match['difference']:
            best_match = {'direction': direction, 'difference': min_val}
    
    return best_match, threshold

def get_bottom_section(screen_image):
    bbox = (360, 484, 1574, 1079)
    bottom_section = screen_image.crop(bbox)
    bottom_section.save("temp/bottom_section.png")
    return cv2.cvtColor(np.array(bottom_section), cv2.COLOR_RGB2BGR)

def get_moves_section(screen_image):
    bbox = (614, 678, 1609, 1110)
    moves_section = screen_image.crop(bbox)
    moves_section.save("temp/moves_section.png")
    return cv2.cvtColor(np.array(moves_section), cv2.COLOR_RGB2BGR)

def get_moves_list(moves_section):
    moves_sprites = [f for f in os.listdir('assets/moves')]
    matches = []
    
    for sprite_name in moves_sprites:
        sprite_path = os.path.join('assets/moves', sprite_name)
        template = cv2.imread(sprite_path)
        
        result = cv2.matchTemplate(
            moves_section,
            template,
            cv2.TM_SQDIFF_NORMED
        )
        min_val, _, min_loc, _ = cv2.minMaxLoc(result)
        
        # Store move name without extension and its position
        move_name = os.path.splitext(sprite_name)[0]
        matches.append((move_name, min_val, min_loc[1]))
    
    # Sort by match value to get top 4 matches
    print("\nAll matched moves:")
    for move, score, y_pos in matches:
        print(f"Move: {move:<20} Score: {score:.4f} Y-Position: {y_pos}")
    matches.sort(key=lambda x: x[1])
    top_matches = matches[:4]
    
    # Sort the top 4 by vertical position and return just the move names
    return [move[0] for move in sorted(top_matches, key=lambda x: x[2])]

def get_my_pokemon_section(screen_image):
    bbox = (362, 306, 917, 733)
    my_pokemon_section = screen_image.crop(bbox)
    my_pokemon_section.save("temp/my_pokemon_section.png")
    return cv2.cvtColor(np.array(my_pokemon_section), cv2.COLOR_RGB2BGR)

def get_enemy_pokemon_section(screen_image):
    bbox = (984, 0, 1564, 423)
    enemy_pokemon_section = screen_image.crop(bbox)
    enemy_pokemon_section.save("temp/enemy_pokemon_section.png")
    return cv2.cvtColor(np.array(enemy_pokemon_section), cv2.COLOR_RGB2BGR)

def get_pp_section(screen_image):
    bbox = (406, 529, 970, 750)
    pp_section = screen_image.crop(bbox)
    pp_section.save("temp/pp_section.png")
    return cv2.cvtColor(np.array(pp_section), cv2.COLOR_RGB2BGR)

def get_pp_value(pp_section):
    template = cv2.imread('assets/0_pp.png')
    
    result = cv2.matchTemplate(
        pp_section,
        template,
        cv2.TM_SQDIFF_NORMED
    )
    min_val, _, _, _ = cv2.minMaxLoc(result)
    
    return min_val


def get_my_pokemon_name(my_pokemon_section):
    threshold = 0.1
    best_match = {'pokemon': None, 'difference': float('inf')}
    
    pokemon_sprites = [f for f in os.listdir('assets/pokemon_back_sprites')]
    print(f"Found {len(pokemon_sprites)} pokemon sprites to check")
    
    for sprite_name in pokemon_sprites:
        sprite_path = os.path.join('assets/pokemon_back_sprites', sprite_name)
        template = cv2.imread(sprite_path)
    
        result = cv2.matchTemplate(
            my_pokemon_section,
            template,
            cv2.TM_SQDIFF_NORMED,
        )
        min_val, _, _, _ = cv2.minMaxLoc(result)
        print(f"Checking {sprite_name}: difference = {min_val}")
        
        if min_val < best_match['difference']:
            pokemon_name = os.path.splitext(sprite_name)[0]
            best_match = {'pokemon': pokemon_name, 'difference': min_val}
            print(f"New best match: {pokemon_name} with difference {min_val}")
    
    if best_match['difference'] <= threshold:
        print(f"Found match: {best_match['pokemon']} with difference {best_match['difference']}")
        return best_match['pokemon']
    print("No match found below threshold")
    return None

def get_enemy_pokemon_name(enemy_pokemon_section):
    threshold = 0.1
    best_match = {'pokemon': None, 'difference': float('inf')}
    
    pokemon_sprites = [f for f in os.listdir('assets/pokemon_front_sprites')]
    
    for sprite_name in pokemon_sprites:
        sprite_path = os.path.join('assets/pokemon_front_sprites', sprite_name)
        template = cv2.imread(sprite_path)
    
        result = cv2.matchTemplate(
            enemy_pokemon_section,
            template,
            cv2.TM_SQDIFF_NORMED,
        )
        min_val, _, _, _ = cv2.minMaxLoc(result)
        
        if min_val < best_match['difference']:
            pokemon_name = os.path.splitext(sprite_name)[0]
            best_match = {'pokemon': pokemon_name, 'difference': min_val}
    
    if best_match['difference'] <= threshold:
        return best_match['pokemon']
    return None

def get_selecting_action_value(bottom_section):
    template = cv2.imread("assets/actions.png")
    result = cv2.matchTemplate(
            bottom_section,
            template,
            cv2.TM_SQDIFF_NORMED,
        )
    min_val, _, _, _ = cv2.minMaxLoc(result)
    return min_val

def get_selecting_move_value(bottom_section):
    template = cv2.imread("assets/move_selection.png")
    result = cv2.matchTemplate(
            bottom_section,
            template,
            cv2.TM_SQDIFF_NORMED,
        )
    min_val, _, _, _ = cv2.minMaxLoc(result)
    return min_val

def perform_movement(direction):
    subprocess.run(['xdotool', 'keydown', direction])
    time.sleep(0.1)  # Adjust this delay as needed
    subprocess.run(['xdotool', 'keyup', direction])

def calculate_move_damage(moves, my_pokemon, enemy_pokemon):
    total_damage = {}
    my_pokemon_types = pokemon_types[my_pokemon]
    enemy_pokemon_types = pokemon_types[enemy_pokemon]

    for move_name in moves:
        # Get move data from moves_data dictionary
        move = moves_data[move_name]
        
        # Base damage
        damage = move['damage']
        
        # Same Type Attack Bonus (STAB)
        if move['type'] in my_pokemon_types:
            damage *= 1.5
            
        # Type effectiveness multiplier
        type_multiplier = 1.0
        for enemy_type in enemy_pokemon_types:
            if move['type'] in damage_multiplier and enemy_type in damage_multiplier[move['type']]:
                type_multiplier *= damage_multiplier[move['type']][enemy_type]
                
        total_damage[move_name] = damage * type_multiplier
        
    return total_damage


TYPE_NORMAL = "NORMAL"
TYPE_FIRE = "FIRE"
TYPE_WATER = "WATER"
TYPE_ELECTRIC = "ELECTRIC"
TYPE_GRASS = "GRASS"
TYPE_ICE = "ICE"
TYPE_FIGHTING = "FIGHTING"
TYPE_POISON = "POISON"
TYPE_GROUND = "GROUND"
TYPE_FLYING = "FLYING"
TYPE_PSYCHIC = "PSYCHIC"
TYPE_BUG = "BUG"
TYPE_ROCK = "ROCK"
TYPE_GHOST = "GHOST"
TYPE_DRAGON = "DRAGON"

damage_multiplier = {
    TYPE_NORMAL: {TYPE_ROCK: 0.5, TYPE_GHOST: 0},
    TYPE_FIRE: {TYPE_FIRE: 0.5, TYPE_WATER: 0.5, TYPE_ROCK: 0.5, TYPE_GRASS: 2, TYPE_ICE: 2, TYPE_BUG: 2, TYPE_DRAGON: 0.5},
    TYPE_WATER: {TYPE_FIRE: 2, TYPE_WATER: 0.5, TYPE_GRASS: 0.5, TYPE_GROUND: 2, TYPE_ROCK: 2, TYPE_DRAGON: 0.5},
    TYPE_ELECTRIC: {TYPE_WATER: 2, TYPE_ELECTRIC: 0.5, TYPE_GRASS: 0.5, TYPE_GROUND: 0, TYPE_FLYING: 2, TYPE_DRAGON: 0.5},
    TYPE_GRASS: {TYPE_FIRE: 0.5, TYPE_WATER: 2, TYPE_GRASS: 0.5, TYPE_POISON: 0.5, TYPE_GROUND: 2, TYPE_FLYING: 0.5, TYPE_BUG: 0.5, TYPE_ROCK: 2, TYPE_DRAGON: 0.5},
    TYPE_ICE: {TYPE_WATER: 0.5, TYPE_GRASS: 2, TYPE_ICE: 0.5, TYPE_GROUND: 2, TYPE_FLYING: 2, TYPE_DRAGON: 2},
    TYPE_FIGHTING: {TYPE_NORMAL: 2, TYPE_ICE: 2, TYPE_POISON: 0.5, TYPE_FLYING: 0.5, TYPE_PSYCHIC: 0.5, TYPE_BUG: 0.5, TYPE_ROCK: 2, TYPE_GHOST: 0},
    TYPE_POISON: {TYPE_GRASS: 2, TYPE_POISON: 0.5, TYPE_GROUND: 0.5, TYPE_BUG: 2, TYPE_ROCK: 0.5, TYPE_GHOST: 0.5},
    TYPE_GROUND: {TYPE_FIRE: 2, TYPE_ELECTRIC: 2, TYPE_GRASS: 0.5, TYPE_POISON: 2, TYPE_FLYING: 0, TYPE_BUG: 0.5, TYPE_ROCK: 2},
    TYPE_FLYING: {TYPE_ELECTRIC: 0.5, TYPE_GRASS: 2, TYPE_FIGHTING: 2, TYPE_BUG: 2, TYPE_ROCK: 0.5},
    TYPE_PSYCHIC: {TYPE_FIGHTING: 2, TYPE_POISON: 2, TYPE_PSYCHIC: 0.5},
    TYPE_BUG: {TYPE_FIRE: 0.5, TYPE_GRASS: 2, TYPE_FIGHTING: 0.5, TYPE_POISON: 2, TYPE_FLYING: 0.5, TYPE_PSYCHIC: 2, TYPE_GHOST: 0.5},
    TYPE_ROCK: {TYPE_FIRE: 2, TYPE_ICE: 2, TYPE_FIGHTING: 0.5, TYPE_GROUND: 0.5, TYPE_FLYING: 2, TYPE_BUG: 2},
    TYPE_GHOST: {TYPE_NORMAL: 0, TYPE_PSYCHIC: 0, TYPE_GHOST: 2},
    TYPE_DRAGON: {TYPE_DRAGON: 2}
}

pokemon_types = {
    "dragonite": [TYPE_DRAGON, TYPE_FLYING],
    "dugtrio": [TYPE_GROUND],
    "fearow": [TYPE_NORMAL, TYPE_FLYING], 
    "snorlax": [TYPE_NORMAL],
    "zapdos": [TYPE_ELECTRIC, TYPE_FLYING],
    "arbok": [TYPE_POISON],
    "ditto": [TYPE_NORMAL],
    "dodrio": [TYPE_NORMAL, TYPE_FLYING],
    "golbat": [TYPE_POISON, TYPE_FLYING],
    "hypno": [TYPE_PSYCHIC],
    "kadabra": [TYPE_PSYCHIC],
    "magneton": [TYPE_ELECTRIC],
    "parasect": [TYPE_BUG, TYPE_GRASS],
    "raichu": [TYPE_ELECTRIC],
    "venomoth": [TYPE_BUG, TYPE_POISON],
}

moves_data = {
    "agility": {"damage": 0, "type": TYPE_PSYCHIC},
    "body_slam": {"damage": 85, "type": TYPE_NORMAL},
    "dig": {"damage": 80, "type": TYPE_GROUND},
    "drill_peck": {"damage": 80, "type": TYPE_FLYING},
    "earthquake": {"damage": 100, "type": TYPE_GROUND},
    "fly": {"damage": 90, "type": TYPE_FLYING},
    "fury_attack": {"damage": 54, "type": TYPE_NORMAL},
    "hyper_beam": {"damage": 150, "type": TYPE_NORMAL},
    "leer": {"damage": 0, "type": TYPE_NORMAL},
    "rest": {"damage": 0, "type": TYPE_PSYCHIC},
    "sand-attack": {"damage": 0, "type": TYPE_GROUND},
    "slash": {"damage": 140, "type": TYPE_NORMAL},
    "strength": {"damage": 80, "type": TYPE_NORMAL},
    "surf": {"damage": 90, "type": TYPE_WATER},
    "thunder": {"damage": 110, "type": TYPE_ELECTRIC},
    "thundershock": {"damage": 40, "type": TYPE_ELECTRIC},
    "thunder_wave": {"damage": 0, "type": TYPE_ELECTRIC},
    "wrap": {"damage": 15, "type": TYPE_NORMAL}
}

def main():

    overlay_window, overlay_label = create_overlay_window()
    activate_emulator_window()
    setup_environment()
    
    current_pos = 0
    movement_pattern = ['r','d','l','u']
    direction_map = {
        'r': 'Right',
        'd': 'Down',
        'l': 'Left',
        'u': 'Up'
    }

    my_pokemon = None
    enemy_pokemon = None
    moves = []
    moves_damage = {}
    move_selected = 0

    while True:
        print(my_pokemon)
        print(enemy_pokemon)

        screen_image = capture_screen()

        character_section = get_character_section(screen_image)
        best_match, threshold = find_best_direction_match(character_section)
        
        if best_match['difference'] <= threshold:
            overlay_label.config(text=f"Seaching for pokemons to battle")
            overlay_window.update()

            # Reset all battle-related variables when character is detected (battle is over)
            my_pokemon = None
            enemy_pokemon = None
            moves = []
            moves_damage = {}
            move_selected = 0

            print(f"Character detected facing {best_match['direction']}! Difference:", best_match['difference'])
            current_movement = movement_pattern[current_pos]
            perform_movement(direction_map[current_movement])
            current_pos = (current_pos + 1) % len(movement_pattern)
            continue

        bottom_section = get_bottom_section(screen_image)
        action_val = get_selecting_action_value(bottom_section)

        if action_val <= threshold and my_pokemon == None and enemy_pokemon == None:
            print("Procurando")
            my_pokemon_section = get_my_pokemon_section(screen_image)
            my_pokemon = get_my_pokemon_name(my_pokemon_section)
            my_pokemon_types = pokemon_types[my_pokemon]
            enemy_pokemon_section = get_enemy_pokemon_section(screen_image)
            enemy_pokemon = get_enemy_pokemon_name(enemy_pokemon_section)
            enemy_pokemon_types = pokemon_types[enemy_pokemon]

            if my_pokemon and enemy_pokemon:
                overlay_label.config(text=f"My Pokemon: {my_pokemon} ({', '.join(my_pokemon_types)})\nEnemy: {enemy_pokemon} ({', '.join(enemy_pokemon_types)})")
                overlay_window.update()

            continue

        if action_val <= threshold:
            subprocess.run(['xdotool', 'keydown', 'x'])
            time.sleep(0.1)
            subprocess.run(['xdotool', 'keyup', 'x'])
            continue

        move_selection_val = get_selecting_move_value(bottom_section)
        print(move_selection_val)

        if move_selection_val <= 0.03 and not moves:
            moves_section = get_moves_section(screen_image)
            moves = get_moves_list(moves_section)
            moves_damage = calculate_move_damage(moves, my_pokemon, enemy_pokemon)
            if moves:
                # Find move with highest damage
                max_damage = -float('inf')
                move_selected = 0
                for i, move in enumerate(moves):
                    if moves_damage[move] > max_damage:
                        max_damage = moves_damage[move]
                        move_selected = i
                
                # Press down arrow move_selected times
                for _ in range(move_selected):
                    subprocess.run(['xdotool', 'keydown', 'Down'])
                    time.sleep(0.1)
                    subprocess.run(['xdotool', 'keyup', 'Down'])
                
                moves_text = "\n".join([f"{move}: {moves_damage[move]:.1f} damage" for move in moves])
                overlay_label.config(text=f"My Pokemon: {my_pokemon} ({', '.join(my_pokemon_types)})\nEnemy: {enemy_pokemon} ({', '.join(enemy_pokemon_types)})\nMoves:\n{moves_text}")
                overlay_window.update()
            continue

        if move_selection_val <= 0.03:
            pp_section = get_pp_section(screen_image)
            is_0_pp_value = get_pp_value(pp_section)
            if is_0_pp_value <= threshold:
                moves_damage[moves[move_selected]] = -1
                # Find new move with highest damage
                max_damage = -float('inf')
                new_move = 0
                for i, move in enumerate(moves):
                    if moves_damage[move] > max_damage:
                        max_damage = moves_damage[move]
                        new_move = i
                
                # Calculate number of presses needed
                moves_difference = new_move - move_selected
                key = 'Down' if moves_difference > 0 else 'Up'
                
                # Press key the required number of times
                for _ in range(abs(moves_difference)):
                    subprocess.run(['xdotool', 'keydown', key])
                    time.sleep(0.1)
                    subprocess.run(['xdotool', 'keyup', key])
                
                # Update selected move
                move_selected = new_move

            else:
                subprocess.run(['xdotool', 'keydown', 'x'])
                time.sleep(0.1)
                subprocess.run(['xdotool', 'keyup', 'x'])



        print("Character not detected. Best match was", best_match['direction'], 
                "with difference:", best_match['difference'])
        subprocess.run(['xdotool', 'keydown', 'z'])
        time.sleep(0.1)
        subprocess.run(['xdotool', 'keyup', 'z'])

if __name__ == "__main__":
    main()