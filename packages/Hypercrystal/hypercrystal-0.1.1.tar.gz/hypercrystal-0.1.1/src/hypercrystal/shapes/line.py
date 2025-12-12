from .polygon import H2Polygon
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from .circle import H2Circle

class H2Line:
    def __init__(self, a: H2Vector, b: H2Vector, key=None) -> None:
        self.a: H2Vector = a
        self.b: H2Vector = b
        self.key = key

    @property
    def length(self) -> float:
        return self.a.distance_to(self.b)

    def approximate(self, samples: int=10) -> H2Polygon:
        assert samples >= 2

        points: list[H2Vector] = [self.a.clone]
        t: float = 1 / (samples - 1)
        movement: H2Transform = H2Transform.LerpAB(self.a, self.b, t)

        for _ in range(samples-1):
            points.append(movement.apply_on_vector(points[-1]))

        return H2Polygon(points, self.key, is_line=True)

    def sample(self, t: float) -> H2Vector:
        transform: H2Transform = H2Transform.LerpAB(self.a, self.b, t)
        return transform @ self.a

    @property
    def circle_hull(self) -> H2Circle:
        return H2Circle(self.a @ self.b, self.length / 2, self.key)
