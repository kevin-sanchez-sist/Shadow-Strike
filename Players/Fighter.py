import pygame

GRAVITY = 0.5
GROUND_Y = 300  # Se debe ajustar de acuerdo al escenario

class Fighter:
    def __init__(self, name: str, x: int, y: int, sprites: dict, stats: dict, facing: str = 'right'):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.facing = facing  # 'right' o 'left'

        # --- Stats ---
        self.max_hp   = stats['max_hp']
        self.hp       = stats['max_hp']
        self.speed    = stats['speed']
        self.defense  = stats['defense']
        self.attacks  = stats['attacks']  # lista de dicts con info de cada ataque

        # --- Sprites y animación ---
        self.sprites      = sprites        # { 'idle': [surf, ...], 'walk': [...], ... }
        self.action       = 'idle'
        self.frame_index  = 0
        self.frame_timer  = 0
        self.frame_duration = 150          # ms por frame, ajustable por acción

        # --- Física ---
        self.vel_x    = 0.0
        self.vel_y    = 0.0
        self.on_ground = True

        # --- Estado ---
        self.is_alive       = True
        self.is_attacking   = False
        self.is_hurt        = False
        self.cooldown_timer = 0

        # --- Rect de colisión (se actualiza cada frame) ---
        first_frame = sprites['idle'][0]
        self.rect = first_frame.get_rect(topleft=(x, y))

    # ─────────────────────────────────────────
    #  ANIMACIÓN
    # ─────────────────────────────────────────

    def set_action(self, new_action: str):
        """Cambia la acción actual y reinicia la animación si es diferente."""
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.frame_timer = 0

    def update_animation(self, delta_time: int):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            frames = self.sprites[self.action]

            if self.frame_index >= len(frames):
                self._on_animation_end()
    
    def _on_animation_end(self):
        """Cada personaje define qué hacer al terminar una animación."""
        self.frame_index = 0  # comportamiento por defecto: loop

    # ─────────────────────────────────────────
    #  FÍSICA
    # ─────────────────────────────────────────

    def apply_gravity(self):
        if not self.on_ground:
            self.vel_y += GRAVITY

    def apply_movement(self):
        self.x += self.vel_x
        self.y += self.vel_y

         # Límites horizontales
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        if self.x > 1280 - self.rect.width:
            self.x = 1280 - self.rect.width
            self.vel_x = 0

        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

        self.rect.topleft = (int(self.x), int(self.y))

    # ─────────────────────────────────────────
    #  COMBATE
    # ─────────────────────────────────────────

    def take_damage(self, amount: int):
        if not self.is_alive:
            return
        reduced = max(0, amount - self.defense)
        self.hp = max(0, self.hp - reduced)
        self.is_hurt = True
        self.set_action('hurt')
        if self.hp == 0:
            self.set_action('death')

    def attack(self, attack_index: int = 0) -> dict | None:
        """
        Intenta ejecutar un ataque.
        Retorna el dict del ataque si es válido, None si está en cooldown.
        """
        if self.cooldown_timer > 0 or self.is_hurt or not self.is_alive:
            return None
        attack_data = self.attacks[attack_index]
        self.is_attacking = True
        self.cooldown_timer = attack_data['cooldown']
        self.set_action(attack_data['action'])
        return attack_data

    def update_cooldown(self, delta_time: int):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

    # ─────────────────────────────────────────
    #  UPDATE GENERAL
    # ─────────────────────────────────────────

    def update(self, delta_time: int):
        self.apply_gravity()
        self.apply_movement()
        self.update_cooldown(delta_time)
        self.update_animation(delta_time)

    # ─────────────────────────────────────────
    #  RENDER
    # ─────────────────────────────────────────

    def draw(self, screen: pygame.Surface):
        frame = self.sprites[self.action][self.frame_index]

        if self.facing == 'left':
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.rect.topleft)