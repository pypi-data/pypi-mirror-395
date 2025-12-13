from dataclasses import dataclass

from example.models.shape_abc import ShapeABC


@dataclass
class Square(ShapeABC):
    length: float

    def get_area(self):
        return self.length**2
