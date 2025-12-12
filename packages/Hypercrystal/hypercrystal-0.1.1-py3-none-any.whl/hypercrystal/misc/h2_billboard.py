import math

import pygame.transform

from ..notation import Resolution
from ..h2_math.h2_vector import H2Vector
from ..h2_math.h2_transform import H2Transform
from ..projections.h2_projection import H2Projection
from pygame import Vector2, Surface


class H2Billboard:
    def __init__(self, center: H2Vector, top_center: H2Vector):
        self.center: H2Vector = center
        self.top_center: H2Vector = top_center
        self.right_center: H2Vector = H2Transform.Around(self.center, -H2Transform.HALF_PI) @ self.top_center

        self.projected_center: Vector2 = None
        self.projected_top_center: Vector2 = None
        self.projected_right_center: Vector2 = None
        self.projected_y_size: int = 1
        self.projected_x_size: int = 1
        self.projected_rotation: float = 0

    def update(self, projection: H2Projection) -> None:
        self.projected_center = projection.project(self.center)
        self.projected_top_center = projection.project(self.top_center)
        self.projected_right_center = projection.project(self.right_center)

        direction_up: Vector2 = self.projected_top_center - self.projected_center
        orthogonal: Vector2 = Vector2(direction_up.y, -direction_up.x).normalize()
        direction_right: Vector2 = self.projected_right_center - self.projected_center

        self.projected_y_size = int(direction_up.length() * 2)
        self.projected_x_size = abs(int(direction_right.dot(orthogonal) * 2))
        self.projected_rotation = -math.degrees(math.atan2(direction_up.y, direction_up.x)) - 90

    def blit(self, image: Surface, target: Surface) -> None:
        if self.projected_center is None:
            raise Exception("Please call .update(projection: H2Projection) each frame before blitting")

        x_scale: int = int((image.width / image.height) * self.projected_x_size)
        resized_resolution: Resolution = (x_scale, self.projected_y_size)
        resized_image: Surface = pygame.transform.scale(image, resized_resolution)
        resized_image.set_colorkey((0, 0, 0))
        rotated_image: Surface = pygame.transform.rotate(resized_image, self.projected_rotation)

        blit_resolution: Resolution = rotated_image.get_size()

        blit_position: Vector2 = Vector2(
            self.projected_center[0] - blit_resolution[0]*0.5,
            self.projected_center[1] - blit_resolution[1]*0.5
        )

        target.blit(rotated_image, blit_position)
