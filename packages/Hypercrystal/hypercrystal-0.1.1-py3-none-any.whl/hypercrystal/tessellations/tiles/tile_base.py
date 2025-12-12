from ...shapes.polygon import H2Polygon
from ...shapes.circle import H2Circle
from ...shapes.line import H2Line
from ...h2_math.h2_vector import H2Vector
from ...h2_math.h2_transform import H2Transform
from ..tessellation_base import TessellationBase


class TileBase:
    # position, forward is in tesselation space
    def __init__(self, tesselation: TessellationBase, position: H2Vector, rotation: float):
        self.tesselation: TesselationBase = tesselation
        self.tiles: list[TileBase] = []

        self._position: H2Vector = position
        self._rotation: float = rotation

    @property
    def position(self) -> H2Vector:
        return self._position

    @property
    def forward(self) -> H2Vector:
        return self.tile_transform @ H2Vector.FromHyperpolar(0, self.tesselation.inscribed_radius * 0.5)

    @property
    def forward_line(self) -> H2Line:
        return H2Line(self.world_position, self.world_forward)

    @property
    def rotation(self) -> float:
        return self._rotation

    @property
    def world_position(self) -> H2Vector:
        return self.tesselation.model_transform @ self.position

    @property
    def world_forward(self) -> H2Vector:
        return self.tesselation.model_transform @ self.forward

    @property
    def tile_transform(self) -> H2Transform:
        return H2Transform.Anchor(self.position, self.rotation)

    @property
    def model_transform(self) -> H2Transform:
        return self.tile_transform.before(self.tesselation.model_transform)

    # shapes in world space
    @property
    def circle(self) -> H2Circle:
        return H2Circle(self.world_position, self.tesselation.radius)

    @property
    def inscribed_circle(self) -> H2Circle:
        return H2Circle(self.world_position, self.tesselation.inscribed_radius)

    @property
    def polygon(self) -> H2Polygon:
        points: list[H2Vector] = self.tesselation.origin_polygon.points
        points = self.model_transform.apply_on_vectors(points)
        return H2Polygon(points)

    # shapes in tesselation space
    @property
    def tesselation_circle(self) -> H2Circle:
        return H2Circle(self.position, self.tesselation.radius)

    @property
    def tesselation_inscribed_circle(self) -> H2Circle:
        return H2Circle(self.position, self.tesselation.inscribed_radius)

    @property
    def tesselation_polygon(self) -> H2Polygon:
        points: list[H2Vector] = self.tesselation.origin_polygon.points
        points = self.tile_transform.apply_on_vectors(points)
        return H2Polygon(points)

    def __repr__(self):
        return f"({self.position.theta}, {self.position.alpha})"
