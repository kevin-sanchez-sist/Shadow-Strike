# ui/FightScreen.py
import pygame
from utils.sprite_loader import load_all_actions
from Players.Knight import Knight, KNIGHT_ACTIONS
from vision.PoseTracker import PoseTracker
import cv2

def fight_screen(screen, personaje):
    fondo = pygame.image.load("Image\ElTemplo.png")
    fondo = pygame.transform.scale(fondo, screen.get_size())

    sprites = load_all_actions("Sprites", "Knight", KNIGHT_ACTIONS, scale=2.5)
    knight = Knight(x=100, y=300, sprites=sprites)

    tracker = PoseTracker()
    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60)
        tracker.update()
        # al inicio del while, después de tracker.update()
        frame = tracker.update()
        if frame is not None:
            frame = tracker.draw_landmarks(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 180))  # tamaño pequeño en esquina
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (10, 10))  # esquina superior izquierda

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tracker.release()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Salto
                if event.key == pygame.K_SPACE and knight.on_ground:
                    knight.vel_y = -12
                    knight.on_ground = False
                    knight.set_action('jump')

                # Ataque básico
                if event.key == pygame.K_p:
                    knight.attack(attack_index=0)

                # Ataque especial
                if event.key == pygame.K_x:
                    knight.attack(attack_index=1)

                # Push
                if event.key == pygame.K_e:
                    knight.attack(attack_index=2)

        keys = pygame.key.get_pressed()
        action   = tracker.get_action()
        movement = tracker.get_movement()

        if not knight.is_attacking and not knight.is_hurt:
            # Movimiento: teclado o mediapipe
            if keys[pygame.K_d] or movement == 'right':
                knight.vel_x = knight.speed
                knight.facing = 'right'
                if knight.on_ground:
                    knight.set_action('run')

            elif keys[pygame.K_a] or movement == 'left':
                knight.vel_x = -knight.speed
                knight.facing = 'left'
                if knight.on_ground:
                    knight.set_action('run')

            elif movement == 'jump' and knight.on_ground:
                knight.vel_y = -12
                knight.on_ground = False
                knight.set_action('jump')

            else:
                knight.vel_x = 0
                if knight.on_ground and knight.action == 'run':
                    knight.set_action('idle')

            # Ataques mediapipe
            if action == 'attack':
                knight.attack(attack_index=0)
            elif action == 'special':
                knight.attack(attack_index=1)

        knight.update(delta_time)
        screen.blit(fondo, (0, 0))
        knight.draw(screen)
        pygame.display.flip()

    tracker.release()