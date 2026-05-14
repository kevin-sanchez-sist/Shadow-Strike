import pygame
import os


def load_action_frames(base_path: str, character: str, action: str,
                       scale=1.0, folder_name: str = None):
    """
    Carga todos los frames de una acción específica de un personaje.

    base_path   : ruta a la carpeta Sprites/
    character   : 'Knight', 'Mage', 'Rogue'
    action      : nombre interno de la acción (clave del dict resultante)
    scale       : factor de escala aplicado a cada frame
    folder_name : nombre real de la carpeta si difiere de `action`
                  (útil para personajes con carpetas en PascalCase, ej. 'Idle')
    """
    folder = os.path.join(base_path, character, folder_name or action)

    if not os.path.exists(folder):
        raise FileNotFoundError(f"No existe la carpeta: {folder}")

    files = sorted([
        f for f in os.listdir(folder)
        if f.endswith('.png')
    ])

    if not files:
        raise ValueError(f"No hay sprites en: {folder}")

    frames = []
    for file in files:
        path = os.path.join(folder, file)
        image = pygame.image.load(path).convert_alpha()
        if scale != 1.0:
            w, h = image.get_size()
            image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
        frames.append(image)

    return frames


def load_all_actions(base_path: str, character: str, actions: list[str],
                     scale=1.0, folder_map: dict = None):
    """
    Carga todas las acciones de un personaje de una vez.
    Retorna un diccionario: { 'idle': [...], 'run': [...], ... }

    folder_map : dict opcional { nombre_acción: nombre_carpeta_real }
                 Solo necesario cuando las carpetas tienen nombre diferente
                 al nombre interno de la acción (ej. Rogue usa PascalCase).
    """
    folder_map = folder_map or {}
    sprites = {}
    for action in actions:
        folder_name = folder_map.get(action)   # None si no está en el mapa
        sprites[action] = load_action_frames(
            base_path, character, action, scale, folder_name
        )
    return sprites