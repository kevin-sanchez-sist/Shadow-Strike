import pygame

def loading_screen(screen):
    imagen = pygame.image.load("Image\Inicio.png")
    imagen = pygame.transform.scale(imagen, screen.get_size())
    screen.blit(imagen, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)