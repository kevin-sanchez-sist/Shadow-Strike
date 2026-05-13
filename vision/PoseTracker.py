# vision/pose_tracker.py
import cv2
import mediapipe as mp

class PoseTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.cap = cv2.VideoCapture(0)
        self.landmarks = None

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(frame_rgb)
        if result.pose_landmarks:
            self.landmarks = result.pose_landmarks.landmark
            self.result_landmarks = result.pose_landmarks  # agrega esta línea
        else:
            self.result_landmarks = None                   # agrega esta línea
        return frame  # retorna el frame

    def get_action(self) -> str | None:
        if not self.landmarks:
            return None

        # Puntos clave
        left_wrist   = self.landmarks[15]
        right_wrist  = self.landmarks[16]
        left_shoulder  = self.landmarks[11]
        right_shoulder = self.landmarks[12]
        left_hip  = self.landmarks[23]
        right_hip = self.landmarks[24]

        hip_x = (left_hip.x + right_hip.x) / 2
        hip_y = (left_hip.y + right_hip.y) / 2

        left_punch  = left_wrist.y  < left_shoulder.y
        right_punch = right_wrist.y < right_shoulder.y

        # Especial: los dos brazos arriba
        if left_punch and right_punch:
            return 'special'

        # Ataque básico: un brazo arriba
        if left_punch or right_punch:
            return 'attack'

        return None

    def get_movement(self) -> str | None:
        """Retorna 'left', 'right', 'jump' o None según posición de cadera."""
        if not self.landmarks:
            return None

        left_hip  = self.landmarks[23]
        right_hip = self.landmarks[24]
        hip_x = (left_hip.x + right_hip.x) / 2
        hip_y = (left_hip.y + right_hip.y) / 2

        # hip_x va de 0 a 1, 0.5 es el centro
        if hip_x < 0.4:
            return 'right'  # la cámara está espejada
        if hip_x > 0.6:
            return 'left'

        # Salto: cadera sube (y disminuye en mediapipe)
        if hip_y < 0.4:
            return 'jump'

        return None

    def release(self):
        self.cap.release()

    def draw_landmarks(self, frame):
        """Dibuja los puntos de mediapipe sobre el frame de la cámara."""
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing.draw_landmarks(
            frame,
            self.result_landmarks,
            self.mp_pose.POSE_CONNECTIONS
        )
        return frame