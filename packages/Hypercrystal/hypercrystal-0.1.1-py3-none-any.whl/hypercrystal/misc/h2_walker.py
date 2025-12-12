from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from ..h2_math.h2_ray import H2Ray


class H2Walker:
    def __init__(self, position: H2Vector, forward: H2Vector):
        self.position: H2Vector = position
        self.forward: H2Vector = forward

    @property
    def rotation(self) -> float:
        forward_: H2Vector = H2Transform.StraightToOrigin(self.position) @ self.forward
        return forward_.theta

    @property
    def ray(self) -> H2Ray:
        return H2Ray(self.position, self.forward)

    @property
    def anchor_transform(self) -> H2Transform:
        return H2Transform.LineToXY(self.position, self.forward).inverse

    @property
    def anchor_inverse_transform(self) -> H2Transform:
        return H2Transform.LineToXY(self.position, self.forward)

    @property
    def clone(self) -> 'H2Walker':
        return H2Walker(self.position.clone, self.forward.clone)

    def _apply_transform(self, transform: H2Transform, ignore_position: bool = False) -> None:
        if not ignore_position:
            self.position = transform @ self.position

        self.forward = transform @ self.forward

    def rotate(self, angle: float) -> None:
        transform: H2Transform = H2Transform.Around(self.position, angle)
        self._apply_transform(transform, True)

    def move(self, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, self.forward, distance)
        self._apply_transform(transform)
