from dataclasses import dataclass

from example.models.shape_abc import ShapeABC


@dataclass
class Rectangle(ShapeABC):
    length: float
    height: float

    def get_area(self):
        return self.length * self.height
