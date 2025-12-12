import math
from typing import Generic, TypeVar
from ..h2_math.h2_vector import H2Vector
from ..shapes.polygon import H2Polygon
from ..shapes.line import H2Line
from ..shapes.circle import H2Circle
from ..shapes.arc import H2Arc


K = TypeVar("K")

# HASH CODE EXPLANATION
# First value(thetint) is angle as discrete value, second(alphint) distance from origin
# For alpha, +1 for each DOUBLING_CONSTANT distance covered
# For theta, range for it is always 2**alphint
HASH_CODE: type = tuple[int, int]


# THIS BECOMES EFFICIENT WHEN YOUR POINTS ARE USUALLY AT LEAST DOUBLING_CONSTANT AWAY FROM EACH OTHER
class H2Lookup(Generic[K]):
    # increasing radius of circle by N doubles its area, in limit N approaches this constant
    DOUBLING_CONSTANT:float = 0.6931471805599472

    def __init__(self):
        self.table: dict[HASH_CODE, K] = {}

    @property
    def bin_count(self) -> int:
        return len(self.table.keys())

    def get(self, key: H2Vector | HASH_CODE, default_value: K=None) -> K:
        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        if (key not in self.table) and (default_value is not None):
            self.table[key] = default_value

        return self.table[key]

    def __getitem__(self, key: H2Vector | HASH_CODE) -> K:
        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        return self.table[key]

    def __setitem__(self, key: H2Vector | HASH_CODE, value: K) -> None:
        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        self.table[key] = value

    def __delitem__(self, key: H2Vector | HASH_CODE) -> None:
        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        del self.table[key]

    def __contains__(self, key: H2Vector | HASH_CODE):
        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        return key in self.table

    def around(self, key: H2Vector | HASH_CODE, distance: int = 1) -> list[K]:
        assert distance >= 0

        if type(key) == H2Vector:
            key = self.vector_to_hash_code(key)

        hashes: set[HASH_CODE] = self.hashes_around(key, distance)
        objects_around: list[K] = list(map(lambda h: self[h], filter(lambda h: h in self.table,hashes)))

        return objects_around

    def hashes_around(self, key: HASH_CODE, distance: int = 1) -> set[HASH_CODE]:
        assert distance >= 0

        hashes: set[HASH_CODE] = {key}

        plus_most: HASH_CODE = key
        minus_most: HASH_CODE = key

        for _ in range(distance):
            plus_most = self.hash_plus(plus_most)
            minus_most = self.hash_minus(minus_most)

            hashes.add(plus_most)
            hashes.add(minus_most)

        topmost: set[HASH_CODE] = hashes.copy()
        bottommost: set[HASH_CODE] = hashes.copy()

        new_topmost: set[HASH_CODE] = set()
        new_bottommost: set[HASH_CODE] = set()

        for _ in range(distance):
            for hash_ in topmost:
                new_hash: HASH_CODE | None = self.hash_above(hash_)

                if new_hash is None:
                    break

                new_topmost.add(new_hash)
                hashes.add(new_hash)

            for hash_ in bottommost:
                hash1, hash2 = self.hashes_below(hash_)

                new_bottommost.add(hash1)
                new_bottommost.add(hash2)
                hashes.add(hash1)
                hashes.add(hash2)

            topmost = new_topmost
            bottommost = new_bottommost

            new_topmost = set()
            new_bottommost = set()

        return hashes

    def vector_to_hash_code(self, vector: H2Vector) -> HASH_CODE:
        theta, alpha = vector.hyperpolar
        if theta < 0:
            theta += math.tau

        alphint: int = alpha // self.DOUBLING_CONSTANT
        # alphint: int = 0 if alpha < 1 else\
        #     1 + ((alpha - 1) // self.DOUBLING_CONSTANT)
        thetint: int = round(theta, 7) // (math.tau / (2 ** alphint))

        return thetint, alphint

    def hash_code_to_vector(self, code: HASH_CODE) -> H2Vector:
        thetint, alphint = code

        if alphint == 0:
            return H2Vector()

        alpha = alphint * self.DOUBLING_CONSTANT
        #alpha = 1 + (self.DOUBLING_CONSTANT * (alphint - 1))
        theta = thetint * (math.tau / (2 ** alphint))

        return H2Vector.FromHyperpolar(theta, alpha)

    @staticmethod
    def hash_above(code: HASH_CODE) -> HASH_CODE | None:
        thetint, alphint = code

        if alphint == 0:
            return None

        return thetint // 2, alphint - 1

    @staticmethod
    def hashes_below(code: HASH_CODE) -> tuple[HASH_CODE, HASH_CODE]:
        thetint, alphint = code

        alphint += 1
        t1, t2 = thetint * 2, (thetint * 2) + 1

        return (t1, alphint), (t2, alphint)

    @staticmethod
    def hash_minus(code: HASH_CODE) -> HASH_CODE:
        thetint, alphint = code

        thetint = (thetint - 1) % (2 ** alphint)

        return thetint , alphint

    @staticmethod
    def hash_plus(code: HASH_CODE) -> HASH_CODE:
        thetint, alphint = code

        thetint = (thetint + 1) % (2 ** alphint)

        return thetint, alphint

    def get_polygons(self, detail: int=1, subdivide_lines: bool=True) -> list[H2Polygon]:
        return list(map(lambda h: self.hash_to_polygon(h, detail, subdivide_lines), self.table.keys()))

    def hash_to_polygon(self, code: HASH_CODE, detail: int=1, subdivide_lines: bool=True) -> H2Polygon:
        assert detail >= 1

        thetint, alphint = code

        if alphint == 0:
            return H2Circle(H2Vector(), self.DOUBLING_CONSTANT).approximate(2 + (2 * detail))

        d_code: HASH_CODE = self.hashes_below(code)[0]

        a: H2Vector = self.hash_code_to_vector(code)
        code = self.hash_plus(code)
        b: H2Vector = self.hash_code_to_vector(code)
        code = self.hashes_below(code)[0]
        c: H2Vector = self.hash_code_to_vector(code)
        d: H2Vector = self.hash_code_to_vector(d_code)

        arc1: H2Arc = H2Arc.ThreePoint(H2Vector(), a, b)
        arc2: H2Arc = H2Arc.ThreePoint(H2Vector(), c, d)

        if alphint == 1:
            arc1.length = abs(arc1.length)
            arc2.length *= -1 if arc2.length >= 0 else 1

        points: list[H2Vector] = arc1.approximate(2 + detail).points

        if subdivide_lines:
            line1: H2Line = H2Line(b, c)
            points += line1.approximate(2 + detail).points[1:-1]

        points += arc2.approximate(3 + 2*detail).points

        if subdivide_lines:
            line2: H2Line = H2Line(d, a)
            points += line2.approximate(2 + detail).points[1:-1]

        return H2Polygon(points)
