# ui/InstructionScreen.py
import pygame
import sys
from vision.HandCursor import HandCursor


def instruction_screen(screen):
    """
    Muestra la pantalla de instrucciones.
    Se cierra con pinch o presionando ESC, y vuelve al menú.
    """
    imagen = pygame.image.load("Image/Instrucciones.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

    cursor = HandCursor()
    clock  = pygame.time.Clock()
    W, H   = screen.get_size()

    running = True
    while running:
        delta_time = clock.tick(60)
        cursor.update(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cursor.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if cursor.consume_click():
            running = False

        screen.blit(imagen, (0, 0))
        cursor.draw_on(screen, W, H)
        cursor.show_camera()
        pygame.display.flip()

    cursor.release()