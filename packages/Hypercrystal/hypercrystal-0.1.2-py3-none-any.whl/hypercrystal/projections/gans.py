import math

from pygame import Vector2

from ..misc.h2_camera import H2Camera
from .h2_projection import H2Projection
from ..h2_math import H2Vector
from ..notation import Resolution
from ..shapes.circle import H2Circle
from ..shapes.projected import ProjectedCircle


class GansModel(H2Projection):
    def __init__(self, camera: H2Camera, display_size: Resolution):
        super().__init__(camera, display_size)

    def project(self, point: H2Vector) -> Vector2:
        view_point: H2Vector = self.world_to_view_space(point)
        projected_point: Vector2 = Vector2(view_point.y, view_point.z)
        return self.projected_to_display_space(projected_point)

    def reproject(self, point: Vector2) -> H2Vector:
        y, z = self.display_to_projected_space(point)
        view_point: H2Vector = H2Vector(
            math.sqrt(1 + y*y + z*z), y, z)
        return self.view_to_world_space(view_point)

    def project_circles(self, circles: list[H2Circle]) -> list[ProjectedCircle]:
        raise Exception("NOT SUPPORTED FOR GANS MODEL")
