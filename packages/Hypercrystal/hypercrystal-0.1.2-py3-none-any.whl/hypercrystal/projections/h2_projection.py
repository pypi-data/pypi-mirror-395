from pygame import Vector2

from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from ..misc.h2_camera import H2Camera
from ..notation import Resolution
from ..shapes.projected import ProjectedCircle, ProjectedLine, ProjectedPolygon
from ..shapes.circle import H2Circle
from ..shapes.line import H2Line
from ..shapes.polygon import H2Polygon

class H2Projection:
    def __init__(self, camera: H2Camera, display_size: Resolution, cull_range=50):
        self._display_size: Resolution = (1, 1)
        self.scale: int = 0
        self.center: Vector2 = Vector2()
        self.display_size: Resolution = display_size

        self.camera: H2Camera = camera
        self.view_transform: H2Transform = camera.transform
        self.inverse_view_transform = self.view_transform.inverse
        self.scalar: float = self.scale * camera.zoom

        self.cull_range: float = cull_range

    @property
    def display_size(self) -> Resolution:
        return self._display_size

    @display_size.setter
    def display_size(self, display_size: Resolution) -> None:
        self._display_size = display_size
        self.scale: int = min(self.display_size) // 2
        self.center: Vector2 = Vector2(
            self.display_size[0] // 2, self.display_size[1] // 2)

    def _update_camera_consequences(self) -> None:
        self.view_transform = self.camera.transform
        self.inverse_view_transform = self.view_transform.inverse
        self.scalar: float = self.scale * self.camera.zoom

    def update(self) -> None:
        self._update_camera_consequences()

    def projected_to_display_space(self, point: Vector2) -> Vector2:
        return (point * self.scalar) + self.center

    def display_to_projected_space(self, point: Vector2) -> Vector2:
        return (point - self.center) / self.scalar

    def world_to_view_space(self, point: H2Vector) -> H2Vector:
        return self.view_transform.apply_on_vector(point)

    def view_to_world_space(self, point: H2Vector) -> H2Vector:
        return self.inverse_view_transform.apply_on_vector(point)

    def project(self, point: H2Vector) -> Vector2:
        raise Exception("Not implemented")

    def reproject(self, point: Vector2) -> H2Vector:
        raise Exception("Not implemented")

    def project_points(self, points: list[H2Vector]) -> list[Vector2]:
        return list(map(self.project, points))

    def project_circles(self, circles: list[H2Circle]) -> list[ProjectedCircle]:
        raise Exception("Not implemented")

    def project_lines(self, lines: list[H2Line]) -> list[ProjectedLine]:
        return list(map(lambda x: ProjectedLine(
            self.project(x.a), self.project(x.b), x.key
        ), lines))

    def project_polygons(self, polygons: list[H2Polygon]) -> list[ProjectedPolygon]:
        return list(map(lambda x: ProjectedPolygon(
            self.project_points(x.points), x.key
        ), polygons))

    def cull_and_project_circles(self, circles: list[H2Circle]) -> list[ProjectedCircle]:
        return self.project_circles(filter(self.to_not_cull_circle, circles))

    def cull_and_project_lines(self, lines: list[H2Line], circle_hulls: list[H2Circle])\
            -> list[ProjectedLine]:
        assert len(lines) == len(circle_hulls)

        projected: list[ProjectedLine] = []

        for line, hull in zip(lines, circle_hulls):
            if self.to_cull_circle(hull):
                continue

            projected.append(ProjectedLine(self.project(line.a), self.project(line.b), line.key))

        return projected

    def cull_and_project_polygons(self, polygons: list[H2Polygon], circle_hulls: list[H2Circle])\
            -> list[ProjectedPolygon]:
        assert len(polygons) == len(circle_hulls)

        projected: list[ProjectedPolygon] = []

        for polygon, hull in zip(polygons, circle_hulls):
            if self.to_cull_circle(hull):
                continue

            projected.append(ProjectedPolygon(
                self.project_points(polygon.points), polygon.key
            ))

        return projected

    def cull_circles(self, circles: list[H2Circle]) -> list[H2Circle]:
        return list(filter(self.to_not_cull_circle, circles))

    def to_not_cull_circle(self, circle: H2Circle) -> bool:
        return not self.to_cull_circle(circle)

    def to_cull_circle(self, circle: H2Circle) -> bool:
        view_point: H2Vector = self.world_to_view_space(circle.center)
        closest_presence: float = view_point.alpha - circle.radius
        return closest_presence > self.cull_range

    @property
    def disc(self) -> ProjectedCircle:
        return ProjectedCircle(self.center, self.scalar)

    @property
    def disc_present(self) -> bool:
        return False

    @property
    def cull_circle(self) -> H2Circle:
        return H2Circle(self.camera.position, self.cull_range)
