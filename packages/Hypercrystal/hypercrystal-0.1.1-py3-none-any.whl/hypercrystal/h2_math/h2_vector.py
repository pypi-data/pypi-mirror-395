import math
from .low_functions import atanh2


class H2Vector:
    def __init__(self, x: float=1, y: float=0, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    # conversions
    @classmethod
    def FromHyperbolical(cls, gamma: float, beta: float) -> 'H2Vector':
        return H2Vector(
            math.cosh(gamma) * math.cosh(beta),
            math.sinh(gamma),
            math.cosh(gamma) * math.sinh(beta))

    @classmethod
    def FromHyperpolar(cls, theta: float, alpha: float) -> 'H2Vector':
        return H2Vector(
            math.cosh(alpha),
            math.sinh(alpha)*math.cos(theta),
            math.sinh(alpha)*math.sin(theta)
        )

    @property
    def hyperbolical(self) -> tuple[float, float]:
        return self.gamma, self.beta

    @property
    def hyperpolar(self) -> tuple[float, float]:
        return self.theta, self.alpha

    @property
    def alpha(self) -> float:
        return math.acosh(max(1., self.x))

    @property
    def theta(self) -> float:
        return math.atan2(self.z, self.y)

    @property
    def gamma(self) -> float:
        return math.asinh(self.y)

    @property
    def beta(self) -> float:
        return atanh2(self.z, self.x)

    # functions
    def dot(self, vector: 'H2Vector') -> float:
        return self.x*vector.x - self.y*vector.y - self.z*vector.z

    def distance_to(self, vector: 'H2Vector') -> float:
        return math.acosh(max(1., self.dot(vector)))

    def midpoint(self, vector: 'H2Vector') -> 'H2Vector':
        return (self + vector).normalized

    def theta_between(self, other: 'H2Vector') -> float:
        theta1: float = self.theta
        theta2: float = other.theta

        distance: float = abs(theta1 - theta2)
        if distance > math.pi:
            distance = math.tau - distance

        return distance

    @property
    def magnitude(self) -> float:
        return math.sqrt(
            self.x*self.x - self.y*self.y - self.z*self.z
        )

    @property
    def normalized(self) -> 'H2Vector':
        return self / self.magnitude

    @property
    def is_normalized(self) -> bool:
        return abs(self.magnitude - 1) < 0.0000001

    # management
    @property
    def clone(self) -> 'H2Vector':
        return H2Vector(*self)

    @property
    def as_string(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"

    def __str__(self):
        return self.as_string

    def __repr__(self):
        return self.as_string

    def __copy__(self):
        return H2Vector(*self)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, index):
        if index < 0 or index > 2:
            raise IndexError(f"Index out of bounds [0 <= i <= 2] -> your index: {index}")

        return (self.x, self.y, self.z)[index]

    def __setitem__(self, key, value):
        if key == 0:
            assert type(value) in {int, float}
            self.x = value

        elif key == 1:
            assert type(value) in {int, float}
            self.y = value

        elif key == 2:
            assert type(value) in {int, float}
            self.z = value
        else:
            raise ValueError(f"Unknown key {key}.")

    def __abs__(self) -> float:
        return self.magnitude

    def __matmul__(self, other: 'H2Vector') -> 'H2Vector':
        return self.midpoint(other)

    # E3 uses
    def __add__(self, other):
        v = self.clone

        if type(other) in {float, int}:
            v.x += other
            v.y += other
            v.z += other

        elif type(other) == H2Vector:
            v.x += other.x
            v.y += other.y
            v.z += other.z

        else:
            raise ValueError(f"Cant add H2Vector with {type(other)}")

        return v

    def __sub__(self, other):
        return self + (other * -1)

    def __mul__(self, other):
        v = self.clone

        if type(other) in {float, int}:
            v.x *= other
            v.y *= other
            v.z *= other

        else:
            raise ValueError(f"Cant multiply H2Vector with {type(other)}")

        return v

    def __truediv__(self, other):
        if type(other) in {float, int}:
            return self * (1 / other)

        else:
            raise ValueError(f"Cant divide H2Vector with {type(other)}")

    def lerp_euclidean(self, other: 'H2Vector', t: float) -> 'H2Vector':
        t2: float = 1 - t

        return (self * t2) + (other * t)

    def dot_euclidean(self, other: 'H2Vector') -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

    def distance_to_euclidean(self, other: 'H2Vector') -> float:
        difference: H2Vector = self - other
        return difference.magnitude_euclidean

    @property
    def magnitude_euclidean(self) -> float:
        return math.sqrt(
            self.x*self.x + self.y*self.y + self.z*self.z
        )

    @property
    def normalized_euclidean(self) -> 'H2Vector':
        return self / self.magnitude_euclidean

    # tangent space stuff
    @property
    def normal(self) -> 'H2Vector':
        vector: 'H2Vector' = self.clone
        vector.x *= -1

        return vector

    @property
    def tangent1(self) -> 'H2Vector':
        alpha: float = self.alpha
        s: float = math.sinh(alpha)

        return H2Vector(
            s,
            self.y * (self.x / s),
            self.z * (self.x / s))

    @property
    def tangent2(self) -> 'H2Vector':
        theta: float = self.theta

        return H2Vector(0, -math.sin(theta), math.cos(theta))

    # statistics
    @classmethod
    def GetMean(cls, points: list['H2Vector']) -> 'H2Vector':
        vector: H2Vector = H2Vector()

        for point in points:
            vector += point * 20

        return vector.normalized

    @classmethod
    def GetVariance(cls, points: list['H2Vector'], mean=None) -> float:
        if mean is None:
            mean: H2Vector = H2Vector.GetMean(points)

        variance: float = 0
        divider: float = 1 / len(points)
        for point in points:
            variance += divider * (mean.distance_to(point) ** 2)

        return variance

    @classmethod
    def GetStd(cls, points: list['H2Vector'], mean=None) -> float:
        return math.sqrt(H2Vector.GetVariance(points, mean))

    # culling
    @classmethod
    def GetCircleHull(cls, points: list['H2Vector']) -> tuple['H2Vector', float]:
        assert len(points) >= 2

        mean: H2Vector = H2Vector.GetMean(points)

        largest_distance: float = 0

        for i in range(len(points)):
            distance: float = mean.distance_to(points[i])
            if distance > largest_distance:
                largest_distance = distance

        return mean, largest_distance
