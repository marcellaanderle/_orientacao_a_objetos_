import pygame
import pygame_menu

from jogo import Jogo

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (52, 186, 235)

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.035)
WINDOW_SIZE = (15 * TILE_SIZE, 15 * TILE_SIZE)
WINDOW_SCALE = 0.75
surface = pygame.display.set_mode(WINDOW_SIZE)


def main_background():
    surface.fill(COLOR_BACKGROUND)


def jogar():
    Jogo(TILE_SIZE, surface).partida()


def main() -> None:
    pygame.init()
    pygame.display.set_caption('Galinhas e Dinamites')
    clock = pygame.time.Clock()

    main_menu = pygame_menu.Menu(
        title='Menu',
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE)
    )

    creditos_menu = pygame_menu.Menu(
        title='Créditos',
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE)
    )

    creditos_menu.add.label('Autoras:')
    creditos_menu.add.label('Marcella')
    creditos_menu.add.label('Nayra')
    creditos_menu.add.label('Fernanda')
    creditos_menu.add.vertical_margin(25)
    creditos_menu.add.button('Voltar', pygame_menu.events.BACK)

    main_menu.add.button('Jogar', jogar)
    main_menu.add.button('Créditos', creditos_menu)
    main_menu.add.button('Sair', pygame_menu.events.EXIT)

    running = True
    while running:
        clock.tick(60)
        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background)

        pygame.display.flip()


if __name__ == '__main__':
    main()
