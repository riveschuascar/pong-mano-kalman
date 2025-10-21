import pygame

class Paleta:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def mover(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        # pygame surface height is accessed via get_height()
        surface = pygame.display.get_surface()
        if surface is not None:
            max_h = surface.get_height()
        else:
            max_h = 0
        if self.rect.bottom > max_h:
            self.rect.bottom = max_h

    def renderizar(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def choque(self, ball):
        return self.rect.colliderect(ball.rect)