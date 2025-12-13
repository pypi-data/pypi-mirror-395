import math
from dataclasses import dataclass

from example.models.shape_abc import ShapeABC


@dataclass
class Circle(ShapeABC):
    radius: float

    def get_area(self):
        return math.pi * self.radius**2
