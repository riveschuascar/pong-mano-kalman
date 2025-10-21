class Pelota:
    def __init__(self, x, y, radio, vel_x, vel_y):
        self.x = x
        self.y = y
        self.radio = radio
        self.vel_x = vel_x
        self.vel_y = vel_y

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def rebotar(self):
        self.vel_x = -self.vel_x

    def reiniciar_posicion(self, x, y):
        self.x = x
        self.y = y

    def choque(self, paleta):
        if (self.x + self.radio > paleta.x and
            self.x - self.radio < paleta.x + paleta.ancho and
            self.y + self.radio > paleta.y and
            self.y - self.radio < paleta.y + paleta.alto):
            self.rebotar()