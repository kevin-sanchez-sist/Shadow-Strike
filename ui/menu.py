import pygame

def menu(screen):
    imagen = pygame.image.load("Image\Menu.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())
    #ambiente = pygame.mixer.Sound("assets/sonidos/ambiente.mp3")

    running = True
    while running:
        #ambiente.play()
        screen.blit(imagen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

                # Boton Jugar
                if 402 < pos[0] < 880 and 382 < pos[1] < 451:
                    #ambiente.stop()
                    return 'character_select'

                # Boton Ayuda
                if 418 < pos[0] < 866 and 395 < pos[1] < 468:
                    #ambiente.stop()
                    return 'ayuda'

                # Boton Salir
                if 418 < pos[0] < 866 and 510 < pos[1] < 568:
                    pygame.quit()

        pygame.display.flip()