# Players/EnemyAI.py
import random

# ── Configuración de dificultad MEDIO ────────────────────────────────────────
ATTACK_RANGE        = 90    # distancia horizontal para intentar atacar
RETREAT_RANGE       = 50    # distancia mínima antes de retroceder
DECISION_INTERVAL   = 600   # ms entre cada "pensamiento" del enemigo
MISTAKE_CHANCE      = 0.25  # 25% de probabilidad de tomar una decisión mala
JUMP_CHANCE = 0.15 #15% de probabilidad de saltar al tomar una decisión

STATES = ['idle', 'chase', 'attack', 'retreat']


class EnemyAI:
    """
    Controla las decisiones de un Fighter como enemigo.
    No hereda de Fighter — le dice QUÉ hacer, el Fighter lo ejecuta.
    """

    def __init__(self):
        self.state          = 'idle'
        self.decision_timer = 0
        self.attack_index   = 0   # 0=ataque básico, 1=especial

    def update(self, enemy: object, player: object, delta_time: int):
        """
        enemy  : el Fighter que controla la IA
        player : el Fighter del jugador (para leer su posición)
        """
        if not enemy.is_alive:
            return
        
        self.decision_timer -= delta_time
        if self.decision_timer > 0:
            return   # todavía no es momento de decidir

        self.decision_timer = DECISION_INTERVAL
        self._decide(enemy, player)

    def _decide(self, enemy, player):
        # Con MISTAKE_CHANCE el enemigo toma una decisión aleatoria (errores humanos)
        if random.random() < MISTAKE_CHANCE:
            self.state = random.choice(STATES)
            return

        dist = abs(enemy.x - player.x)

        if enemy.is_alive and enemy.on_ground and random.random() < JUMP_CHANCE:
            enemy.vel_y = -40
            enemy.on_ground = False
            enemy.set_action('jump')
            return

        if not player.is_alive:
            self.state = 'idle'

        elif dist <= RETREAT_RANGE:
            self.state = 'retreat'

        elif dist <= ATTACK_RANGE:
            self.state = 'attack'
            # Ocasionalmente usa ataque especial si lo tiene
            self.attack_index = 1 if random.random() < 0.3 else 0

        else:
            self.state = 'chase'

    def apply(self, enemy, player):
        """
        Traduce el estado actual en acciones concretas sobre el Fighter.
        Llamar después de update(), en el mismo frame.
        """
        if not enemy.is_alive or enemy.is_hurt or enemy.is_attacking:
            return

        # El enemigo siempre mira hacia el jugador
        enemy.facing = 'left' if enemy.x > player.x else 'right'

        if self.state == 'chase':
            # Moverse hacia el jugador
            direction = -1 if enemy.x > player.x else 1
            enemy.vel_x = enemy.speed * direction
            if enemy.on_ground:
                enemy.set_action('run')

        elif self.state == 'attack':
            enemy.vel_x = 0
            enemy.attack(self.attack_index)

        elif self.state == 'retreat':
            # Alejarse del jugador
            direction = 1 if enemy.x > player.x else -1
            enemy.vel_x = enemy.speed * direction
            if enemy.on_ground:
                enemy.set_action('run')

        elif self.state == 'idle':
            enemy.vel_x = 0
            if enemy.on_ground:
                enemy.set_action('idle')