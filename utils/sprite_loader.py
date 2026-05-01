import pygame
import os

def load_action_frames(base_path: str, character: str, action: str, scale=1.0):
    """
    Carga todos los frames de una acción específica de un personaje.
    base_path: ruta a la carpeta sprites/
    character: 'Knight', 'Mage', 'Rogue'
    action: 'idle', 'walk', 'attack_1', 'hurt', 'death', etc.
    """
    folder = os.path.join(base_path, character, action)
    
    if not os.path.exists(folder):
        raise FileNotFoundError(f"No existe la carpeta: {folder}")
    
    files = sorted([
        file for file in os.listdir(folder)
        if file.endswith('.png')
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


def load_all_actions(base_path: str, character: str, actions: list[str], scale = 1.0):
    """
    Carga todas las acciones de un personaje de una vez.
    Retorna un diccionario: { 'idle': [...], 'walk': [...], ... }
    """
    sprites = {}
    for action in actions:
        sprites[action] = load_action_frames(base_path, character, action, scale)
    return sprites