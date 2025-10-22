import threading
import cv2
import mediapipe as mp
import numpy as np
from seguidor_mano.filtro_kalman import FiltroKalman
from seguidor_mano.filtro_kalman_extendido import FiltroKalmanExtendido

class SeguidorMano:
    def __init__(self, dt):
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

        # Video capture
        self.video_cv2 = cv2.VideoCapture(0)

        # último valor suavizado (None hasta que haya datos)
        self.y_suavizado = None

        # control de hilo
        self._thread = None
        self._stop_event = threading.Event()

    def iniciar_filtro_kalman(self, y_medicion):
        # Estado inicial [posicion, velocidad, aceleracion]
        x0 = np.array([[y_medicion], [0.0], [0.0]])
        P0 = np.eye(3) * 500.0  # incertidumbre inicial
        Q = np.diag([1.0, 1.0, 1.0])  # ruido del proceso
        R = np.array([[1000.0]])      # ruido de medición
        self.filtro_kalman = FiltroKalmanExtendido(Q, R, x0, P0, self.dt)

    def _loop(self):
        while not self._stop_event.is_set():
            ret, imagen = self.video_cv2.read()
            if not ret:
                # si no hay frame, esperar un poco y continuar
                cv2.waitKey(10)
                continue

            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            resultado = self.mano.process(imagen_rgb)
            alto, ancho = imagen.shape[:2]

            if resultado.multi_hand_landmarks:
                referencias_mano = resultado.multi_hand_landmarks[0]
                palma = referencias_mano.landmark[self.mano_mp.HandLandmark.WRIST]
                x_px = int(palma.x * ancho)
                y_px = float(palma.y * alto)

                if self.filtro_kalman is None:
                    self.iniciar_filtro_kalman(y_px)

                self.filtro_kalman.predecir()
                z = np.array([[y_px]])
                self.filtro_kalman.actualizar(z)

                self.y_suavizado = float(self.filtro_kalman.x[0, 0])

                # Opcional: dibujar para debugging (se puede desactivar)
                cv2.circle(imagen, (x_px, int(y_px)), 8, (0, 0, 255), -1)
                cv2.circle(imagen, (x_px, int(self.y_suavizado)), 8, (0, 255, 0), -1)
                self.graficar_mp.draw_landmarks(imagen, referencias_mano, self.mano_mp.HAND_CONNECTIONS)
                cv2.putText(imagen, f"medicion={int(y_px)} suavizado={int(self.y_suavizado)}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # mostrar ventana de debug (puedes comentar si no la quieres)
            cv2.imshow("SeguidorMano - 'q' sale", imagen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._stop_event.set()

        self.detener()

    def iniciar(self, background=True):
        """Inicia la captura.

        Si background=True, lanza un hilo y regresa inmediatamente.
        Si background=False, ejecuta el loop en el hilo actual (bloqueante).
        """
        self._stop_event.clear()
        if background:
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._loop, daemon=True)
                self._thread.start()
        else:
            self._loop()

    def detener(self):
        # Señalizar stop y liberar recursos
        self._stop_event.set()
        if self.mano:
            try:
                self.mano.close()
            except Exception:
                pass
        if self.video_cv2 and self.video_cv2.isOpened():
            try:
                self.video_cv2.release()
            except Exception:
                pass
        cv2.destroyAllWindows()
