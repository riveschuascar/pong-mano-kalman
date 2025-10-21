import cv2
import mediapipe as mp
import numpy as np
from FiltroKalman import FiltroKalman

class SeguidorMano:
    def __init__(self, dt):
        self.video_cv2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.mano_mp = mp.solutions.hands
        self.mano = self.mano_mp.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.graficar_mp = mp.solutions.drawing_utils
        self.filtro_kalman = None
        self.dt = dt

    def iniciar_filtro_kalman(self, y_medicion):
        F = np.array([[1.0, self.dt],
                      [0.0, 1.0]])
        H = np.array([[1.0, 0.0]])
        Q = np.array([[1.0, 0.0],
                      [0.0, 1.0]])
        R = np.array([[500.0]]) # Ruido ajustable
        x0 = np.array([[y_medicion],
                       [0.0]])
        P0 = np.eye(2) * 1000.0
        self.filtro_kalman = FiltroKalman(F, H, Q, R, x0, P0)

    def iniciar(self):
        while True:
            ret, imagen = self.video_cv2.read()
            if not ret:
                break

            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            resultado = self.mano.process(imagen_rgb)
            alto, ancho = imagen.shape[:2]

            if resultado.multi_hand_landmarks:
                referencias_mano = resultado.multi_hand_landmarks[0]
                # Usamos WRIST como referencia de palma
                palma = referencias_mano.landmark[self.mano_mp.HandLandmark.WRIST]
                x_px = int(palma.x * ancho)
                y_px = float(palma.y * alto)

                if self.filtro_kalman is None:
                    self.iniciar_filtro_kalman(y_px)

                self.filtro_kalman.predecir()
                z = np.array([[y_px]])
                self.filtro_kalman.actualizar(z)

                y_suavizado = float(self.filtro_kalman.estado_actual[0, 0])

                # Dibujar: medicion (rojo) y filtrado (verde)
                cv2.circle(imagen, (x_px, int(y_px)), 8, (0, 0, 255), -1)
                cv2.circle(imagen, (x_px, int(y_suavizado)), 8, (0, 255, 0), -1)

                # Dibujar esqueleto de MediaPipe para referencia
                self.graficar_mp.draw_landmarks(imagen, referencias_mano, self.mano_mp.HAND_CONNECTIONS)

                # Mostrar valores en pantalla (opcional, breve)
                cv2.putText(imagen, f"medicion={int(y_px)} suavizado={int(y_suavizado)}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("'q' para salir", imagen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.detener()

    def detener(self):
        if self.mano:
            self.mano.close()
        if self.video_cv2 and self.video_cv2.isOpened():
            self.video_cv2.release()
        cv2.destroyAllWindows()