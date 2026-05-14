from Players.Fighter import Fighter

ROGUE_STATS = {
    'max_hp': 110,          # más frágil que el Knight
    'speed': 14,            # más rápido
    'defense': 1,
    'attacks': [
        {
            'name': 'Attack',
            'action': 'attack',
            'damage': 12,
            'range': 70,
            'cooldown': 400,    # más rápido que el Knight
        },
        {
            'name': 'Attack_Extra',
            'action': 'attack_extra',
            'damage': 28,
            'range': 90,
            'cooldown': 1000,
        },
    ]
}

# Acciones implementadas (Climb, Push, Walk, Run_Attack, Walk_Attack excluidas por ahora)
ROGUE_ACTIONS = ['idle', 'run', 'jump', 'high_jump', 'attack', 'attack_extra', 'hurt', 'death']

# Mapeo: nombre de acción interno → nombre de carpeta real en Sprites/Rogue/
ROGUE_FOLDER_MAP = {
    'idle':         'Idle',
    'run':          'Run',
    'jump':         'Jump',
    'high_jump':    'High_Jump',
    'attack':       'Attack',
    'attack_extra': 'Attack_Extra',
    'hurt':         'Hurt',
    'death':        'Death',
}


class Rogue(Fighter):
    def __init__(self, x: int, y: int, sprites: dict, facing: str = 'right', sounds: dict = None):
        super().__init__(
            name='Rogue',
            x=x,
            y=y,
            sprites=sprites,
            stats=ROGUE_STATS,
            facing=facing,
            sounds=sounds,
        )
        # El Rogue tiene tiempos de frame más rápidos en general
        self.frame_durations.update({
            'idle':         110,
            'run':          70,
            'jump':         80,
            'high_jump':    75,
            'attack':       65,
            'attack_extra': 90,
            'hurt':         18,
            'death':        55,
        })

    def _on_animation_end(self):
        frames = self.sprites[self.action]

        if self.action == 'death':
            self.frame_index = len(frames) - 1
            self.is_alive = False

        elif self.action in ('attack', 'attack_extra', 'hurt'):
            self.is_attacking = False
            self.is_hurt = False
            self.set_action('idle')

        else:   # idle, run, jump, high_jump → loop
            self.frame_index = 0
