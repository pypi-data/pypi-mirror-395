from .polygon import H2Polygon
from .circle import H2Circle
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from ..h2_math.high_functions import angleAtB, is_clockwise


class H2Arc:
    def __init__(self, center: H2Vector, anchor: H2Vector, length: float, key=None) -> None:
        self.center: H2Vector = center
        self.anchor: H2Vector = anchor
        self.length: float = max(-H2Transform.TAU, min(H2Transform.TAU, length))
        self.key = key

    @classmethod
    def ThreePoint(cls,center: H2Vector, anchor: H2Vector, hook: H2Vector, key=None) -> 'H2Arc':
        length: float = angleAtB(hook, center, anchor)

        if not is_clockwise(center, anchor, hook):
            length *= -1

        return H2Arc(center, anchor, length, key)

    def reverse(self) -> None:
        self.anchor = self.hook
        self.length *= -1

    @property
    def hook(self) -> H2Vector:
        rotor: H2Transform = H2Transform.Around(self.center, self.length)
        return rotor @ self.anchor

    @property
    def radius(self) -> float:
        return self.center.distance_to(self.anchor)

    @property
    def circle(self) -> H2Circle:
        return H2Circle(self.center, self.radius, self.key)

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    def sample(self, t: float) -> H2Vector:
        transform: H2Transform = H2Transform.Around(self.center, self.length * t)
        return transform @ self.anchor

    def approximate(self, samples: int=10) -> H2Polygon:
        assert samples >=2

        points: list[H2Vector] = [self.anchor.clone]
        theta: float = self.length / (samples-1)
        rotor: H2Transform = H2Transform.Around(self.center, theta)

        for _ in range(samples-1):
            points.append(rotor.apply_on_vector(points[-1]))

        return H2Polygon(points, self.key, is_line=True)

    @property
    def circle_hull(self) -> H2Circle:
        return self.circle
