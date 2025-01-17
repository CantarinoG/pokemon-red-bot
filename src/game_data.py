"""
Módulo que contém dados estáticos sobre tipos de Pokémon, multiplicadores de dano,
informações de Pokémon e seus movimentos.

Este módulo define constantes e dicionários que são usados para calcular danos
e determinar efetividade de ataques em batalhas Pokémon.
"""

# Constantes para os tipos de Pokémon
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

# Dicionário com multiplicadores de dano entre tipos
# A chave externa é o tipo do ataque e a interna é o tipo do Pokémon que recebe o ataque
# Os valores representam o multiplicador de dano (2 para super efetivo, 0.5 para não muito efetivo, 0 para sem efeito)
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

# Dicionário com dados dos Pokémon
# A chave é o nome do Pokémon e o valor é uma lista com seus tipos
pokemon_data = {
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

# Dicionário com dados dos movimentos
# A chave é o nome do movimento e o valor é um dicionário com seu dano base e tipo
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