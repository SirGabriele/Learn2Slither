# Colours
GL_BOARD_BG_COLOUR: str = "dimgray"
GL_GREEN_APPLE_COLOUR: str = "green"
GL_RED_APPLE_COLOUR: str = "red"
GL_SNAKE_HEAD_COLOUR: str = "cornflowerblue"
GL_SNAKE_BODY_COLOUR: str = "lightblue"
GL_SNAKE_TAIL_COLOUR: str = "lightcyan"
GL_SNAKE_EYE_COLOUR: str = "white"
GL_SNAKE_PUPIL_COLOUR: str = "black"
CL_GRID_COLOUR: str = "white"

# Sizes
# 5 <= GL_BOARD_SIZE_IN_CELL <= 30
GL_BOARD_SIZE_IN_CELL: int = 10

# Window
GL_PROGRAM_NAME: str = "Learn2Slither"

# Game state letters
GL_GAME_STATE_WALL: str = 'W'
GL_GAME_STATE_SNAKE_HEAD: str = 'H'
GL_GAME_STATE_SNAKE_BODY: str = 'S'
GL_GAME_STATE_SNAKE_TAIL: str = 'T'
GL_GAME_STATE_FREE_CELL: str = '0'
GL_GAME_STATE_EMPTY: str = ' '
GL_GAME_STATE_GREEN_APPLE: str = 'G'
GL_GAME_STATE_RED_APPLE: str = 'R'

# Game parameters
GL_FRAME_PER_SECOND: int = 60
GL_MAX_STEP: int = 100
# TODO delete
GL_PRINT_TERMINAL: bool = False

# Rewards
GL_REWARD_GREEN_APPLE = 400
GL_REWARD_RED_APPLE = -150
GL_REWARD_EMPTY_SPACE = -10
GL_REWARD_DEATH = -1000