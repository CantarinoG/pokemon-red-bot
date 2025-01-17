from game_data import pokemon_data, moves_data, damage_multiplier

class BattleState:
    def __init__(self):
        self.my_pokemon_name: str = None
        self.my_pokemon_types: list = None
        self.enemy_pokemon_name: str = None 
        self.enemy_pokemon_types: list = None
        self.moves: list = None
        self.move_selected: int = 0

    def get_pokemon_types(self) -> None:
        self.my_pokemon_types = pokemon_data[self.my_pokemon_name]
        self.enemy_pokemon_types = pokemon_data[self.enemy_pokemon_name]

    def update_moves_damage(self) -> None:
        for move in self.moves:
            move_data = moves_data[move["name"]]
            damage = move_data["damage"]
            if move_data["type"] in self.my_pokemon_types:
                damage *= 1.5
            type_multiplier = 1.0
            for enemy_type in self.enemy_pokemon_types:
                if move_data["type"] in damage_multiplier and enemy_type in damage_multiplier[move_data["type"]]:
                    type_multiplier *= damage_multiplier[move_data["type"]][enemy_type]
            move["damage"] = damage * type_multiplier

    def get_movements_to_highest_damage(self) -> None:
        max_damage = -float('inf')
        best_move_index = 0
        for i, move in enumerate(self.moves):
            if move["damage"] > max_damage:
                max_damage = move["damage"]
                best_move_index = i
        if best_move_index >= self.move_selected:
            moves_needed = best_move_index - self.move_selected
        else:
            moves_needed = len(self.moves) - self.move_selected + best_move_index
        self.move_selected = best_move_index
        return moves_needed

    def to_string(self) -> str:
        string = (
            f"BATTLE STATE\n\n"
            f"{self.my_pokemon_name} ({', '.join(self.my_pokemon_types) if self.my_pokemon_types else 'None'})\n"
            f"{self.enemy_pokemon_name} ({', '.join(self.enemy_pokemon_types) if self.enemy_pokemon_types else 'None'})"
        )
        if self.moves:
            string += (
                f"\n\nMOVES:\n"
                + "\n".join([f"{i+1}. {move['name']} (Damage {int(move['damage'])})" for i, move in enumerate(self.moves)])
            )
        return string