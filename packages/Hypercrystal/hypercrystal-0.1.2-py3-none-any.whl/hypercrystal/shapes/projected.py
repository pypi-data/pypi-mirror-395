from pygame import Vector2


class ProjectedCircle:
    def __init__(self, center: Vector2, radius: float, key=None) -> None:
        self.center: Vector2 = center
        self.radius: float = radius
        self.key = key

class ProjectedLine:
    def __init__(self, a: Vector2, b: Vector2, key=None) -> None:
        self.a: Vector2 = a
        self.b: Vector2 = b
        self.key = key

class ProjectedPolygon:
    def __init__(self, points: list[Vector2], key=None) -> None:
        self.points: list[Vector2] = points
        self.key = key
