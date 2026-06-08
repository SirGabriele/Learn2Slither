from constants import GL_REWARD_EMPTY_SPACE


def process_step_limit(step_limit: int, reward: int) -> int:
    # If the snake moved to an empty tile, the counter is increased by one.
    # When step_limit reaches a certain amount, the session will be counted as
    # finished because the snake is going in circles.
    if reward == GL_REWARD_EMPTY_SPACE:
        return step_limit + 1
    else:
        return 0