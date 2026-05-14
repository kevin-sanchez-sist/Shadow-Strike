import pygame
import sys


def character_select(screen):
    imagen = pygame.image.load("Image\SeleccionPersonaje.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

    running = True
    while running:
        screen.blit(imagen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)  # para identificar coordenadas de cada personaje

                # Boton Knight
                if 219 < pos[0] < 450 and 330 < pos[1] < 568:
                    return 'knight'

                # Boton Rogue
                # TODO: ajustar coordenadas corriendo el juego y viendo el print(pos)
                if 829 < pos[0] < 1061 and 331 < pos[1] < 567:
                    return 'rogue'

        pygame.display.flip()
