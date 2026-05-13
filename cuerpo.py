import cv2
import mediapipe as mp

# INICIALIZAR MEDIAPIPE POSE

# Módulo de pose de MediaPipe
mp_pose = mp.solutions.pose

# Objeto detector de pose
pose = mp_pose.Pose(
    static_image_mode=False,         # False = modo video en tiempo real
    model_complexity=1,              # complejidad del modelo (0, 1 o 2)
    smooth_landmarks=True,           # suaviza landmarks entre frames
    enable_segmentation=False,       # no segmenta el cuerpo
    min_detection_confidence=0.5,    # confianza mínima de detección
    min_tracking_confidence=0.5      # confianza mínima de seguimiento
)

# Utilidad para dibujar landmarks y conexiones
mp_drawing = mp.solutions.drawing_utils

# LISTA DE NOMBRES DE LOS 33 PUNTOS

# Estos son todos los landmarks que MediaPipe Pose puede detectar
nombres_landmarks = [
    "NARIZ",                # 0
    "OJO_IZQ_INTERNO",      # 1
    "OJO_IZQ",              # 2
    "OJO_IZQ_EXTERNO",      # 3
    "OJO_DER_INTERNO",      # 4
    "OJO_DER",              # 5
    "OJO_DER_EXTERNO",      # 6
    "OREJA_IZQ",            # 7
    "OREJA_DER",            # 8
    "BOCA_IZQ",             # 9
    "BOCA_DER",             # 10
    "HOMBRO_IZQ",           # 11
    "HOMBRO_DER",           # 12
    "CODO_IZQ",             # 13
    "CODO_DER",             # 14
    "MUNECA_IZQ",           # 15
    "MUNECA_DER",           # 16
    "MEÑIQUE_IZQ",          # 17
    "MEÑIQUE_DER",          # 18
    "INDICE_IZQ",           # 19
    "INDICE_DER",           # 20
    "PULGAR_IZQ",           # 21
    "PULGAR_DER",           # 22
    "CADERA_IZQ",           # 23
    "CADERA_DER",           # 24
    "RODILLA_IZQ",          # 25
    "RODILLA_DER",          # 26
    "TOBILLO_IZQ",          # 27
    "TOBILLO_DER",          # 28
    "TALON_IZQ",            # 29
    "TALON_DER",            # 30
    "PIE_IZQ",              # 31
    "PIE_DER"               # 32
]

# ABRIR CÁMARA

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

# Configuración de cámara
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Presiona 'q' para salir.")

# BUCLE PRINCIPAL

while True:
    # Leer frame
    ret, frame = cap.read()

    if not ret:
        print("Error al leer frame.")
        break

    # Voltear imagen para efecto espejo
    frame = cv2.flip(frame, 1)

    # Convertir de BGR a RGB porque MediaPipe trabaja en RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar frame
    results = pose.process(rgb_frame)

    # Si detecta pose
    if results.pose_landmarks:
        # Dibujar esqueleto general
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

        # Dimensiones del frame
        h, w, _ = frame.shape

        # Lista de landmarks detectados
        landmarks = results.pose_landmarks.landmark

        # Recorrer todos los puntos detectados
        for i, lm in enumerate(landmarks):
            # Convertir coordenadas normalizadas a coordenadas en píxeles
            x = int(lm.x * w)
            y = int(lm.y * h)

            # Nombre del landmark actual
            nombre = nombres_landmarks[i]

            # Dibujar un círculo más visible en cada punto
            cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)

            # Mostrar índice y nombre del punto
            texto = f"{i}-{nombre}"

            cv2.putText(
                frame,
                texto,
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

    # Mostrar ventana
    cv2.imshow("Pose Corporal - Todos los puntos", frame)

    # Salir con q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# CIERRE SEGURO

cap.release()
cv2.destroyAllWindows()