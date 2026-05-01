import pygame

def character_select(screen):
    imagen = pygame.image.load("Image\SeleccionPersonaje.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())

    running = True
    while running:
        screen.blit(imagen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)  # para identificar coordenadas de cada personaje

                # Boton Knight
                if 219 < pos[0] < 450 and 330 < pos[1] < 568:
                    return 'knight'

        pygame.display.flip()