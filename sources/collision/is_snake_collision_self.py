def is_snake_collision_self(body_segments: list[tuple[int, int]],
                            next_snake_head_coord: tuple[int, int]) -> bool:
    """Checks if the snake collides with any segment of its own body apart
    from its tail. We do not check collision with the tail because it moves
    exactly as the head moves, which makes them impossible to collide."""
    return (len(body_segments) is not None and next_snake_head_coord in
            body_segments)
