# vision/PoseTracker.py
import cv2
import mediapipe as mp

# ── Umbrales ajustables ──────────────────────────────────────────
SHOULDER_TILT_THRESHOLD = 0.08   # diferencia en Y entre hombros para moverse
JUMP_VELOCITY_THRESHOLD = 0.06   # cuánto debe subir la cadera en un frame para detectar salto
PUNCH_ABOVE_SHOULDER    = 0.04   # cuánto más arriba que el hombro debe estar la muñeca
# ────────────────────────────────────────────────────────────────

class PoseTracker:
    def __init__(self):
        self.mp_pose    = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.landmarks        = None
        self.result_landmarks = None
        self.prev_hip_y       = None   # para detectar salto por velocidad

    # ─────────────────────────────────────────
    #  UPDATE
    # ─────────────────────────────────────────

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)  # efecto espejo
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(frame_rgb)

        if result.pose_landmarks:
            self.landmarks        = result.pose_landmarks.landmark
            self.result_landmarks = result.pose_landmarks
        else:
            self.landmarks        = None
            self.result_landmarks = None

        return frame

    # ─────────────────────────────────────────
    #  ACCIONES DE COMBATE
    # ─────────────────────────────────────────

    def get_action(self) -> str | None:
        if not self.landmarks:
            return None

        lm = self.landmarks

        left_wrist    = lm[15]
        right_wrist   = lm[16]
        left_shoulder = lm[11]
        right_shoulder= lm[12]

        # Mano por encima del hombro (Y menor = más arriba en pantalla)
        left_punch  = left_wrist.y  < left_shoulder.y  - PUNCH_ABOVE_SHOULDER
        right_punch = right_wrist.y < right_shoulder.y - PUNCH_ABOVE_SHOULDER

        if left_punch and right_punch:
            return 'special'

        if left_punch or right_punch:
            return 'attack'

        return None

    # ─────────────────────────────────────────
    #  MOVIMIENTO Y SALTO
    # ─────────────────────────────────────────

    def get_movement(self) -> str | None:
        if not self.landmarks:
            return None

        lm = self.landmarks

        left_shoulder  = lm[11]
        right_shoulder = lm[12]
        left_hip       = lm[23]
        right_hip      = lm[24]

        # ── Salto por velocidad de cadera ──
        hip_y = (left_hip.y + right_hip.y) / 2

        if self.prev_hip_y is not None:
            delta_y = self.prev_hip_y - hip_y  # positivo = cadera subió
            if delta_y > JUMP_VELOCITY_THRESHOLD:
                self.prev_hip_y = hip_y
                return 'jump'

        self.prev_hip_y = hip_y

        # ── Inclinación de hombros ──
        # Si hombro izquierdo baja (Y mayor) → cuerpo inclinado a la izquierda → personaje va a la derecha
        tilt = left_shoulder.y - right_shoulder.y  # positivo = hombro izq más abajo

        if tilt > SHOULDER_TILT_THRESHOLD:
            return 'right'
        if tilt < -SHOULDER_TILT_THRESHOLD:
            return 'left'

        return None

    # ─────────────────────────────────────────
    #  RENDER DE LANDMARKS
    # ─────────────────────────────────────────

    def draw_landmarks(self, frame):
        if self.result_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.result_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
        return frame

    # ─────────────────────────────────────────
    #  VENTANA SEPARADA DE CÁMARA
    # ─────────────────────────────────────────

    def show_camera_window(self, frame):
        """Muestra la cámara en una ventana OpenCV separada al juego."""
        if frame is not None:
            display = self.draw_landmarks(frame.copy())
            cv2.imshow("Shadow Strike - Camara", display)
            cv2.waitKey(1)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()