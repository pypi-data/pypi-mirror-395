from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform


class H2Camera:
    def __init__(self, position: H2Vector, up: H2Vector, zoom: float=1):
        self.position: H2Vector = position
        self.up: H2Vector = up
        self.right: H2Vector = H2Transform.Around(self.position, -H2Transform.HALF_PI) @ self.up

        # zoom is ignored for bounded region projections
        self.zoom: float = zoom
    @property
    def transform(self) -> H2Transform:
        return H2Transform.LineToXY(self.position, self.right)

    def _apply_transform(self, transform: H2Transform, ignore_position: bool=False) -> None:
        if not ignore_position:
            self.position = transform @ self.position

        self.up = transform @ self.up
        self.right = transform @ self.right

    def move_right(self, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, self.right, distance)
        self._apply_transform(transform)

    def move_left(self, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, self.right, -distance)
        self._apply_transform(transform)

    def move_up(self, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, self.up, distance)
        self._apply_transform(transform)

    def move_down(self, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, self.up, -distance)
        self._apply_transform(transform)

    def rotate(self, angle: float) -> None:
        transform: H2Transform = H2Transform.Around(self.position, angle)
        self._apply_transform(transform, True)

    def move(self, direction: H2Vector, distance: float) -> None:
        transform: H2Transform = H2Transform.AtoB(self.position, direction, distance)
        self._apply_transform(transform)

    def move_by_theta(self, theta: float, distance: float) -> None:
        rotor: H2Transform = H2Transform.Around(self.position, theta)
        direction: H2Vector = rotor.apply_on_vector(self.right)
        self.move(direction, distance)
