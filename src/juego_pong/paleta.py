import pygame

class Paleta:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def mover(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pygame.display.get_surface().get_alto():
            self.rect.bottom = pygame.display.get_surface().get_alto()

    def renderizar(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def choque(self, ball):
        return self.rect.colliderect(ball.rect)