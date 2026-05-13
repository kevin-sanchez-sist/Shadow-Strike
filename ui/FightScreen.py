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
    knight = Knight(x=100, y=450, sprites=sprites)

    tracker = PoseTracker()
    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60)
        frame = tracker.update()
        tracker.show_camera_window(frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tracker.release()
                pygame.quit()

        keys = pygame.key.get_pressed()
        action   = tracker.get_action()
        movement = tracker.get_movement()

        if not knight.is_attacking and not knight.is_hurt:
            # Movimiento: teclado o mediapipe
            if movement == 'right':
                knight.vel_x = knight.speed
                knight.facing = 'right'
                if knight.on_ground:
                    knight.set_action('run')

            elif movement == 'left':
                knight.vel_x = -knight.speed
                knight.facing = 'left'
                if knight.on_ground:
                    knight.set_action('run')

            elif movement == 'jump' and knight.on_ground:
                knight.vel_y = -40
                knight.on_ground = False
                knight.set_action('jump')

            else:
                knight.vel_x = 0
                if knight.on_ground:
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