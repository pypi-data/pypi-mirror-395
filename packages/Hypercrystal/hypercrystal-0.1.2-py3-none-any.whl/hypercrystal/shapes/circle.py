from .polygon import H2Polygon
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from math import sinh, cosh


class H2Circle:
    def __init__(self, center: H2Vector, radius: float, key=None) -> None:
        self.center: H2Vector = center
        self.radius: float = radius
        self.key = key

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    @property
    def circumference(self) -> float:
        return H2Transform.TAU * sinh(self.radius)

    @property
    def area(self) -> float:
        return H2Transform.TAU * (cosh(self.radius) - 1)

    def approximate(self, samples: int=10) -> H2Polygon:
        assert samples >=2

        offset: H2Transform = H2Transform.AtoB(self.center, H2Vector(), self.radius)
        points: list[H2Vector] = [offset.apply_on_vector(self.center)]

        theta: float = H2Transform.TAU / samples
        rotor: H2Transform = H2Transform.Around(self.center, theta)

        for _ in range(samples-1):
            points.append(rotor.apply_on_vector(points[-1]))

        return H2Polygon(points, self.key)
