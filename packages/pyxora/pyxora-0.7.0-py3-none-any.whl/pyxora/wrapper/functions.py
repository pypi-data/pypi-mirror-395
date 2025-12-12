from typing import Tuple
import pygame

__all__ = ["vector","rect"]

def vector(x: int | float, y: int | float, z: int | float | None = None) -> pygame.math.Vector2 | pygame.math.Vector3:
    """
    Creates a 2D or 3D pygame vector based on the input arguments.

    Args:
        x (int | float): X value of the vector.
        y (int | float): Y value of the vector.
        z (int | float | None): Optional Z value; if provided, returns a 3D vector.

    Returns:
        pygame.math.Vector2 or pygame.math.Vector3: A 2D or 3D vector.

    Examples:
        vector(1, 2) -> pygame.math.Vector2(1, 2)\n
        vector(1, 2, 3) -> pygame.math.Vector3(1, 2, 3)
    """
    if z is not None:
        return pygame.math.Vector3(x, y, z)
    return pygame.math.Vector2(x, y)

def rect(
    pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3,
    size: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3
) -> pygame.Rect | pygame.FRect:
    """
    Returns the bounding rectangle (pygame.Rect or pygame.FRect) based on coordinate types.

    Args:
        pos (Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3): Position of the rectangle.
        size (Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3): Size of the rectangle.

    Returns:
        pygame.Rect | pygame.FRect: The bounding rectangle of the shape.
    """
    if all(isinstance(i, int) for i in (pos[0], pos[1], size[0], size[1])):
        return pygame.Rect(pos, size)  # Use pygame.Rect if all values are integers
    return pygame.FRect(pos,size)  # Use pygame.FRect otherwise
