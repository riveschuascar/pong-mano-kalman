import numpy as np

class FiltroKalmanExtendido:
    def __init__(self, Q, R, x0, P0, dt):
        self.Q = Q
        self.R = R
        self.x = x0
        self.P = P0
        self.dt = dt

    def f(self, x):
        """Modelo de movimiento no lineal."""
        y, v, a = x.flatten()
        # Puedes incluir una no linealidad si quieres (p.ej., saturar aceleración)
        a_next = np.tanh(a)
        y_next = y + v * self.dt + 0.5 * a_next * self.dt**2
        v_next = v + a_next * self.dt
        return np.array([[y_next], [v_next], [a_next]])

    def h(self, x):
        """Modelo de observación: solo medimos posición (y)."""
        y, v, a = x.flatten()
        return np.array([[y]])

    def jacobiano_F(self, x):
        y, v, a = x.flatten()
        da_da = 1 - np.tanh(a)**2  # derivada de tanh(a)
        F = np.array([
            [1, self.dt, 0.5 * self.dt**2 * da_da],
            [0, 1, self.dt * da_da],
            [0, 0, da_da]
        ])
        return F

    def jacobiano_H(self, x):
        """Jacobiana del modelo de observación (dh/dx)."""
        H = np.array([[1, 0, 0]])
        return H

    def predecir(self):
        # Predicción del estado con función no lineal
        self.x = self.f(self.x)
        # Jacobiana del modelo de transición
        F = self.jacobiano_F(self.x)
        # Propagación de la covarianza
        self.P = F @ self.P @ F.T + self.Q
        return self.x

    def actualizar(self, z):
        # Predicción de la medición
        z_pred = self.h(self.x)
        y = z - z_pred  # innovación
        H = self.jacobiano_H(self.x)
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ H) @ self.P
        return self.x
