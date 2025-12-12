import math
from ..notation import untested

def atanh2(y: float, x: float) -> float:
    magnitude: float = math.sqrt(x*x - y*y)

    return math.asinh(y / magnitude)


def c_from_angles(alpha: float, beta: float, gamma: float) -> float:
    return math.acosh(
        ( math.cos(gamma) + math.cos(alpha)*math.cos(beta) )
        / ( math.sin(alpha)*math.sin(beta) )
    )

@untested
def gamma_from_sidelengths(a: float, b: float, c: float) -> float:
    return math.acos(
        ( math.cosh(a)*math.cosh(b) - math.cosh(c) )
        / ( math.sinh(a)*math.sinh(b) )
    )

@untested
def b_from_sine_law(a: float, alpha: float, beta: float) -> float:
    return math.asinh( ( math.sinh(a)*math.sin(beta) ) / math.sin(alpha) )

@untested
def beta_from_sine_law(a: float, alpha: float, b: float) -> float:
    return math.asin( ( math.sin(alpha)*math.sinh(b) ) / math.sinh(a) )


def pythagorean_get_c(a: float, b: float) -> float:
    return math.acosh( math.cosh(a)*math.cosh(b) )


def pythagorean_get_a(b: float, c: float) -> float:
    return math.acosh( math.cosh(c) / math.cosh(b) )


def pythagorean_get_b(a: float, c: float) -> float:
    return pythagorean_get_a(a, c)
