import pygame

BAR_W      = 400
BAR_H      = 28
BAR_Y      = 20
MARGIN     = 40

COLOR_BG        = (40, 40, 40)
COLOR_BORDER    = (200, 200, 200)
COLOR_PLAYER    = (50, 120, 255)   # azul
COLOR_ENEMY     = (220, 50, 50)    # rojo
COLOR_NAME      = (255, 255, 255)


def _load_font():
    try:
        return pygame.font.SysFont("segoeui", 18, bold=True)
    except Exception:
        return pygame.font.Font(None, 22)


def draw_hud(screen, player, enemy):
    font   = _load_font()
    sw     = screen.get_width()

    # ── Barra del jugador (izquierda) ────────────────────────────────────────
    player_ratio = max(0, player.hp / player.max_hp)
    player_bar_x = MARGIN

    # Nombre
    name_surf = font.render(player.name, True, COLOR_NAME)
    screen.blit(name_surf, (player_bar_x, BAR_Y - 20))

    # Fondo
    pygame.draw.rect(screen, COLOR_BG,
                     (player_bar_x, BAR_Y, BAR_W, BAR_H), border_radius=6)
    # Relleno
    pygame.draw.rect(screen, COLOR_PLAYER,
                     (player_bar_x, BAR_Y, int(BAR_W * player_ratio), BAR_H),
                     border_radius=6)
    # Borde
    pygame.draw.rect(screen, COLOR_BORDER,
                     (player_bar_x, BAR_Y, BAR_W, BAR_H), 2, border_radius=6)

    # ── Barra del enemigo (derecha) ──────────────────────────────────────────
    enemy_ratio = max(0, enemy.hp / enemy.max_hp)
    enemy_bar_x = sw - MARGIN - BAR_W

    # Nombre (alineado a la derecha)
    name_surf = font.render(enemy.name, True, COLOR_NAME)
    screen.blit(name_surf, (sw - MARGIN - name_surf.get_width(), BAR_Y - 20))

    # Fondo
    pygame.draw.rect(screen, COLOR_BG,
                     (enemy_bar_x, BAR_Y, BAR_W, BAR_H), border_radius=6)
    # Relleno — se vacía de derecha a izquierda
    fill_w = int(BAR_W * enemy_ratio)
    pygame.draw.rect(screen, COLOR_ENEMY,
                     (enemy_bar_x + BAR_W - fill_w, BAR_Y, fill_w, BAR_H),
                     border_radius=6)
    # Borde
    pygame.draw.rect(screen, COLOR_BORDER,
                     (enemy_bar_x, BAR_Y, BAR_W, BAR_H), 2, border_radius=6)