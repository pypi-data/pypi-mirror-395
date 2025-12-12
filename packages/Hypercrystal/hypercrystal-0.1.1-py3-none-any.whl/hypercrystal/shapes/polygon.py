from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform

class H2Polygon:
    def __init__(self, points: list[H2Vector], key=None, is_line: bool=False) -> None:
        self.points: list[H2Vector] = points
        self.key = key
        self.is_line: bool=is_line

    @property
    def circle_hull(self) -> 'H2Circle':
        from .circle import H2Circle
        center, radius = H2Vector.GetCircleHull(self.points)
        return H2Circle(center, radius, self.key)

    def subdivide(self, samples=3) -> 'H2Polygon':
        assert samples >= 0
        points: list[H2Vector] = []

        iter_amount: int = len(self.points)
        if self.is_line:
            iter_amount -= 1

        for i in range(iter_amount):
            points.append(self.points[i].clone)

            rotor: H2Transform = H2Transform.LerpAB(
                self.points[i], self.points[(i+1) % len(self.points)], 1 / (samples + 1))

            for t in range(samples):
                points.append(
                    rotor @ points[-1])

        if self.is_line:
            points.append(self.points[-1].clone)

        return H2Polygon(points, self.key, self.is_line)
