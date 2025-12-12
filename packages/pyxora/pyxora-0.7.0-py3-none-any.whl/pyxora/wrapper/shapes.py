from .functions import vector
from abc import ABC, abstractmethod
from math import ceil
from typing import Tuple
import pygame

class Shape(ABC):
    """Abstract base class for all drawable shapes."""

    def __init__(self, pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3, color: str | tuple):
        """
        Initializes the shape with a position and color.

        Args:
            pos (pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3): The position of the shape.
            color (str | tuple): The color of the shape, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        self._pos = vector(*pos)
        self._color = color

    @property
    def position(self) -> pygame.math.Vector2 | pygame.math.Vector3:
        """property to get a copy of the position of the shape."""
        return self._pos.copy()

    @property
    def color(self) -> str | Tuple[int,int,int]:
        """property to get the color of the shape."""
        return self._color

    @property
    @abstractmethod
    def rect(self) -> pygame.Rect | pygame.FRect:
        """
        Returns the bounding rectangle (pygame.Rect or pygame.FRect) based on coordinate types.

        Returns:
            pygame.Rect | pygame.FRect: The bounding rectangle of the shape.
        """
        pass

    @abstractmethod
    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Abstract method to draw the shape on a surface with a given fill and scale.

        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the shape (positive values for outline else is solid).
            scale (int | float): The scale factor for the shape size.
        """
        pass

    def move(self,pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3) -> None:
        """
        Moves the shape by the given offset.

        Args:
            pos (Tuple[int | float, int | float] | Vector2 | Vector3):
                The amount to move the shape by, relative to its current position.
        """
        self._pos.x += pos[0]
        self._pos.y += pos[1]

    def move_at(self,pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3) -> None:
        """
        Moves the shape to a position.

        Args:
            pos (Tuple[int | float, int | float] | Vector2 | Vector3):
                The new position for the shape.
        """
        self._pos.x = pos[0]
        self._pos.y = pos[1]


class Rect(Shape):
    """Represents a rectangle shape."""

    def __init__(
            self,
            pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3,
            size: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3,
            color: str | tuple
    ):
        """
        Initializes the rectangle with position, size, and color.

        Args:
            pos (tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3): The position of the rectangle.
            size (tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3): The size of the rectangle (width, height).
            color (str | tuple): The color of the rectangle, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        super().__init__(pos, color)
        self._size = tuple(size)

    @property
    def size(self) -> Tuple[int | float, int | float]:
        """ The size of the Rect"""
        return self._size

    @property
    def rect(self) -> pygame.Rect | pygame.FRect:
        """
        Returns the bounding rectangle (pygame.Rect or pygame.FRect) based on coordinate types.

        Returns:
            pygame.Rect | pygame.FRect: The bounding rectangle of the shape.
        """
        if all(isinstance(i, int) for i in (self._pos[0], self._pos[1], self._size[0], self._size[1])):
            return pygame.Rect(self._pos, self._size)  # Use pygame.Rect if all values are integers
        return pygame.FRect(self._pos, self._size)  # Use pygame.FRect otherwise

    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Draws the rectangle on the surface with a given fill and scale.

        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the shape (positive values for outline else is solid).
            scale (int | float): The scale factor for the rectangle size.
        """
        # Scale the rectangle and fill value
        rect = self.rect
        color = self.color
        fill *= scale
        rect.width *= scale
        rect.height *= scale
        fill = ceil(fill)  # Ensure fill is an integer

        # Draw the rectangle
        pygame.draw.rect(surf, color, rect, width=fill if fill > 0 else 0)


class Circle(Shape):
    """Represents a circle shape."""

    def __init__(self, pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3, radius: int | float, color: str | tuple):
        """
        Initializes the circle with position, radius, and color.

        Args:
            pos: Tuple[int | float, int | float] | pygame.math.Vector2 | pygame.math.Vector3,
            radius (int | float): The radius of the circle.
            color (str | tuple): The color of the circle, either as a string (e.g., "red") or a tuple (R, G, B).
        """
        super().__init__(pos, color)
        self._radius = radius

    @property
    def radius(self) -> int | float:
        """ The radius of the Circle"""
        return self._radius

    @property
    def rect(self) -> pygame.Rect:
        """
        Returns the bounding rectangle for the circle.

        Returns:
            pygame.Rect: The bounding rectangle that encloses the circle.
        """
        pos = (self._pos[0] - self.radius, self._pos[1] - self.radius)  # Top-left corner of the bounding rect
        size = (self.radius * 2, self.radius * 2)  # Size of the bounding rectangle
        return pygame.Rect(pos, size)

    def draw(self, surf: pygame.Surface, fill: int, scale: int | float) -> None:
        """
        Draws the circle on the surface with a given fill and scale.

        Args:
            surf (pygame.Surface): The surface to draw on.
            fill (int): The fill value for the circle outline (negative for outline, positive for solid).
            scale (int | float): The scale factor for the circle size.
        """
        # Scale the circle and fill value
        pos = self._pos
        fill *= scale
        radius = self.radius * scale  # Scale the radius
        fill = ceil(fill)  # Ensure fill is an integer

        # Draw the circle
        pygame.draw.circle(surf, self.color, pos, radius, width=fill if fill > 0 else 0)
