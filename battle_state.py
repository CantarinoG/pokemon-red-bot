class BattleState:
    def __init__(self):
        self.my_pokemon: str = None
        self.enemy_pokemon: str = None 
        self.moves: list = None
        self.move_selected: int = 0

class Move:
    def __init__(self):
        self.name: str = None
        self.damage: float = None