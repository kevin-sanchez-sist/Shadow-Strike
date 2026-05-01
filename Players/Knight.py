from Players.Fighter import Fighter

KNIGHT_STATS = {
    'max_hp': 150,
    'speed': 4,
    'defense': 3,
    'attacks': [
        {
            'name': 'Attack',
            'action': 'attack',
            'damage': 15,
            'range': 80,
            'cooldown': 500,
        },
        {
            'name': 'Attack_Extra',
            'action': 'attack_extra',
            'damage': 30,
            'range': 100,
            'cooldown': 1200,
        },
        {
            'name': 'Push',
            'action': 'push',
            'damage': 5,
            'range': 60,
            'cooldown': 800,
        },
    ]
}

KNIGHT_ACTIONS = ['idle', 'run', 'jump', 'attack', 'attack_extra', 'push', 'hurt', 'death']

class Knight(Fighter):
    def __init__(self, x: int, y: int, sprites: dict, facing: str = 'right'):
        super().__init__(
            name='Knight',
            x=x,
            y=y,
            sprites=sprites,
            stats=KNIGHT_STATS,
            facing=facing
        )
    
    def _on_animation_end(self):
        frames = self.sprites[self.action]

        if self.action == 'death':
            self.frame_index = len(frames) - 1
            self.is_alive = False

        elif self.action in ('attack', 'attack_extra', 'push', 'hurt'):
            self.is_attacking = False
            self.is_hurt = False
            self.set_action('idle')

        else:  # idle, run, jump → loop
            self.frame_index = 0