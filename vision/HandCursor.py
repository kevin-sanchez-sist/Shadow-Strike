import cv2
import mediapipe as mp
import numpy as np

PINCH_THRESHOLD   = 0.05
PINCH_COOLDOWN_MS = 600


class HandCursor:
    def __init__(self):
        self.mp_hands   = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self._frame          = None
        self._hand_landmarks = None
        self._is_pinching    = False
        self._click_ready    = False
        self._was_pinching   = False
        self._cooldown_ms    = 0

    def update(self, delta_time: int = 16):
        if self._cooldown_ms > 0:
            self._cooldown_ms -= delta_time

        ret, frame = self.cap.read()
        if not ret:
            self._frame = None
            self._hand_landmarks = None
            return

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        self._frame = frame

        if result.multi_hand_landmarks:
            self._hand_landmarks = result.multi_hand_landmarks[0]
            self._update_pinch()
        else:
            self._hand_landmarks = None
            self._is_pinching    = False
            self._was_pinching   = False

    def _update_pinch(self):
        lm    = self._hand_landmarks.landmark
        thumb = lm[4]
        index = lm[8]
        dist  = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)
        pinching_now = dist < PINCH_THRESHOLD

        if pinching_now and not self._was_pinching and self._cooldown_ms <= 0:
            self._click_ready = True
            self._cooldown_ms = PINCH_COOLDOWN_MS

        self._is_pinching  = pinching_now
        self._was_pinching = pinching_now

    def get_position(self, screen_w: int, screen_h: int) -> tuple[int, int] | None:
        if not self._hand_landmarks:
            return None
        index = self._hand_landmarks.landmark[8]
        return (int(index.x * screen_w), int(index.y * screen_h))

    def is_pinching(self) -> bool:
        return self._is_pinching

    def consume_click(self) -> bool:
        if self._click_ready:
            self._click_ready = False
            return True
        return False

    def draw_on(self, screen, screen_w: int = None, screen_h: int = None):
        """
        Dibuja el cursor directamente con pygame:
        - Mano abierta: circulo blanco con crosshair
        - Pinch activo: circulo amarillo relleno (feedback visual de click)
        """
        import pygame

        if screen_w is None:
            screen_w = screen.get_width()
        if screen_h is None:
            screen_h = screen.get_height()

        pos = self.get_position(screen_w, screen_h)
        if pos is None:
            return

        x, y = pos

        if self._is_pinching:
            # Anillo exterior
            pygame.draw.circle(screen, (255, 220, 50), (x, y), 22, 3)
            # Relleno semitransparente
            surf = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 220, 50, 120), (24, 24), 20)
            screen.blit(surf, (x - 24, y - 24))
            # Punto central
            pygame.draw.circle(screen, (255, 220, 50), (x, y), 6)
        else:
            # Sombra
            shadow = pygame.Surface((56, 56), pygame.SRCALPHA)
            pygame.draw.circle(shadow, (0, 0, 0, 60), (28, 30), 18)
            screen.blit(shadow, (x - 28, y - 28))
            # Relleno semitransparente
            surf = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 255, 180), (24, 24), 18)
            screen.blit(surf, (x - 24, y - 24))
            # Borde
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 18, 2)
            # Crosshair central
            pygame.draw.line(screen, (255, 255, 255), (x - 5, y), (x + 5, y), 2)
            pygame.draw.line(screen, (255, 255, 255), (x, y - 5), (x, y + 5), 2)

    def show_camera(self):
        if self._frame is None:
            return
        display = self._frame.copy()
        if self._hand_landmarks:
            self.mp_drawing.draw_landmarks(
                display,
                self._hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
            )
        cv2.imshow("Shadow Strike - Cursor", display)
        cv2.waitKey(1)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()