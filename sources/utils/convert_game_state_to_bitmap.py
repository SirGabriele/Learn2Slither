from itertools import chain

import numpy as np
from bitmap import BitMap
from numpy import ndarray

from constants import GL_GAME_STATE_GREEN_APPLE, GL_GAME_STATE_RED_APPLE, \
    GL_GAME_STATE_SNAKE_BODY, GL_GAME_STATE_SNAKE_HEAD, \
    GL_GAME_STATE_WALL
from sources.enums.bitindex_enum import BitIndex


def _aligned_green_apples(game_state: ndarray) -> list[BitIndex]:
    indices: list[BitIndex] = []

    # Retrieves the coordinates of the snake's head
    row, col = np.where(game_state == GL_GAME_STATE_SNAKE_HEAD)
    head_y, head_x = row[0], col[0]
    tmp_y, tmp_x = head_y, head_x

    game_state_rows, game_state_cols = game_state.shape

    # Checks for top cells
    while 0 <= tmp_y - 1 < game_state_rows:
        if game_state[tmp_y - 1, tmp_x] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_UP)
        tmp_y -= 1

    tmp_y = head_y

    # Checks for bottom cells
    while 0 <= tmp_y + 1 < game_state_rows:
        if game_state[tmp_y + 1, tmp_x] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_DOWN)
        tmp_y += 1

    tmp_y = head_y

    # Checks for bottom cells
    while 0 <= tmp_y + 1 < game_state_rows:
        if game_state[tmp_y + 1, tmp_x] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_DOWN)
        tmp_y += 1


    tmp_y, tmp_x = head_y, head_x

    # Checks for left cells
    while 0 <= tmp_x - 1 < game_state_cols:
        if game_state[tmp_y, tmp_x - 1] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_LEFT)
        tmp_x -= 1

    tmp_x = head_x

    # Checks for left cells
    while 0 <= tmp_x + 1 < game_state_cols:
        if game_state[tmp_y, tmp_x + 1] == GL_GAME_STATE_GREEN_APPLE:
            indices.append(BitIndex.GREEN_APPLE_RIGHT)
        tmp_x += 1

    return indices


def _immediate_red_apples(game_state: ndarray) -> list[BitIndex]:
    indices: list[BitIndex] = []

    # Retrieves the coordinates of the snake's head
    row, col = np.where(game_state == GL_GAME_STATE_SNAKE_HEAD)
    head_y, head_x = row[0], col[0]

    game_state_rows, game_state_cols = game_state.shape

    # Checks for top cell
    if 0 <= head_y - 1 < game_state_rows:
        if game_state[head_y - 1, head_x] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_UP)

    # Checks for bottom cell
    if 0 <= head_y + 1 < game_state_rows:
        if game_state[head_y + 1, head_x] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_DOWN)

    # Checks for left cell
    if 0 <= head_x - 1 < game_state_cols:
        if game_state[head_y, head_x - 1] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_LEFT)

    # Checks for right cell
    if 0 <= head_x + 1 < game_state_cols:
        if game_state[head_y, head_x + 1] == GL_GAME_STATE_RED_APPLE:
            indices.append(BitIndex.IMMEDIATE_RED_APPLE_RIGHT)

    return indices


def _immediate_deaths(game_state: ndarray) -> list[BitIndex]:
    indices: list[BitIndex] = []

    # Retrieves the coordinates of the snake's head
    row, col = np.where(game_state == GL_GAME_STATE_SNAKE_HEAD)
    # TODO snake.size is 0 here, deconstruction fails
    head_y, head_x = row[0], col[0]

    game_state_rows, game_state_cols = game_state.shape
    lethal_states = (GL_GAME_STATE_WALL, GL_GAME_STATE_SNAKE_BODY)

    # Checks for top cell
    if 0 <= head_y - 1 < game_state_rows:
        if game_state[head_y - 1, head_x] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_UP)

    # Checks for bottom cell
    if 0 <= head_y + 1 < game_state_rows:
        if game_state[head_y + 1, head_x] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_DOWN)

    # Checks for left cell
    if 0 <= head_x - 1 < game_state_cols:
        if game_state[head_y, head_x - 1] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_LEFT)

    # Checks for right cell
    if 0 <= head_x + 1 < game_state_cols:
        if game_state[head_y, head_x + 1] in lethal_states:
            indices.append(BitIndex.IMMEDIATE_DEATH_RIGHT)

    return indices


def convert_game_state_to_bitmap(game_state: ndarray) -> BitMap:
    bitmap: BitMap = BitMap(len(BitIndex))

    deaths_idx = _immediate_deaths(game_state)
    red_apples_idx = _immediate_red_apples(game_state)
    green_apples_idx = _aligned_green_apples(game_state)

    for index in chain(deaths_idx, red_apples_idx, green_apples_idx):
        bitmap.set(index)

    return bitmap
