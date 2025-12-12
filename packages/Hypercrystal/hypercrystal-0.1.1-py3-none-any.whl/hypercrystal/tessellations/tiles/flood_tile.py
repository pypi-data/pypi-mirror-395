from ...h2_math.h2_vector import H2Vector
from ..tessellation_base import TessellationBase
from .tile_base import TileBase


class FloodTile(TileBase):
    # position is in tesselation space
    def __init__(self, tesselation: TessellationBase, position: H2Vector, rotation: float):
        super().__init__(tesselation, position, rotation)
