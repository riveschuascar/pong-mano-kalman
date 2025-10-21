import pygame
from .pelota import Pelota
from .paleta import Paleta

class Juego:
    def __init__(self, ancho, alto, seguidor_mano=None, dificultad=1):
        pygame.init()
        self.ancho = int(ancho)
        self.alto = int(alto)
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()
        self.ejecucion = True
        self.seguidor_mano = seguidor_mano

        # initialize game objects
        self.pelota = Pelota(self.ancho // 2, self.alto // 2, 8, 4 + dificultad * 1.3, 3 + dificultad * 1.3)
        pal_alto = int(self.alto * 0.3)
        self.paleta_izq = Paleta(30, self.alto // 2 - pal_alto // 2, 20, pal_alto)
        self.paleta_der = Paleta(self.ancho - 50, self.alto // 2 - pal_alto // 2, 20, pal_alto)
        # score per paddle
        self.score_izq = 0
        self.score_der = 0
        # contact flags to avoid multiple counts while ball stays colliding
        self._contact_izq = False
        self._contact_der = False
        # font for rendering score
        try:
            self.font = pygame.font.Font(None, 36)
        except Exception:
            self.font = None

    def ejecutar(self):
        while self.ejecucion:
            self._handle_eventos()
            self._actualizar()
            self._renderizar()
            self.reloj.tick(60)

        pygame.quit()

    def _handle_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ejecucion = False

        # simple keyboard control for right paddle (W/S) and left paddle (Up/Down)
        keys = pygame.key.get_pressed()
        # move amount per frame
        dy = 6
        if keys[pygame.K_w]:
            self.paleta_izq.mover(-dy)
        if keys[pygame.K_s]:
            self.paleta_izq.mover(dy)
        if keys[pygame.K_UP]:
            self.paleta_der.mover(-dy)
        if keys[pygame.K_DOWN]:
            self.paleta_der.mover(dy)

        # If we have a seguidor_mano instance and it provides a y position, try to set left paddle
        if self.seguidor_mano is not None:
            # safe attribute access: expect seguidor_mano to expose latest smoothed y in 'y_suavizado'
            y_val = getattr(self.seguidor_mano, 'y_suavizado', None)
            if y_val is not None:
                # center paleta_izq on y_val
                self.paleta_der.rect.centery = int(y_val)

    def _actualizar(self):
        # move pelota
        self.pelota.mover()

        # check top/bottom border collisions and bounce (no score here)
        _ = self.pelota.verificar_rebote_bordes(self.ancho, self.alto)

        # check collisions with left paddle
        collided_izq = self.pelota.rect.colliderect(self.paleta_izq.rect)
        if collided_izq and not self._contact_izq:
            # new collision event for left paddle
            self.pelota.rebotar()
            self.score_izq += 1
            self._contact_izq = True
        if not collided_izq:
            self._contact_izq = False

        # check collisions with right paddle
        collided_der = self.pelota.rect.colliderect(self.paleta_der.rect)
        if collided_der and not self._contact_der:
            # new collision event for right paddle
            self.pelota.rebotar()
            self.score_der += 1
            self._contact_der = True
        if not collided_der:
            self._contact_der = False

        # check out of bounds horizontally
        if self.pelota.x - self.pelota.radio < 0 or self.pelota.x + self.pelota.radio > self.ancho:
            self.pelota.reiniciar_posicion(self.ancho // 2, self.alto // 2)

    def _renderizar(self):
        self.pantalla.fill((0, 0, 0))
        self.pelota.draw(self.pantalla)
        # Paleta uses renderizar method
        self.paleta_izq.renderizar(self.pantalla)
        self.paleta_der.renderizar(self.pantalla)
        # render scores per paddle
        if self.font is not None:
            left_surf = self.font.render(str(self.score_izq), True, (255, 255, 255))
            right_surf = self.font.render(str(self.score_der), True, (255, 255, 255))
            # left score top-left
            self.pantalla.blit(left_surf, (10, 10))
            # right score top-right
            rw = right_surf.get_width()
            self.pantalla.blit(right_surf, (self.ancho - rw - 10, 10))
        pygame.display.flip()