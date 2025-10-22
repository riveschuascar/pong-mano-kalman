import pygame
from .pelota import Pelota
from .paleta import Paleta

class Juego:
    def __init__(self, ancho, alto, seguidor_mano=None):
        pygame.init()
        self.ancho = int(ancho)
        self.alto = int(alto)
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()
        self.ejecucion = True
        self.seguidor_mano = seguidor_mano

        # initialize game objects
        initial_speed = 5
        self.pelota = Pelota(self.ancho // 2, self.alto // 2, 8, initial_speed, initial_speed * 0.75)
        pal_alto = int(self.alto * 0.3)
        self.paleta_der = Paleta(self.ancho - 50, self.alto // 2 - pal_alto // 2, 20, pal_alto)
        self.score = 0
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

        # keyboard control only for right paddle (Up/Down)
        keys = pygame.key.get_pressed()
        dy = 6
        if keys[pygame.K_UP]:
            self.paleta_der.mover(-dy)
        if keys[pygame.K_DOWN]:
            self.paleta_der.mover(dy)

        # If we have a seguidor_mano instance and it provides a y position, control the right paddle
        if self.seguidor_mano is not None:
            y_val = getattr(self.seguidor_mano, 'y_suavizado', None)
            if y_val is not None:
                # center paleta_der on y_val
                self.paleta_der.rect.centery = int(y_val)

    def _cambiar_velocidad_pelota(self):
        vel_act_x = self.pelota.vel_x
        vel_act_y = self.pelota.vel_y
        if vel_act_x < 0:
            self.pelota.vel_x = vel_act_x - (0.15 * self.score)
        else:
            self.pelota.vel_x = vel_act_x + (0.15 * self.score * 0.75)
        if vel_act_y < 0:
            self.pelota.vel_y = vel_act_y - (0.15 * self.score)
        else:
            self.pelota.vel_y = vel_act_y + (0.15 * self.score * 0.75)

    def _reset_velocidad_pelota(self):
        self.pelota.vel_x = 5
        self.pelota.vel_y = 5 * 0.75

    def _actualizar(self):
        self.pelota.mover()

        _ = self.pelota.verificar_rebote_bordes(self.ancho, self.alto)

        collided_der = self.pelota.rect.colliderect(self.paleta_der.rect)
        if collided_der and not self._contact_der:
            self.pelota.rebotar()
            self.score += 1
            self._cambiar_velocidad_pelota()
            self._contact_der = True
        if not collided_der:
            self._contact_der = False

        if self.pelota.x + self.pelota.radio > self.ancho:
            self.score = 0
            self._reset_velocidad_pelota()
            self.pelota.reiniciar_posicion(self.ancho // 2, self.alto // 2)           

    def _renderizar(self):
        self.pantalla.fill((0, 0, 0))
        self.pelota.draw(self.pantalla)
        # render only right paddle
        self.paleta_der.renderizar(self.pantalla)
        # render single score
        if self.font is not None:
            score_surf = self.font.render(str(self.score), True, (255, 255, 255))
            # draw score top-right
            sw = score_surf.get_width()
            self.pantalla.blit(score_surf, (self.ancho - sw - 10, 10))
        pygame.display.flip()