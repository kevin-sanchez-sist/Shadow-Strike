import pygame
import sys


def result_screen(screen, won: bool):
    """
    won=True  → imagen de victoria
    won=False → imagen de derrota
    Espera 4 segundos y vuelve al menú.
    """
    path = "Image/Victoria.png" if won else "Image/Derrota.png"
    imagen = pygame.image.load(path)
    imagen = pygame.transform.scale(imagen, screen.get_size())

    pygame.mixer.music.stop()

    start = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(imagen, (0, 0))
        pygame.display.flip()

        if pygame.time.get_ticks() - start >= 4000:
            return