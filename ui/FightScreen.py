# ui/FightScreen.py
import random
import pygame
import sys
from utils.sprite_loader import load_all_actions, load_action_frames
from utils.Combat import check_hit, check_projectile_hits
from Players.Knight import Knight, KNIGHT_ACTIONS
from Players.Rogue import Rogue, ROGUE_ACTIONS, ROGUE_FOLDER_MAP
from Players.Mage import Mage, MAGE_ACTIONS, MAGE_FOLDER_MAP
from Players.EnemyAI import EnemyAI
from vision.PoseTracker import PoseTracker
from ui.HUD import draw_hud
from ui.ResultScreen import result_screen

# ── Fondos por mapa ──────────────────────────────────────────────────────────
MAP_BACKGROUNDS = {
    'bosque':     "Image/ElBosque.png",
    'templo':     "Image/ElTemplo.png",
    'otro_mundo': "Image/ElOtroMundo.png",
}

# ── Música por mapa ──────────────────────────────────────────────────────────
MAP_MUSIC = {
    'bosque':     "sounds/cancion2_op.wav",
    'templo':     "sounds/cancion3_op.wav",
    'otro_mundo': "sounds/cancion1_op.wav",
}


def get_character_config():
    """Retorna la configuración de personajes, inicializando los sonidos."""
    # Se llama dentro de la función para asegurar que pygame.mixer esté inicializado
    death_sound = pygame.mixer.Sound("sounds/muerte.wav")

    return {
        'knight': {
            'folder':     'Knight',
            'actions':    KNIGHT_ACTIONS,
            'folder_map': None,
            'scale':      2.5,
            'class':      Knight,
            'spawn_x':    100,
            'spawn_y':    450,
            'sounds': {
                'attack':       pygame.mixer.Sound("sounds/atq_basico_kng.wav"),
                'attack_extra': pygame.mixer.Sound("sounds/atq_especial_kng.wav"),
                'death':        death_sound,
                # 'no_hit': pygame.mixer.Sound("sounds/no_hit_espada.wav"), # Pendiente
            }
        },
        'rogue': {
            'folder':     'Rogue',
            'actions':    ROGUE_ACTIONS,
            'folder_map': ROGUE_FOLDER_MAP,
            'scale':      2.5,
            'class':      Rogue,
            'spawn_x':    100,
            'spawn_y':    450,
            'sounds': {
                'attack':       pygame.mixer.Sound("sounds/bola_fuego.wav"),
                'attack_extra': pygame.mixer.Sound("sounds/bola_fuego.wav"),
                'death':        death_sound,
            }
        },
        'mage': {
            'folder':     'Mage',
            'actions':    MAGE_ACTIONS,
            'folder_map': MAGE_FOLDER_MAP,
            'scale':      2.5,
            'class':      Mage,
            'spawn_x':    100,
            'spawn_y':    450,
            'sounds': {
                'attack':       pygame.mixer.Sound("sounds/ninja.wav"),  # reemplaza con el sonido del mago cuando lo tengas
                'attack_extra': pygame.mixer.Sound("sounds/ninja.wav"),
                'death':        death_sound,
            }
        },
    }


