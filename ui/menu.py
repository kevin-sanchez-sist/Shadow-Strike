import pygame
import sys


def menu(screen):
    imagen = pygame.image.load("Image\\Menu.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

    # Música de ambiente del menú (loop infinito)
    pygame.mixer.music.load("sounds/menu_musica.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1 = loop infinito

    running = True
    while running:
        screen.blit(imagen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

                # Boton Jugar
                if 402 < pos[0] < 880 and 382 < pos[1] < 451:
                    return 'character_select'

                # Boton Ayuda
                if 418 < pos[0] < 866 and 395 < pos[1] < 468:
                    return 'ayuda'

                # Boton Salir
                if 400 < pos[0] < 870 and 560 < pos[1] < 615:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
