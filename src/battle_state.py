from game_data import pokemon_data, moves_data, damage_multiplier

class BattleState:
    """
    Classe que representa o estado de uma batalha Pokémon.
    
    Mantém informações sobre os Pokémon em batalha, seus tipos, movimentos disponíveis
    e calcula danos considerando vantagens/desvantagens de tipo.
    """

    def __init__(self):
        """
        Inicializa um novo estado de batalha com valores vazios.
        """
        self.my_pokemon_name: str = None
        self.my_pokemon_types: list = None
        self.enemy_pokemon_name: str = None 
        self.enemy_pokemon_types: list = None
        self.moves: list = None
        self.move_selected: int = 0

    def get_pokemon_types(self) -> None:
        """
        Obtém os tipos dos Pokémon em batalha a partir do conjunto de dados.
        """
        self.my_pokemon_types = pokemon_data[self.my_pokemon_name]
        self.enemy_pokemon_types = pokemon_data[self.enemy_pokemon_name]

    def update_moves_damage(self) -> None:
        """
        Atualiza o dano de cada movimento considerando:
        - Dano base do movimento
        - Bônus STAB (Same Type Attack Bonus) de 1.5x se o tipo do movimento corresponder ao tipo do Pokémon
        - Multiplicadores de tipo contra o Pokémon inimigo
        """
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
        """
        Calcula quantos movimentos são necessários para selecionar o ataque com maior dano.
        
        Returns:
            int: Número de vezes que é necessário mover o cursor para chegar no melhor movimento
        """
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
        """
        Gera uma representação em string do estado atual da batalha.
        
        Returns:
            str: String formatada contendo informações sobre os Pokémon e seus movimentos
        """
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