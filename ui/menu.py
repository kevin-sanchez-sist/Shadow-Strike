# ui/menu.py
import pygame
import sys
from vision.HandCursor import HandCursor
from ui.InstructionScreen import instruction_screen


def menu(screen):
    imagen = pygame.image.load("Image\\Menu.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

    pygame.mixer.music.load("sounds/menu_musica.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    cursor = HandCursor()
    clock  = pygame.time.Clock()
    W, H   = screen.get_size()
    result = None
    running = True

    while running:
        delta_time = clock.tick(60)
        cursor.update(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cursor.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        pos = cursor.get_position(W, H)
        if pos and cursor.consume_click():
            px, py = pos
            if 402 < px < 880 and 382 < py < 451:
                result = 'character_select'
                running = False
            elif 400 < px < 870 and 560 < py < 615:
                cursor.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif 418 < px < 866 and 460 < py < 555:
                cursor.release()
                instruction_screen(screen)
                return menu(screen)   # vuelve al menú después de cerrar instrucciones

        screen.blit(imagen, (0, 0))
        cursor.draw_on(screen, W, H)
        cursor.show_camera()
        pygame.display.flip()

    cursor.release()
    return result