import pygame

from constants import GL_BOARD_SIZE_IN_CELL, GL_BOARD_BG_COLOUR, \
    GL_SNAKE_BODY_COLOUR, GL_WINDOW_NAME
from pygame import Clock, Event, Surface

from sources.board import Board
from sources.direction_enum import Direction
from sources.handle_movement import handle_movement
from sources.utils.get_window_size import get_window_size


def draw_grid(surface: Surface, grid: Surface, pos: tuple[int, int]):
    surface.blit(grid, pos)


def draw_head(surface: Surface, head: Surface, pos: tuple[int, int]):
    surface.blit(head, pos)


def is_game_win_or_lost(board: Board) -> bool:
    return board.is_win() or board.snake.is_dead()


def should_quit_game(event: Event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    return False


def main():
    pygame.init()

    (win_w, win_h), cell_length_px = get_window_size(GL_BOARD_SIZE_IN_CELL)

    surface: Surface = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption(GL_WINDOW_NAME)

    board: Board = Board(win_w, win_h, cell_length_px)

    clock: Clock = pygame.time.Clock()
    quit_game: bool = False

    # Associate each keyboard movement key with its matching Direction
    MOVE_MAP = {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT
    }

    while not quit_game and not is_game_win_or_lost(board):
        for event in pygame.event.get():
            if should_quit_game(event):
                quit_game = True

            if event.type == pygame.KEYDOWN and event.key in MOVE_MAP:
                handle_movement(board, MOVE_MAP[event.key])

        if is_game_win_or_lost(board):
            continue

        surface.fill(GL_BOARD_BG_COLOUR)

        # Draw snake
        snake = board.snake
        draw_head(surface, snake.get_head_surface(), snake.get_head_pos())
        for segment in snake.get_body_without_head():
            pygame.draw.rect(surface, GL_SNAKE_BODY_COLOUR, segment)

        # Draw apples
        for apple in board.apples:
            pygame.draw.rect(surface, apple.colour.value, apple.rect)

        # Draw grid at the end to keep it on the foreground
        draw_grid(surface, board.get_grid(), (board.rect.left, board.rect.top))

        pygame.display.update()

        # TODO remove this tick for training
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
