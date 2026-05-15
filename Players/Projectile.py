import pygame

PROJECTILE_SPEED_NORMAL = 30
PROJECTILE_SPEED_EXTRA  = 25


class Projectile:
    """
    Proyectil animado lanzado por el Mago.
    Se mueve en línea recta y desaparece al colisionar o salir de pantalla.
    """

    def __init__(self, x: int, y: int, direction: int,
                 frames: list, damage: int, speed: int):
        """
        direction : 1 = derecha, -1 = izquierda
        frames    : lista de pygame.Surface con la animación del fuego
        """
        self.x         = float(x)
        self.y         = float(y)
        self.direction = direction
        self.frames    = frames
        self.damage    = damage
        self.speed     = speed

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = 80   # ms por frame

        self.active = True   # False = debe eliminarse

        first = frames[0]
        self.rect = first.get_rect(topleft=(x, y))

    def update(self, delta_time: int):
        # Movimiento
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)

        # Animación en loop
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        # Salió de pantalla
        if self.x < -100 or self.x > 1400:
            self.active = False

    def draw(self, screen: pygame.Surface):
        frame = self.frames[self.frame_index]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, self.rect.topleft)