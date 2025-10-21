import pygame
from juego_pong.juego_pong import Juego
from seguidor_mano.seguidor_mano import SeguidorMano

def main():
    pygame.init()
    screen = pygame.display.set_mode((1260, 720))
    pygame.display.set_caption("Hand Controlled Pong")

    reloj = pygame.time.Clock()
    seguidor = SeguidorMano(2)
    juego = Juego(screen.get_width(), screen.get_height(), seguidor)

    juego.ejecutar()

    pygame.quit()

if __name__ == "__main__":
    main()