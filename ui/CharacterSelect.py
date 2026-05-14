# ui/CharacterSelect.py
import pygame
import sys
from vision.HandCursor import HandCursor


def character_select(screen):
    imagen = pygame.image.load("Image\\SeleccionPersonaje.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

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
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                px, py = pygame.mouse.get_pos()
                if 219 < px < 450 and 330 < py < 568:
                    result = 'knight'
                    running = False
                elif 829 < px < 1061 and 331 < py < 567:
                    result = 'rogue'
                    running = False

        pos = cursor.get_position(W, H)
        if pos and cursor.consume_click():
            px, py = pos
            if 219 < px < 450 and 330 < py < 568:
                result = 'knight'
                running = False
            elif 829 < px < 1061 and 331 < py < 567:
                result = 'rogue'
                running = False

        screen.blit(imagen, (0, 0))
        cursor.draw_on(screen, W, H)
        cursor.show_camera()
        pygame.display.flip()

    cursor.release()
    return result