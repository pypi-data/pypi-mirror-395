from .line import H2Line
from .polygon import H2Polygon
from .circle import H2Circle
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform


class Hypercycle:
    def __init__(self, line: H2Line, distance: float, bounds: tuple[float, float], key=None) -> None:
        self.line: H2Line = line
        self.distance: float = distance
        self.bounds: tuple[float, float] = bounds
        self.key = key

    @property
    def bounds_size(self) -> float:
        return abs(self.bounds[0] - self.bounds[1])

    @property
    def bounds_length(self) -> float:
        return self.line.length * self.bounds_size

    @property
    def start_on_line(self) -> H2Vector:
        return self.line.sample(min(self.bounds))

    @property
    def end_on_line(self) -> H2Vector:
        return self.line.sample(max(self.bounds))

    def approximate(self, samples: int=10) -> H2Polygon:
        assert samples >=2

        start: H2Vector = self.start_on_line
        end: H2Vector = self.end_on_line
        step_size: float = self.bounds_length / (samples - 1)

        transform: H2Transform = H2Transform.LineToXZ(start, end).inverse

        points: list[H2Vector] = [
            H2Vector.FromHyperbolical(self.distance, step_size * i)
            for i in range(samples)
        ]

        points = list(map(transform.apply_on_vector, points))

        return H2Polygon(points, self.key, is_line=True)

    def sample(self, t: float) -> H2Vector:
        transform: H2Transform = H2Transform.LineToXZ(self.start_on_line, self.end_on_line).inverse
        point: H2Vector = H2Vector.FromHyperbolical(self.distance, t * self.bounds_length)
        return transform.apply_on_vector(point)

    @property
    def circle_hull(self) -> H2Circle:
        center, radius = H2Vector.GetCircleHull([
            self.sample(0),
            self.sample(0.5),
            self.sample(1)
        ])
        return H2Circle(center, radius, self.key)
