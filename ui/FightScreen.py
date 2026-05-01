# ui/fight_screen.py
import pygame
from utils.sprite_loader import load_all_actions
from Players.Knight import Knight, KNIGHT_ACTIONS

def fight_screen(screen, personaje):
    fondo = pygame.image.load("Image\ElTemplo.png")
    fondo = pygame.transform.scale(fondo, screen.get_size())

    sprites = load_all_actions("Sprites", "Knight", KNIGHT_ACTIONS, scale=2.5)
    knight = Knight(x=100, y=300, sprites=sprites)

    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Salto
                if event.key == pygame.K_SPACE and knight.on_ground:
                    knight.vel_y = -12
                    knight.on_ground = False
                    knight.set_action('jump')

                # Ataque básico
                if event.key == pygame.K_p:
                    knight.attack(attack_index=0)  # 'attack'

                # Ataque especial
                if event.key == pygame.K_x:
                    knight.attack(attack_index=1)  # 'attack_extra'

                # Push
                if event.key == pygame.K_e:
                    knight.attack(attack_index=2)

        # Movimiento continuo con teclas sostenidas
        keys = pygame.key.get_pressed()

        if not knight.is_attacking and not knight.is_hurt:
            if keys[pygame.K_d]:  # mover derecha
                knight.vel_x = knight.speed
                knight.facing = 'right'
                if knight.on_ground:
                    knight.set_action('run')

            elif keys[pygame.K_a]:  # mover izquierda
                knight.vel_x = -knight.speed
                knight.facing = 'left'
                if knight.on_ground:
                    knight.set_action('run')

            else:
                knight.vel_x = 0
                if knight.on_ground and knight.action == 'run':
                    knight.set_action('idle')

        knight.update(delta_time)
        screen.blit(fondo, (0, 0))
        knight.draw(screen)
        pygame.display.flip()