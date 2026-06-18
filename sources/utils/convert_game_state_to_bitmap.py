from itertools import chain

from bitmap import BitMap
from numpy import ndarray

from constants import GL_GAME_STATE_GREEN_APPLE, GL_GAME_STATE_RED_APPLE, \
    GL_GAME_STATE_SNAKE_BODY, GL_GAME_STATE_WALL
from sources.enums.bitindex_enum import BitIndex


def _aligned_green_apples(game_state: ndarray,
                          snake_head_coord: tuple[int, int]) -> list[BitIndex]:
    indices: list[BitIndex] = []

    head_row, head_col = snake_head_coord
    tmp_row, tmp_col = head_row, head_col

    game_state_rows, game_state_cols = game_state.shape

    # Checks for top cells
    while 0 <= tmp_row - 1 < game_state_rows:
        if game_state[tmp_row - 1, tmp_col] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_UP)
        tmp_row -= 1

    tmp_row = head_row

    # Checks for bottom cells
    while 0 <= tmp_row + 1 < game_state_rows:
        if game_state[tmp_row + 1, tmp_col] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_DOWN)
        tmp_row += 1

    tmp_row = head_row

    # Checks for bottom cells
    while 0 <= tmp_row + 1 < game_state_rows:
        if game_state[tmp_row + 1, tmp_col] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_DOWN)
        tmp_row += 1

    tmp_row, tmp_col = head_row, head_col

    # Checks for left cells
    while 0 <= tmp_col - 1 < game_state_cols:
        if game_state[tmp_row, tmp_col - 1] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_LEFT)
        tmp_col -= 1

    tmp_col = head_col

    # Checks for left cells
    while 0 <= tmp_col + 1 < game_state_cols:
        if game_state[tmp_row, tmp_col + 1] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_RIGHT)
        tmp_col += 1

    return indices


def _immediate_red_apples(game_state: ndarray,
                          snake_head_coord: tuple[int, int]) -> list[BitIndex]:
    indices: list[BitIndex] = []

    head_row, head_col = snake_head_coord

    game_state_rows, game_state_cols = game_state.shape

    # Checks for top cell
    if 0 <= head_row - 1 < game_state_rows:
        if game_state[head_row - 1, head_col] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_UP)

    # Checks for bottom cell
    if 0 <= head_row + 1 < game_state_rows:
        if game_state[head_row + 1, head_col] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_DOWN)

    # Checks for left cell
    if 0 <= head_col - 1 < game_state_cols:
        if game_state[head_row, head_col - 1] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_LEFT)

    # Checks for right cell
    if 0 <= head_col + 1 < game_state_cols:
        if game_state[head_row, head_col + 1] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_RIGHT)

    return indices


def _immediate_deaths(game_state: ndarray,
                      snake_head_coord: tuple[int, int]) -> list[BitIndex]:
    indices: list[BitIndex] = []

    head_row, head_col = snake_head_coord

    game_state_rows, game_state_cols = game_state.shape
    lethal_states = (GL_GAME_STATE_WALL, GL_GAME_STATE_SNAKE_BODY)

    # Checks for top cell
    if 0 <= head_row < game_state_rows:
        if game_state[head_row - 1, head_col] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_UP)

    # Checks for bottom cell
    if 0 <= head_row + 1 < game_state_rows:
        if game_state[head_row + 1, head_col] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_DOWN)

    # Checks for left cell
    if 0 <= head_col - 1 < game_state_cols:
        if game_state[head_row, head_col - 1] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_LEFT)

    # Checks for right cell
    if 0 <= head_col + 1 < game_state_cols:
        if game_state[head_row, head_col + 1] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_RIGHT)

    return indices


def convert_game_state_to_bitmap(game_state: ndarray,
                                 snake_head_coord: tuple[int, int]) -> BitMap:
    bitmap: BitMap = BitMap(len(BitIndex))

    # Snake head coordinates are store in the playable area context. However,
    # full board contains an extra outline of walls. Thus, we need to add 1 to
    # the coordinates to have them in the full board frame of reference.
    head_row, head_col = snake_head_coord
    actual_head_coord = (head_row + 1, head_col + 1)

    deaths_idx = _immediate_deaths(game_state, actual_head_coord)
    red_apples_idx = _immediate_red_apples(game_state, actual_head_coord)
    green_apples_idx = _aligned_green_apples(game_state, actual_head_coord)

    for index in chain(deaths_idx, red_apples_idx, green_apples_idx):
        bitmap.set(index)

    return bitmap
