import math

from ..shapes.circle import H2Circle
from ..shapes.polygon import H2Polygon
from ..shapes.line import H2Line
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from ..h2_math.low_functions import c_from_angles


class TessellationBase:
    def __init__(self, p: int, q: int, position: H2Vector, rotation: float) -> None:
        self._p: int = p
        self._q: int = q

        if not self._tesselation_validity_check():
            raise ValueError(f"Tesselation [{p}, {q}] is not a valid hyperbolic tesselation.")

        self._alpha = math.tau / self.p
        self._beta = math.tau / self.q

        half_alpha: float = self.alpha * 0.5
        half_beta: float = self.beta * 0.5
        half_pi: float = math.pi * 0.5

        self._radius: float = c_from_angles(half_alpha, half_beta, half_pi)
        self._sidelength: float = 2 * c_from_angles(half_beta, half_pi, half_alpha)
        self._inscribed_radius: float = c_from_angles(half_alpha, half_pi, half_beta)

        self.position: H2Vector = position
        self.rotation: float = rotation

    @property
    def forward(self) -> H2Vector:
        return self.model_transform @ H2Vector.FromHyperpolar(0, self.inscribed_radius * 0.5)

    @property
    def forward_line(self) -> H2Line:
        return H2Line(self.position, self.forward)

    @property
    def model_transform(self) -> H2Transform:
        return H2Transform.Anchor(self.position, self.rotation)

    @property
    def p(self) -> int:
        return self._p

    @property
    def q(self) -> int:
        return self._q

    @property
    def alpha(self) -> float:
        return self._alpha

    @property
    def beta(self) -> float:
        return self._beta

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def sidelength(self) -> float:
        return self._sidelength

    @property
    def inscribed_radius(self) -> float:
        return self._inscribed_radius

    @classmethod
    def check_validity(cls, p: int, q: int) -> bool:
        return max(0, p-2) * max(0, q-2) > 4

    def _tesselation_validity_check(self) -> bool:
        return TessellationBase.check_validity(self.p, self.q)

    # shapes in world space
    @property
    def circle(self) -> H2Circle:
        return H2Circle(self.position, self.radius)

    @property
    def inscribed_circle(self) -> H2Circle:
        return H2Circle(self.position, self.inscribed_radius)

    @property
    def polygon(self) -> H2Polygon:
        points: list[H2Vector] = self.origin_polygon.points
        points = self.model_transform.apply_on_vectors(points)
        return H2Polygon(points)

    # shapes centered at origin, direction is set to y+
    @property
    def origin_circle(self) -> H2Circle:
        return H2Circle(H2Vector(), self.radius)

    @property
    def origin_inscribed_circle(self) -> H2Circle:
        return H2Circle(H2Vector(), self.inscribed_radius)

    @property
    def origin_polygon(self) -> H2Polygon:
        rotor: H2Transform = H2Transform.Plane("yz", self.alpha)
        points: list[H2Vector] = [
            H2Vector.FromHyperpolar(-0.5 * self.alpha, self.radius)
        ]

        for _ in range(self.p - 1):
            points.append(rotor @ points[-1])

        return H2Polygon(points)
