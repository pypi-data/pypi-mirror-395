from abc import ABC, abstractmethod


class ShapeABC(ABC):
    @abstractmethod
    def get_area(self):
        """Get the area of this 2D Shape"""
