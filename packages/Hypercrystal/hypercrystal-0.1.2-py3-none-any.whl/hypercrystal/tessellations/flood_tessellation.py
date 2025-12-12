import math

from .tessellation_base import TessellationBase
from .tiles.flood_tile import FloodTile
from ..h2_math.h2_vector import H2Vector
from ..misc.h2_walker import H2Walker
from ..shapes.circle import H2Circle
from ..shapes.polygon import H2Polygon
from ..shapes.line import H2Line
from ..misc.h2_lookup import H2Lookup


class FloodTessellation(TessellationBase):
    LOG_PROGRESS:bool = False

    def __init__(self, p: int, q: int, position: H2Vector=None, rotation: float=0, layers: int=3):
        if position is None:
            position = H2Vector()

        super().__init__(p, q, position, rotation)

        self._layers = 0
        self._root_tile: FloodTile = None
        self.tiles: list[FloodTile] = []
        self.tile_layers: dict[int, list[FloodTile]] = {}
        self.tile_lookup: H2Lookup[list[FloodTile]] = H2Lookup()

        for _ in range(layers):
            self.generate_layer()

    @property
    def layers(self) -> int:
        return self._layers

    @property
    def tile_count(self) -> int:
        return len(self.tiles)

    @property
    def root_tile(self) -> FloodTile:
        return self._root_tile

    @property
    def tile_polygons(self) -> list[H2Polygon]:
        return list(map(lambda x: x.polygon, self.tiles))

    @property
    def tile_inscribed_circles(self) -> list[H2Circle]:
        return list(map(lambda x: x.inscribed_circle, self.tiles))

    @property
    def tile_circles(self) -> list[H2Circle]:
        return list(map(lambda x: x.circle, self.tiles))

    @property
    def tile_forward_lines(self) -> list[H2Line]:
        return list(map(lambda x: x.forward_line, self.tiles))

    def generate_layer(self) -> None:
        if self.layers == 0:
            self._create_root()
        else:
            self._flood_last_layer()

        self._layers += 1

        if self.LOG_PROGRESS:
            print(f"FloodTesselation [{self.p}, {self.q}] - layer {self.layers} done")

    def _create_root(self) -> None:
        self._root_tile = FloodTile(self, H2Vector(), 0)
        self.tiles.append(self.root_tile)
        self.tile_layers[0] = [self.root_tile]
        self.tile_lookup[self.root_tile.position] = [self.root_tile]

    def _flood_last_layer(self):
        self.tile_layers[self.layers] = []

        for tile in self.tile_layers[self.layers - 1]:
            self._flood_tile(tile, True if self.layers == 1 else False)

    def _flood_tile(self, tile: FloodTile, second_layer: bool) -> None:
        walker: H2Walker = H2Walker(tile.position, tile.forward)

        directions_to_check: int = self.p - 1
        if second_layer:
            directions_to_check += 1

        for i in range(directions_to_check):
            walker.rotate(self.alpha)

            explorer: H2Walker = walker.clone
            explorer.move(self.inscribed_radius * 2)

            if self._check_tile_existence(explorer.position):
                continue

            new_tile: FloodTile = FloodTile(self, explorer.position, explorer.rotation + math.pi)
            new_tile.tiles.append(tile)

            self.tiles.append(new_tile)
            self.tile_layers[self.layers].append(new_tile)
            self.tile_lookup.get(new_tile.position, []).append(new_tile)
            tile.tiles.append(new_tile)

        if second_layer:
            self.root_tile.tiles = self.root_tile.tiles[-1:] + self.root_tile.tiles[:-1]

    def _check_collision_with_tiles(self, position: H2Vector, tiles: list[FloodTile]) -> bool:
        for tile in tiles:
            if position.distance_to(tile.position) < self.inscribed_radius:
                return True

        return False

    def _check_tile_existence(self, position: H2Vector) -> bool:
        tile_lists_around = self.tile_lookup.around(position, distance=1)
        #tile_lists_around = [self.tiles]

        for tile_list in tile_lists_around:
            if self._check_collision_with_tiles(position, tile_list):
                return True

        return False
