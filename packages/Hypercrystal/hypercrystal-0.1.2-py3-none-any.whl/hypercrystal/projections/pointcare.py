from pygame import Vector2

from ..misc.h2_camera import H2Camera
from .h2_projection import H2Projection
from ..h2_math import H2Transform
from ..h2_math import H2Vector
from ..notation import Resolution
from ..shapes.circle import H2Circle
from ..shapes.projected import ProjectedCircle


# suggestion project lines and equi and horo as arcs
class PointcareModel(H2Projection):
    def __init__(self, camera: H2Camera, display_size: Resolution):
        super().__init__(camera, display_size)

    def project(self, point: H2Vector) -> Vector2:
        view_point: H2Vector = self.world_to_view_space(point)
        projected_point: Vector2 = Vector2(view_point.y / (1 + view_point.x),
                                           view_point.z / (1 + view_point.x))
        return self.projected_to_display_space(projected_point)

    def reproject(self, point: Vector2) -> H2Vector | None:
        projected_point: Vector2 = self.display_to_projected_space(point)
        y, z = projected_point

        if projected_point.length() >= 1:
            return None

        t: float = 2 / (1 - y*y - z*z)
        view_point: H2Vector = H2Vector(t-1, t*y, t*z)
        return self.view_to_world_space(view_point)

    def project_circles(self, circles: list[H2Circle]) -> list[ProjectedCircle]:
        return list(map(self._project_circle, circles))

    def _project_circle(self, circle: H2Circle) -> ProjectedCircle:
        to_camera: H2Transform = H2Transform.AtoB(circle.center, self.camera.position, circle.radius)
        from_camera: H2Transform = to_camera.inverse

        a: Vector2 = self.project(to_camera.apply_on_vector(circle.center))
        b: Vector2 = self.project(from_camera.apply_on_vector(circle.center))
        center: Vector2 = (a + b) * 0.5
        radius: float = (b - center).length()

        return ProjectedCircle(center, radius, circle.key)

    @property
    def disc_present(self) -> bool:
        return True
