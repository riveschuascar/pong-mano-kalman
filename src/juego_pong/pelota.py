import pygame

class Pelota:
    def __init__(self, x, y, radio, vel_x, vel_y):
        self.x = float(x)
        self.y = float(y)
        self.radio = int(radio)
        self.vel_x = float(vel_x)
        self.vel_y = float(vel_y)
        # rect used for collision with paletas
        self.rect = pygame.Rect(int(self.x - self.radio), int(self.y - self.radio),
                                self.radio * 2, self.radio * 2)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
        # keep rect in sync
        self.rect.center = (int(self.x), int(self.y))

    def rebotar(self):
        self.vel_x = -self.vel_x

    def rebotar_vertical(self):
        self.vel_y = -self.vel_y

    def reiniciar_posicion(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.rect.center = (int(self.x), int(self.y))

    def choque(self, paleta):
        """Check collision against a Paleta instance (which has .rect).
        Reverse X velocity on collision.
        """
        if self.rect.colliderect(paleta.rect):
            self.rebotar()

    def verificar_rebote_bordes(self, ancho, alto):
        bounced = False
        # borde superior
        if self.y - self.radio <= 0:
            self.y = float(self.radio)
            self.rebotar_vertical()
            bounced = True
        # borde inferior
        if self.y + self.radio >= alto:
            self.y = float(alto - self.radio)
            self.rebotar_vertical()
            bounced = True
        if self.x - self.radio <= 0:
            self.x = float(self.radio)
            self.rebotar()
            bounced = True
        # mantener rect en sincronía
        self.rect.center = (int(self.x), int(self.y))
        return bounced

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radio)