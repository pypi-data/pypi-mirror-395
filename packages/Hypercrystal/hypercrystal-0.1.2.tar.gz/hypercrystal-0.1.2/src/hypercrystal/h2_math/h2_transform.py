import math

from .h2_vector import H2Vector
from .matrix3D import Matrix3D


class H2Transform(Matrix3D):
    def __init__(self):
        identity: Matrix3D = Matrix3D.get_identity()
        super().__init__(identity.i, identity.j, identity.k)

    @classmethod
    def Identity(cls) -> 'H2Transform':
        return H2Transform()

    @classmethod
    def Plane(cls, axis: str, angle: float) -> 'H2Transform':
        if axis == "zy":
            axis = "yz"
            angle *= -1

        elif axis == "yx":
            axis = "xy"
            angle *= -1

        elif axis == "zx":
            axis = "xz"
            angle *= -1

        m: H2Transform = cls.Identity()

        if axis == "yz":
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)

            m.j.y = cos_angle
            m.j.z = sin_angle

            m.k.y = -sin_angle
            m.k.z = cos_angle

        elif axis == "xy":
            cosh_angle = math.cosh(angle)
            sinh_angle = math.sinh(angle)

            m.i.x = cosh_angle
            m.i.y = sinh_angle

            m.j.x = sinh_angle
            m.j.y = cosh_angle

        elif axis == "xz":
            cosh_angle = math.cosh(angle)
            sinh_angle = math.sinh(angle)

            m.i.x = cosh_angle
            m.i.z = sinh_angle

            m.k.x = sinh_angle
            m.k.z = cosh_angle

        else:
            raise ValueError(f"Axis needs to be of form [xy, xz, yz, yx, zy, zx], your axis: {axis}")

        return m

    @classmethod
    def Point(cls, p: H2Vector) -> 'H2Transform':
        transform: H2Transform = cls.Plane("zy", p.theta)
        return transform.before(cls.Plane("yx", p.alpha))

    @classmethod
    def PointInverse(cls, p: H2Vector) -> 'H2Transform':
        transform: H2Transform = cls.Plane("xy", p.alpha)
        return transform.before(cls.Plane("yz", p.theta))

    @classmethod
    def Around(cls, p: H2Vector, angle: float) -> 'H2Transform':
        transform: H2Transform = cls.Point(p)
        transform = transform.before(cls.Plane("yz", angle))
        return transform.before(cls.PointInverse(p))

    @classmethod
    def LineToXY(cls, a: H2Vector, b: H2Vector) -> 'H2Transform':
        transform: H2Transform = cls.Point(a)
        b_: H2Vector = transform.apply_on_vector(b)
        return transform.before(cls.Plane("zy", b_.theta))

    @classmethod
    def LineToXZ(cls, a: H2Vector, b: H2Vector) -> 'H2Transform':
        transform: H2Transform = cls.Point(a)
        b_: H2Vector = transform.apply_on_vector(b)
        return transform.before(cls.Plane("zy", b_.theta - cls.HALF_PI))

    @classmethod
    def AtoB(cls, a: H2Vector, b: H2Vector, angle: float) -> 'H2Transform':
        transform: H2Transform = cls.LineToXY(a, b)
        movement: H2Transform = cls.Plane("xy", angle)
        return transform.before(movement.before(transform.inverse))

    @classmethod
    def LerpAB(cls, a: H2Vector, b: H2Vector, t: float) -> 'H2Transform':
        return cls.AtoB(a, b, a.distance_to(b) * t)

    @classmethod
    def StraightToA(cls, a: H2Vector) -> 'H2Transform':
        return cls.AtoB(H2Vector(), a, a.alpha)

    @classmethod
    def StraightToOrigin(cls, a: H2Vector) -> 'H2Transform':
        return cls.AtoB(a, H2Vector(), a.alpha)

    @classmethod
    def Anchor(cls, position: H2Vector, rotation: float) -> 'H2Transform':
        transform: H2Transform = H2Transform.Plane("yz", rotation)
        transform = transform.before(H2Transform.StraightToA(position))
        return transform

    @classmethod
    def AnchorInverse(cls, position: H2Vector, rotation: float) -> 'H2Transform':
        transform: H2Transform = H2Transform.StraightToOrigin(position)
        transform = transform.before(H2Transform.Plane("zy", rotation))
        return transform


if __name__ == '__main__':
    print("Test 1")

    a_ = H2Vector.FromHyperpolar(0.89, 3.56)

    t = H2Transform.Point(a_)
    t_inv = H2Transform.PointInverse(a_)
    print(a_.hyperpolar)

    print(t.apply_on_vector(a_))
    print(t_inv.apply_on_vector(t.apply_on_vector(a_)).hyperpolar)

    print("Test 2")

    b_ = H2Vector.FromHyperbolical(-4.1, -7.2)
    print(b_.hyperbolical)

    t_lerp = H2Transform.LerpAB(a_, b_, 1)
    print(t_lerp.apply_on_vector(a_).hyperbolical)
