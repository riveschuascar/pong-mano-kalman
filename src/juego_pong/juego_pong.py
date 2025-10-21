import pygame
from .pelota import Pelota
from .paleta import Paleta

class Juego:
    def __init__(self, ancho, alto, seguidor_mano):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()
        self.ejecucion = True
        self.seguidor_mano = seguidor_mano

        self.pelota = Pelota(self.ancho // 2, self.alto // 2, 5, 3, 2)
        self.paleta_izq = Paleta(30, self.alto // 2 - 50, 30, self.alto * 0.1)
        self.paleta_der = Paleta(self.ancho - 40, self.alto // 2 - 50, 30, self.alto * 0.1)

    def ejecutar(self):
        while self.ejecucion:
            self.eventos()
            self.actualizar()
            self.render()
            self.reloj.tick(60)

        pygame.quit()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ejecutar = False

    def actualizar(self):
        self.pelota.update()
        self.paleta_izq.update()
        self.paleta_der.update()

        if self.pelota.rect.colliderect(self.paleta_izq.rect) or self.pelota.rect.colliderect(self.paleta_der.rect):
            self.pelota.rebotar()

        if self.pelota.rect.x < 0 or self.pelota.rect.x > self.ancho:
            self.pelota.reiniciar_posicion(self.ancho // 2, self.alto // 2)

    def renderizar(self):
        self.pantalla.fill((0, 0, 0))
        self.pelota.draw(self.pantalla)
        self.paleta_izq.draw(self.pantalla)
        self.paleta_der.draw(self.pantalla)
        pygame.display.flip()