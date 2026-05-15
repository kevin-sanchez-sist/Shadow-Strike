from Players.Fighter import Fighter
from Players.Projectile import Projectile, PROJECTILE_SPEED_NORMAL, PROJECTILE_SPEED_EXTRA

MAGE_STATS = {
    'max_hp': 320,           # frágil
    'speed':  8,
    'defense': 0,
    'attacks': [
        {
            'name':     'Attack',
            'action':   'attack',
            'damage':   10,
            'range':    1280,  
            'cooldown': 700,
        },
        {
            'name':     'Attack_Extra',
            'action':   'attack_extra',
            'damage':   24,
            'range':    1280,
            'cooldown': 1400,
        },
    ]
}

MAGE_ACTIONS = ['idle', 'run', 'jump', 'attack', 'attack_extra', 'hurt', 'death']

MAGE_FOLDER_MAP = {
    'idle':         'Idle',
    'run':          'Run',
    'jump':         'Jump',
    'attack':       'Attack',
    'attack_extra': 'Attack_Extra',
    'hurt':         'Hurt',
    'death':        'Death',
}


class Mage(Fighter):
    def __init__(self, x, y, sprites, fire_frames, fire_extra_frames,
                 facing='right', sounds=None):
        super().__init__(
            name='Mage',
            x=x, y=y,
            sprites=sprites,
            stats=MAGE_STATS,
            facing=facing,
            sounds=sounds,
        )
        self.fire_frames       = fire_frames        # frames animación Fire
        self.fire_extra_frames = fire_extra_frames  # frames animación Fire_Extra
        self.projectiles       = []                 # proyectiles activos
        self._spawn_projectile = False              # flag interno

    def attack(self, attack_index: int = 0):
        result = super().attack(attack_index)
        if result:
            self._spawn_projectile = True
            self._pending_attack_index = attack_index
        return result

    def _on_animation_end(self):
        frames = self.sprites[self.action]

        if self.action == 'death':
            self.frame_index = len(frames) - 1
            self.is_alive = False

        elif self.action in ('attack', 'attack_extra', 'hurt'):
            # Lanzar proyectil al terminar la animación de ataque
            if self._spawn_projectile:
                self._launch_projectile()
                self._spawn_projectile = False
            self.is_attacking = False
            self.is_hurt = False
            self.set_action('idle')

        else:
            self.frame_index = 0

    def _launch_projectile(self):
        direction = 1 if self.facing == 'right' else -1
        # Offset para que salga desde la mano del mago
        px = self.rect.centerx + (40 * direction)
        py = self.rect.centery - 10

        if self._pending_attack_index == 0:
            proj = Projectile(
                x=px, y=py,
                direction=direction,
                frames=self.fire_frames,
                damage=self.attacks[0]['damage'],
                speed=PROJECTILE_SPEED_NORMAL,
            )
        else:
            proj = Projectile(
                x=px, y=py,
                direction=direction,
                frames=self.fire_extra_frames,
                damage=self.attacks[1]['damage'],
                speed=PROJECTILE_SPEED_EXTRA,
            )
        self.projectiles.append(proj)

    def update(self, delta_time: int):
        super().update(delta_time)
        # Actualizar proyectiles y limpiar los inactivos
        for p in self.projectiles:
            p.update(delta_time)
        self.projectiles = [p for p in self.projectiles if p.active]

    def draw(self, screen):
        super().draw(screen)
        for p in self.projectiles:
            p.draw(screen)