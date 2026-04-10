import pygame

from board import Board
from constants import BOARD_SIZE_IN_CELL, BOARD_BG_COL, WINDOW_NAME
from pygame import Event, Surface

from sources.sprites.SpriteManager import SpriteManager
from sources.sprites.SpritesConfig import SpriteName
from sources.utils.get_window_size import get_window_size


# FIXME temporary method. To delete
def draw_grid(surface: Surface, board: Board):
    left: int = board.l_border
    top: int = board.t_border
    step: int = board.cell_length_px
    size_in_cell: int = board.size_in_cell

    # Vertical lines
    for i in range(size_in_cell + 1):
        x = left + i * step
        pygame.draw.line(
            surface,
            'white',
            (x, top),
            (x, top + size_in_cell * step),
            1
        )

    # Horizontal lines
    for j in range(size_in_cell + 1):
        y = top + j * step
        pygame.draw.line(
            surface,
            'white',
            (left, y),
            (left + size_in_cell * step, y),
            1
        )


def should_quit_game(event: Event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    return False


def main():
    pygame.init()

    (win_w, win_h), cell_length_px = get_window_size(BOARD_SIZE_IN_CELL)

    surface: Surface = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption(WINDOW_NAME)

    sm: SpriteManager = SpriteManager(cell_length_px)
    # FIXME issue with odd nb_cells
    board: Board = Board(win_w, win_h, cell_length_px)

    pos_x = win_w / 2
    pos_y = win_h / 2
    clock = pygame.time.Clock()
    running: bool = True

    while running:
        for event in pygame.event.get():
            if should_quit_game(event):
                running = False

            surface.fill(BOARD_BG_COL)
            draw_grid(surface, board)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pos_y -= board.cell_length_px
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pos_y += board.cell_length_px
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pos_x -= board.cell_length_px
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pos_x += board.cell_length_px

        surface.blit(sm.get(SpriteName.SNAKE_HEAD_UP), (pos_x, pos_y))

        # TODO provide sequence of rectangle to update?
        pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
