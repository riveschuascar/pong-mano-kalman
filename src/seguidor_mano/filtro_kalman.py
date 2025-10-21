import numpy as np

class FiltroKalman:
    def __init__(self, F, H, Q, R, x0, P0):
        self.transicion = F  # Matriz de transición de estado
        self.observacion = H # Matriz de observación
        self.covarianza_ruido_proceso = Q # Covarianza del ruido del proceso (wk)
        self.covarianza_ruido_medicion = R # Covarianza del ruido de la medición (vk)
        self.estado_actual = x0 # Estimación inicial del estado
        self.covarianza_actual = P0 # Covarianza inicial del error de estimación

    def predecir(self):
        # 1. Proyectar el estado hacia adelante
        self.estado_actual = self.transicion @ self.estado_actual
        # 2. Proyectar la covarianza del error hacia adelante
        self.covarianza_actual = self.transicion @ self.covarianza_actual @ self.transicion.T + self.covarianza_ruido_proceso
        return self.estado_actual

    def actualizar(self, z):
        # 1. Calcular la innovación (residuo de la medición)
        y = z - self.observacion @ self.estado_actual
        # 2. Calcular la covarianza de la innovación
        S = self.observacion @ self.covarianza_actual @ self.observacion.T + self.covarianza_ruido_medicion
        # 3. Calcular la ganancia de Kalman
        K = self.covarianza_actual @ self.observacion.T @ np.linalg.inv(S)
        # 4. Actualizar la estimación del estado
        self.estado_actual = self.estado_actual + K @ y
        # 5. Actualizar la covarianza del error
        self.covarianza_actual = (np.eye(self.covarianza_actual.shape[0]) - K @ self.observacion) @ self.covarianza_actual
        return self.estado_actual