def fight_screen(screen, personaje, mapa='templo'):
    # Detener la música del menú e iniciar la de combate
    pygame.mixer.music.stop()
    music_path = MAP_MUSIC.get(mapa)
    if music_path:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # ── Fondo ────────────────────────────────────────────────────────────────
    bg_path = MAP_BACKGROUNDS.get(mapa, "Image/ElTemplo.png")
    fondo = pygame.image.load(bg_path)
    fondo = pygame.transform.scale(fondo, screen.get_size())

    # ── Personaje ────────────────────────────────────────────────────────────
    char_config = get_character_config()
    cfg = char_config.get(personaje)
    if cfg is None:
        raise ValueError(f"Personaje desconocido: '{personaje}'")

    sprites = load_all_actions(
        "Sprites",
        cfg['folder'],
        cfg['actions'],
        scale=cfg['scale'],
        folder_map=cfg['folder_map'],
    )
    if cfg['class'] == Mage:
        fire_frames = load_action_frames("Sprites", "Mage", "Fire",
                                        scale=cfg['scale'], folder_name="Fire")
        fire_extra_frames = load_action_frames("Sprites", "Mage", "Fire_Extra",
                                            scale=cfg['scale'], folder_name="Fire_Extra")
        player = Mage(x=cfg['spawn_x'], y=cfg['spawn_y'],
                    sprites=sprites,
                    fire_frames=fire_frames,
                    fire_extra_frames=fire_extra_frames,
                    sounds=cfg['sounds'])
    else:
        player = cfg['class'](x=cfg['spawn_x'], y=cfg['spawn_y'],
                            sprites=sprites, sounds=cfg['sounds'])
    # ── Enemigo aleatorio ─────────────────────────────────────────────────────
    enemy_key = random.choice([k for k in char_config if k != personaje])
    ecfg = char_config[enemy_key]
    enemy_sprites = load_all_actions(
        "Sprites",
        ecfg['folder'],
        ecfg['actions'],
        scale=ecfg['scale'],
        folder_map=ecfg['folder_map'],
    )
    if ecfg['class'] == Mage:
        fire_frames = load_action_frames("Sprites", "Mage", "Fire",
                                        scale=ecfg['scale'], folder_name="Fire")
        fire_extra_frames = load_action_frames("Sprites", "Mage", "Fire_Extra",
                                            scale=ecfg['scale'], folder_name="Fire_Extra")
        enemy = Mage(x=1100, y=450,
                    sprites=enemy_sprites,
                    fire_frames=fire_frames,
                    fire_extra_frames=fire_extra_frames,
                    facing='left',
                    sounds=ecfg['sounds'])
    else:
        enemy = ecfg['class'](x=1100, y=450,
                            sprites=enemy_sprites,
                            facing='left',
                            sounds=ecfg['sounds'])
    ai = EnemyAI()

    # ── Sistemas ─────────────────────────────────────────────────────────────
    tracker = PoseTracker()
    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60)
        frame = tracker.update()
        tracker.show_camera_window(frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tracker.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        action = tracker.get_action()
        movement = tracker.get_movement()

        if not player.is_attacking and not player.is_hurt:
            # ── Movimiento ───────────────────────────────────────────────────
            if movement == 'right':
                player.vel_x = player.speed
                player.facing = 'right'
                if player.on_ground:
                    player.set_action('run')

            elif movement == 'left':
                player.vel_x = -player.speed
                player.facing = 'left'
                if player.on_ground:
                    player.set_action('run')

            elif movement == 'jump' and player.on_ground:
                player.vel_y = -40
                player.on_ground = False
                player.set_action('jump')

            else:
                player.vel_x = 0
                if player.on_ground:
                    player.set_action('idle')

            # ── Ataques (MediaPipe) ──────────────────────────────────────────
            if action == 'attack':
                player.attack(attack_index=0)
            elif action == 'special':
                player.attack(attack_index=1)

        if player.hp == 0 or enemy.hp == 0:
            slow_delta = delta_time // 4
            player.update(slow_delta)
            enemy.update(slow_delta)
        else:
            player.update(delta_time)
            enemy.update(delta_time)
        
        if not player.is_alive:
            result_screen(screen, won=False)
            return
        if not enemy.is_alive:
            result_screen(screen, won=True)
            return

        ai.update(enemy, player, delta_time)
        ai.apply(enemy, player)

        # El jugador golpea al enemigo
        if check_hit(player, enemy):
            attack_data = next(
                (a for a in player.attacks if a['action'] == player.action), None
            )
            if attack_data:
                enemy.take_damage(attack_data['damage'])

        # El enemigo golpea al jugador
        if check_hit(enemy, player):
            attack_data = next(
                (a for a in enemy.attacks if a['action'] == enemy.action), None
            )
            if attack_data:
                player.take_damage(attack_data['damage'])
        
        # Proyectiles del jugador → enemigo
        dmg = check_projectile_hits(player, enemy)
        if dmg > 0:
            enemy.take_damage(dmg)

        # Proyectiles del enemigo → jugador
        dmg = check_projectile_hits(enemy, player)
        if dmg > 0:
            player.take_damage(dmg)

        screen.blit(fondo, (0, 0))
        player.draw(screen)
        enemy.draw(screen)
        draw_hud(screen, player, enemy)
        pygame.display.flip()

    tracker.release()
    pygame.mixer.music.stop()
