import pygame
import math

# Mapas disponibles: (id retornado, ruta de imagen, nombre visible)
MAPS = [
    ('bosque',      "Image/ElBosque.png",     "El Bosque"),
    ('templo',      "Image/ElTemplo.png",      "El Templo"),
    ('otro_mundo',  "Image/ElOtroMundo.png",   "El Otro Mundo"),
]

# ── Estética ────────────────────────────────────────────────────────────────
COLOR_TITLE = (255, 230, 100)
COLOR_CARD_NORMAL = (20, 18, 40, 200)
COLOR_CARD_HOVER = (55, 40, 110, 230)
COLOR_BORDER = (100, 70, 180)
COLOR_BORDER_HOVER = (190, 140, 255)
COLOR_NAME = (230, 230, 255)
COLOR_NAME_HOVER = (255, 230, 100)
COLOR_HINT = (160, 160, 195)

CARD_W = 300
CARD_H = 390
CARD_GAP = 50
BORDER_RADIUS = 18


def _load_font(size, bold=False):
    try:
        return pygame.font.SysFont("segoeui", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


def map_select(screen):
    """
    Muestra el menú de selección de mapa.
    Retorna: 'bosque', 'templo' o 'otro_mundo'.
    Retorna None si el jugador cierra la ventana.
    """
    W, H = screen.get_size()

    # ── Cargar imágenes ─────────────────────────────────────────────────────
    map_data = []
    for map_id, img_path, map_name in MAPS:
        img_full = pygame.image.load(img_path).convert()
        thumb = pygame.transform.scale(img_full, (CARD_W - 20, 195))
        map_data.append((map_id, img_full, thumb, map_name))

    # ── Posición de las tarjetas (centradas) ────────────────────────────────
    total_w = len(MAPS) * CARD_W + (len(MAPS) - 1) * CARD_GAP
    start_x = (W - total_w) // 2
    card_y = (H - CARD_H) // 2 + 50

    cards = []
    for i, (map_id, img_full, thumb, map_name) in enumerate(map_data):
        rect = pygame.Rect(start_x + i * (CARD_W + CARD_GAP),
                           card_y, CARD_W, CARD_H)
        cards.append((map_id, img_full, thumb, map_name, rect))

    # ── Fuentes ─────────────────────────────────────────────────────────────
    font_title = _load_font(56, bold=True)
    font_name = _load_font(30, bold=True)
    font_hint = _load_font(22)

    # Overlay oscuro fijo
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    clock = pygame.time.Clock()
    hover_idx = -1
    bg_idx = 0          # índice del fondo activo
    glow_t = 0.0

    running = True
    while running:
        dt = clock.tick(60)
        glow_t += dt * 0.003

        mouse_pos = pygame.mouse.get_pos()

        # Detectar hover
        hover_idx = -1
        for i, (_, _, _, _, rect) in enumerate(cards):
            if rect.collidepoint(mouse_pos):
                hover_idx = i
                break

        # El fondo cambia según la tarjeta hovered (o la 0 por defecto)
        if hover_idx != -1:
            bg_idx = hover_idx

        # ── Eventos ─────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for map_id, _, _, _, rect in cards:
                    if rect.collidepoint(mouse_pos):
                        return map_id

        # ── Render ──────────────────────────────────────────────────────────
        # Fondo dinámico
        bg_scaled = pygame.transform.scale(map_data[bg_idx][1], (W, H))
        screen.blit(bg_scaled, (0, 0))
        screen.blit(overlay, (0, 0))

        # Título con sombra y brillo pulsante
        title_text = "SELECCIONA EL ESCENARIO"
        title_surf = font_title.render(title_text, True, COLOR_TITLE)
        title_rect = title_surf.get_rect(centerx=W // 2, y=30)
        screen.blit(title_surf,  title_rect)

        # Línea decorativa bajo el título

        # Tarjetas
        for i, (map_id, _, thumb, map_name, rect) in enumerate(cards):
            is_hover = (i == hover_idx)

            # Desplazamiento vertical en hover (efecto "levantar")
            offset_y = -10 if is_hover else 0
            draw_rect = rect.move(0, offset_y)

            # Panel semitransparente
            card_surf = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
            c = COLOR_CARD_HOVER if is_hover else COLOR_CARD_NORMAL
            pygame.draw.rect(card_surf, c, (0, 0, CARD_W, CARD_H),
                             border_radius=BORDER_RADIUS)
            screen.blit(card_surf, draw_rect.topleft)

            # Borde
            bc = COLOR_BORDER_HOVER if is_hover else COLOR_BORDER
            bw = 3 if is_hover else 2
            pygame.draw.rect(screen, bc, draw_rect, bw,
                             border_radius=BORDER_RADIUS)

            # Miniatura
            thumb_x = draw_rect.x + 10
            thumb_y = draw_rect.y + 14
            screen.blit(thumb, (thumb_x, thumb_y))

            # Línea separadora
            sep_y = thumb_y + thumb.get_height() + 10
            pygame.draw.line(screen, bc,
                             (draw_rect.x + 15, sep_y),
                             (draw_rect.right - 15, sep_y), 1)

            # Nombre del mapa
            nc = COLOR_NAME_HOVER if is_hover else COLOR_NAME
            name_surf = font_name.render(map_name, True, nc)
            name_rect = name_surf.get_rect(
                centerx=draw_rect.centerx, y=sep_y + 12)
            screen.blit(name_surf, name_rect)

        # Hint ESC
        esc_surf = font_hint.render("ESC — Volver", True, COLOR_HINT)
        screen.blit(esc_surf, (20, H - 38))

        pygame.display.flip()
