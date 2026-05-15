# main.py
import pygame
from ui.LoadingScreen import loading_screen
from ui.menu import menu
from ui.CharacterSelect import character_select
from ui.MapSelect import map_select
from ui.FightScreen import fight_screen

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Shadow Strike")

loading_screen(screen)

while True:
    opcion = menu(screen)

    if opcion == 'character_select':
        personaje = character_select(screen)

        if personaje is None:
            continue  # usuario cerró la ventana

        # ── Selección de mapa ────────────────────────────────────────────
        mapa = map_select(screen)

        if mapa is None:
            continue  # usuario cerró la ventana o presionó ESC

        # ── Combate ──────────────────────────────────────────────────────
        fight_screen(screen, personaje, mapa)
