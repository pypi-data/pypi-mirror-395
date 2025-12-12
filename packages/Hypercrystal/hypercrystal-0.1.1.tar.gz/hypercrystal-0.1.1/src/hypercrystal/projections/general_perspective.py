import math

from pygame import Vector2

from ..misc.h2_camera import H2Camera
from .h2_projection import H2Projection
from ..h2_math import H2Vector
from ..notation import Resolution
from ..shapes.circle import H2Circle
from ..shapes.projected import ProjectedCircle


class GeneralPerspectiveModel(H2Projection):
    def __init__(self, camera: H2Camera, display_size: Resolution, perspective_distance=2):
        super().__init__(camera, display_size)
        self.perspective_distance = perspective_distance

    def project(self, point: H2Vector) -> Vector2:
        view_point: H2Vector = self.world_to_view_space(point)
        projected_point: Vector2 = Vector2(
            view_point.y / (self.perspective_distance + view_point.x),
            view_point.z / (self.perspective_distance + view_point.x))
        return self.projected_to_display_space(projected_point)

    def reproject(self, point: Vector2) -> H2Vector | None:
        projected_point: Vector2 = self.display_to_projected_space(point)
        y, z = projected_point

        if projected_point.length() >= 1:
            return None

        o: float = -self.perspective_distance
        A: float = 1 - y * y - z * z
        if A <= 0:
            return None

        D: float = o * o - ((o * o - 1) * A)
        if D < 0:
            return None

        t = (-o + math.sqrt(D)) / A
        view_point: H2Vector = H2Vector(o + t, t * y, t * z)
        return self.view_to_world_space(view_point)

    def project_circles(self, circles: list[H2Circle]) -> list[ProjectedCircle]:
        raise Exception("NOT SUPPORTED FOR GENERAL PERSPECTIVE MODEL")

    @property
    def disc_present(self) -> bool:
        return True
