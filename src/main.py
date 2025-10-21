import pygame
from juego_pong.juego_pong import Juego
from seguidor_mano.seguidor_mano import SeguidorMano

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Hand Controlled Pong")

    reloj = pygame.time.Clock()
    DIFICULTAD = 3
    seguidor = SeguidorMano(2)
    seguidor.iniciar(background=True)
    juego = Juego(screen.get_width(), screen.get_height(), seguidor, DIFICULTAD)

    juego.ejecutar()

    pygame.quit()

if __name__ == "__main__":
    main()