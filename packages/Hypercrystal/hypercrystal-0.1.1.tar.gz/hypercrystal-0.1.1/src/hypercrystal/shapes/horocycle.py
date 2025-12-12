from .circle import H2Circle
from .polygon import H2Polygon
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform


class Horocycle:
    def __init__(self, angle_to_horizon: float, anchor: H2Vector, bounds: tuple[float, float]=None,
                 key=None):
        if bounds is None:
            bounds = (-1, 1)

        self.angle_to_horizon: float = angle_to_horizon
        self.anchor: H2Vector = anchor
        self.bounds: tuple[float, float] = bounds
        self.key = key

    def _t_to_x(self, t: float) -> float:
        return self.bounds[0] + (t * self.bounds_size)

    @property
    def bounds_size(self) -> float:
        return abs(self.bounds[0] - self.bounds[1])

    def sample(self, t: float) -> H2Vector:
        return self.sample_directly(self._t_to_x(t))

    def sample_directly(self, x: float) -> H2Vector:
        sample: H2Vector = self._sample_unit_horocycle(x)
        return self._unit_model_transform.apply_on_vector(sample)

    @staticmethod
    def _sample_unit_horocycle(x: float) -> H2Vector:
        return H2Vector(
            1 + ((x * x) * 0.5),
            (x * x) * 0.5,
            -x)

    @property
    def _unit_model_transform(self) -> H2Transform:
        return H2Transform.Anchor(self.anchor, self.angle_to_horizon)

    def approximate(self, samples: int=10) -> H2Polygon:
        assert samples >= 2

        transform: H2Transform = self._unit_model_transform

        points: list[H2Vector] = [
            transform @ self._sample_unit_horocycle(self._t_to_x(i / (samples - 1)))
            for i in range(samples)
        ]

        return H2Polygon(points, self.key, is_line=True)

    @property
    def circle_hull(self) -> H2Circle:
        center, radius = H2Vector.GetCircleHull([
            self.sample(0),
            self.sample(0.5),
            self.sample(1)
        ])
        return H2Circle(center, radius, self.key)
