import math
from .h2_vector import H2Vector
from .h2_transform import H2Transform
from ..notation import untested


def angleAtB(a: H2Vector, b: H2Vector, c: H2Vector) -> float:
    point_b: H2Transform = H2Transform.Point(b)

    a_: H2Vector = point_b.apply_on_vector(a)
    c_: H2Vector = point_b.apply_on_vector(c)

    return a_.theta_between(c_)

def is_clockwise(a: H2Vector, b: H2Vector, c: H2Vector) -> bool:
    transform: H2Transform = H2Transform.LineToXY(a, b)

    c_: H2Vector = transform.apply_on_vector(c)

    return c_.z >= 0

@untested
def project(a: H2Vector, b: H2Vector) -> H2Vector:
    a_normal: H2Vector = a.normal.normalized_euclidean
    b_: H2Vector = b - (a_normal * b.dot_euclidean(a_normal))
    return b_

@untested
def reproject(a: H2Vector, b_: H2Vector) -> H2Vector:
    point_a: H2Transform = H2Transform.Point(a)
    point_a_inverse: H2Transform = H2Transform.PointInverse(a)

    b__: H2Vector = point_a.apply_on_vector(b_)
    b__.x = math.sqrt(1 + b__.y*b__.y + b__.z*b__.z)

    return point_a_inverse.apply_on_vector(b__)
