from .h2_transform import H2Transform
from .h2_vector import H2Vector
from ..notation import H2RayHit
from ..shapes.line import H2Line
from ..shapes.polygon import H2Polygon
from ..shapes.circle import H2Circle
from .low_functions import pythagorean_get_a


type CASTABLE_SHAPE = H2Line | H2Circle | H2Polygon | H2Ray


class H2Ray:
    def __init__(self, position: H2Vector, direction: H2Vector):
        self.position: H2Vector = position
        self.direction: H2Vector = direction

    def sample(self, d: float) -> H2Vector:
        return H2Transform.AtoB(self.position, self.direction, d) @ self.position

    @property
    def line(self) -> H2Line:
        return H2Line(self.position.clone, self.direction.clone)

    def get_line(self, length: float = 1) -> H2Line:
        return H2Line(self.position.clone, self.sample(length))

    def duel(self, other: 'H2Ray') -> H2RayHit:
        transform: H2Transform = H2Transform.LineToXY(self.position, self.direction)
        a: H2Vector = transform @ other.position
        b: H2Vector = transform @ other.direction

        if a.z == 0 and a.y == 0:
            return 0

        if a.z == 0 and b.z == 0:
            if a.y < 0 and b.y > a.y:
                return 0

            if a.y > 0 and b.y < a.y:
                return 0

            return None

        if 0 < a.z < b.z:
            return None
        if 0 > a.z > b.z:
            return None

        a_projected: H2Vector = H2Vector(1, a.y / a.x, a.z / a.x)
        b_projected: H2Vector = H2Vector(1, b.y / b.x, b.z / b.x)
        line_direction: H2Vector = b_projected - a_projected

        t: float = -a_projected.z / line_direction.z

        final_y: float = a_projected.y + line_direction.y * t
        if final_y < 0:
            return None

        if final_y >= 1:
            return None

        reprojected: H2Vector = H2Vector(1, final_y, 0).normalized

        return reprojected.alpha

    def __matmul__(self, other: 'H2Ray') -> H2RayHit:
        return self.duel(other)

    def cast_against(self, shape: CASTABLE_SHAPE) -> H2RayHit:
        if type(shape) == H2Line:
            return self.cast_against_line(line=shape)
        elif type(shape) == H2Circle:
            return self.cast_against_circle(circle=shape)
        elif type(shape) == H2Polygon:
            return self.cast_against_polygon(polygon=shape)
        elif type(shape) == H2Ray:
            return self.duel(other=shape)

        raise TypeError(f"Unsupported shape type: {type(shape)}")

    def cast_against_line(self, line: H2Line) -> H2RayHit:
        transform: H2Transform = H2Transform.LineToXY(self.position, self.direction)
        a_: H2Vector = transform @ line.a
        b_: H2Vector = transform @ line.b

        if (a_.z > 0 and b_.z > 0) or (a_.z < 0 and b_.z < 0):
            return None

        if a_.z == 0 and b_.z == 0:
            if self._sign(a_.y) != self._sign(b_.y):
                return 0

            if self._sign(a_.y) == -1:
                return None

            return min(a_.alpha, b_.alpha)

        if a_.z == 0:
            if a_.y < 0:
                return None

            return a_.alpha

        if b_.z == 0:
            if b_.y < 0:
                return None

            return b_.alpha

        a_projected: H2Vector = H2Vector(1, a_.y / a_.x, a_.z / a_.x)
        b_projected: H2Vector = H2Vector(1, b_.y / b_.x, b_.z / b_.x)
        line_direction: H2Vector = b_projected - a_projected
        t: float = -a_projected.z / line_direction.z

        final_y: float = a_projected.y + line_direction.y * t
        if final_y < 0:
            return None

        reprojected: H2Vector = H2Vector(1, final_y, 0).normalized

        return reprojected.alpha

    def cast_against_circle(self, circle: H2Circle) -> H2RayHit:
        transform: H2Transform = H2Transform.LineToXZ(self.position, self.direction)
        a: H2Vector = transform @ circle.center
        gamma, beta = a.hyperbolical
        gamma = abs(gamma)

        if gamma > circle.radius:
            return None
        if gamma == circle.radius:
            if beta >= 0:
                return beta
            return None

        offset: float = pythagorean_get_a(gamma, circle.radius)
        d1, d2 = beta + offset, beta - offset

        if d1 < 0 and d2 < 0:
            return None
        if d2 < 0:
            return d1

        return d2

    def cast_against_polygon(self, polygon: H2Polygon) -> H2RayHit:
        t: H2RayHit = None

        segments_n: int = len(polygon.points)
        if polygon.is_line:
            segments_n -= 1

        for i in range(segments_n):
            new_t = self.cast_against_line(H2Line(
                polygon.points[i], polygon.points[(i + 1) % len(polygon.points)]))

            if new_t is None:
                continue

            if t is None:
                t = new_t

            t = min(t, new_t)

        return t

    @staticmethod
    def _sign(x: float) -> float:
        return 1 if x >= 0 else -1
